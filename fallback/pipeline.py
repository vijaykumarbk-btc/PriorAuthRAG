"""
Single entry point and orchestrator for PDF processing:
- Checks page count up front cheaply with pypdf
- Routes to Docling + hierarchical-pdf pipeline (<= threshold) or Tiered Bookmark pipeline (> threshold)
- Escalates to Tiered Bookmark pipeline if sanity check fails on <= threshold docs
- Standardizes output into .hierarchical.md, .hierarchical.json, and .qa_report.json
"""

import os
import json
import logging
from pathlib import Path
from typing import List, Dict, Optional, Tuple, Any

from docling.datamodel.base_models import InputFormat
from docling.datamodel.pipeline_options import PdfPipelineOptions
from docling.document_converter import DocumentConverter, PdfFormatOption
from docling_core.types.doc import TextItem, TableItem, SectionHeaderItem, TitleItem, ListItem

from fallback.config import PipelineConfig, ProcessingResult
from fallback.extractors import (
    get_pdf_page_count,
    extract_bookmarks_tier1,
    extract_toc_regex_tier2,
    calibrate_page_offset,
    compute_string_similarity
)
from fallback.builder import (
    assemble_normalized_blocks,
    generate_markdown_from_blocks,
    generate_qa_report
)

logger = logging.getLogger("fallback_pipeline")
logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(name)s: %(message)s")


def _get_item_label(item) -> str:
    label = getattr(item, "label", None)
    if label is not None:
        label_str = str(label).lower()
        if "title" in label_str:
            return "title"
        if "section_header" in label_str:
            return "heading"
        if "list" in label_str:
            return "list"
        if "caption" in label_str:
            return "caption"
        if "formula" in label_str:
            return "formula"
        return "paragraph"
    return item.__class__.__name__.lower()


def _get_provenance(item) -> Tuple[Optional[int], Optional[List[float]]]:
    prov_list = getattr(item, "prov", None)
    if not prov_list:
        return None, None
    prov = prov_list[0]
    page = getattr(prov, "page_no", None)
    bbox = getattr(prov, "bbox", None)
    if bbox:
        return page, [bbox.l, bbox.t, bbox.r, bbox.b]
    return page, None


def _get_item_text(item, document) -> str:
    if isinstance(item, TableItem):
        try:
            return item.export_to_markdown(doc=document)
        except Exception:
            return str(item)
    text = getattr(item, "text", None)
    if text is not None:
        return text
    return ""


def _extract_docling_raw_items(document) -> List[Dict[str, Any]]:
    """Extract raw flat items directly from Docling document.iterate_items()."""
    raw_items = []
    reading_order = 0

    for item, level in document.iterate_items():
        reading_order += 1
        item_type = _get_item_label(item)
        item_text = _get_item_text(item, document)
        page, bbox = _get_provenance(item)

        entry = {
            "reading_order": reading_order,
            "type": item_type,
            "text": item_text,
            "level": level,
            "page": page,
            "bbox": bbox,
            "item": item
        }

        if isinstance(item, TableItem):
            entry["type"] = "table"
            try:
                df = item.export_to_dataframe(doc=document)
                entry["table"] = {
                    "headers": [str(c) for c in df.columns],
                    "rows": [[val for val in row] for row in df.values.tolist()]
                }
            except Exception as e:
                entry["table"] = {"error": str(e)}

        raw_items.append(entry)

    return raw_items


# =========================================================================
# PIPELINE 1: EXISTING DOCLING HIERARCHICAL POSTPROCESSOR
# =========================================================================
def run_docling_hierarchical_pipeline(
    pdf_path: Path,
    config: PipelineConfig
) -> Tuple[List[Dict[str, Any]], str, Dict[str, Any]]:
    """
    Runs:
    1. Docling conversion
    2. docling-hierarchical-pdf ResultPostprocessor
    3. Document export
    """
    logger.info("Executing main pipeline (Docling + hierarchical ResultPostprocessor) for %s", pdf_path.name)
    pipeline_options = PdfPipelineOptions()
    pipeline_options.do_ocr = config.enable_ocr

    converter = DocumentConverter(
        format_options={
            InputFormat.PDF: PdfFormatOption(pipeline_options=pipeline_options)
        }
    )

    conv_result = converter.convert(str(pdf_path))

    # Run postprocessor
    try:
        from hierarchical.postprocessor import ResultPostprocessor
        logger.info("Running ResultPostprocessor on conversion result...")
        ResultPostprocessor(conv_result).process()
    except Exception as e:
        logger.warning("ResultPostprocessor failed or raised error: %s", e)

    doc = conv_result.document
    raw_items = _extract_docling_raw_items(doc)

    # Mark heading source
    for entry in raw_items:
        if entry["type"] in {"heading", "title"}:
            entry["type"] = "heading"
            entry["heading_level"] = entry["level"] or 1
            entry["heading_source"] = "docling_hierarchical"
            entry["match_confidence"] = 1.0

    blocks = assemble_normalized_blocks(raw_items)

    # Export markdown: try document.export_to_markdown() first
    try:
        exported_md = doc.export_to_markdown()
    except Exception as e:
        logger.warning("doc.export_to_markdown() failed (%s); building from blocks", e)
        exported_md = generate_markdown_from_blocks(blocks)

    meta = {"docling_document": doc, "raw_items": raw_items}
    return blocks, exported_md, meta


# =========================================================================
# PIPELINE 2: NEW TIERED BOOKMARK-FIRST PIPELINE
# =========================================================================
def run_tiered_bookmark_pipeline(
    pdf_path: Path,
    config: PipelineConfig,
    preconverted_doc=None
) -> Tuple[List[Dict[str, Any]], str, Optional[int], List[Dict[str, Any]]]:
    """
    Runs tiered heading detection:
    Tier 1: Bookmarks / Outline via pypdf
    Tier 2: Visual TOC page text regex
    Tier 3: Docling native SectionHeaderItem/TitleItem
    Tier 4: Unstructured fallback
    With page offset calibration and per-entry fallback.
    """
    logger.info("Executing NEW tiered bookmark-first pipeline for %s", pdf_path.name)

    # 1. Plain Docling conversion (no postprocessor)
    if preconverted_doc is None:
        logger.info("Running plain Docling conversion (do_ocr=%s)...", config.enable_ocr)
        pipeline_options = PdfPipelineOptions()
        pipeline_options.do_ocr = config.enable_ocr
        converter = DocumentConverter(
            format_options={
                InputFormat.PDF: PdfFormatOption(pipeline_options=pipeline_options)
            }
        )
        conv_result = converter.convert(str(pdf_path))
        preconverted_doc = conv_result.document

    raw_items = _extract_docling_raw_items(preconverted_doc)

    # In tiered pipeline, we bypass Docling's default heading detection:
    # reset item types to paragraph until promoted by Tier 1/2/3
    for entry in raw_items:
        if entry["type"] not in {"table", "list", "caption", "formula"}:
            entry["orig_type"] = entry["type"]
            entry["type"] = "paragraph"
            entry["heading_level"] = None
            entry["heading_source"] = None
            entry["match_confidence"] = None

    # Gather candidate tiers
    # Tier 1
    tier1_entries = extract_bookmarks_tier1(pdf_path)
    # Tier 2
    tier2_entries = extract_toc_regex_tier2(pdf_path)

    # Calibration: compute page offset using best available candidate entries
    calibration_candidates = tier1_entries if tier1_entries else tier2_entries
    offset = calibrate_page_offset(calibration_candidates, raw_items, sample_count=5)
    logger.info("Calibrated page offset for matching: %s", offset)

    # Check tier health document-wide
    # If a tier produces fewer than min_confident_matches_before_fallback, fall back to next tier
    active_tier = None
    if len(tier1_entries) >= config.min_confident_matches_before_fallback:
        active_tier = 1
        primary_entries = tier1_entries
        secondary_entries = tier2_entries
    elif len(tier2_entries) >= config.min_confident_matches_before_fallback:
        logger.info("Tier 1 had fewer than %d entries; falling back to Tier 2 document-wide.", config.min_confident_matches_before_fallback)
        active_tier = 2
        primary_entries = tier2_entries
        secondary_entries = []
    else:
        logger.info("Tiers 1 & 2 both produced fewer than %d entries; falling back to Tier 3 (Docling native).", config.min_confident_matches_before_fallback)
        active_tier = 3
        primary_entries = []
        secondary_entries = []

    unmatched_entries: List[Dict[str, Any]] = []
    matched_block_indices = set()

    def match_entry_to_blocks(
        entry: Dict[str, Any],
        source_label: str
    ) -> Tuple[Optional[int], float]:
        title = entry["title"]
        stated_page = entry.get("page")
        best_idx = None
        best_ratio = 0.0

        # Determine page search window adjusted by offset
        candidate_blocks = []
        if stated_page is not None and offset is not None:
            target_page = stated_page + offset
            min_page = target_page - config.page_search_window
            max_page = target_page + config.page_search_window
            candidate_blocks = [
                (idx, b) for idx, b in enumerate(raw_items)
                if b.get("page") is not None and min_page <= b["page"] <= max_page
            ]

        # If window yielded no blocks, search document-wide
        if not candidate_blocks:
            candidate_blocks = list(enumerate(raw_items))

        for idx, b in candidate_blocks:
            if idx in matched_block_indices:
                continue
            ratio = compute_string_similarity(title, b.get("text", ""))
            if ratio > best_ratio:
                best_ratio = ratio
                best_idx = idx

        if best_ratio >= config.min_match_ratio and best_idx is not None:
            return best_idx, best_ratio

        return None, best_ratio

    # Match primary entries with per-entry fallback
    if active_tier in (1, 2):
        for entry in primary_entries:
            src_label = "bookmark_tier1" if active_tier == 1 else "toc_tier2"
            best_idx, best_ratio = match_entry_to_blocks(entry, src_label)

            if best_idx is not None:
                matched_block_indices.add(best_idx)
                raw_items[best_idx]["type"] = "heading"
                raw_items[best_idx]["heading_level"] = entry.get("level", 1)
                raw_items[best_idx]["heading_source"] = src_label
                raw_items[best_idx]["match_confidence"] = round(best_ratio, 3)
            else:
                # Per-entry fallback: try secondary tier for THIS entry if available
                fell_back_success = False
                if secondary_entries:
                    for s_entry in secondary_entries:
                        s_idx, s_ratio = match_entry_to_blocks(s_entry, "toc_tier2")
                        if s_idx is not None:
                            matched_block_indices.add(s_idx)
                            raw_items[s_idx]["type"] = "heading"
                            raw_items[s_idx]["heading_level"] = s_entry.get("level", 1)
                            raw_items[s_idx]["heading_source"] = "toc_tier2"
                            raw_items[s_idx]["match_confidence"] = round(s_ratio, 3)
                            fell_back_success = True
                            break

                if not fell_back_success:
                    logger.warning("Unmatched entry '%s' (stated page: %s, best ratio: %.3f)", entry["title"], entry.get("page"), best_ratio)
                    unmatched_entries.append({
                        "title": entry["title"],
                        "stated_page": entry.get("page"),
                        "best_ratio": round(best_ratio, 3),
                        "source": src_label
                    })

    # Tier 3: Native Docling headers (if active_tier == 3 or as supplementary)
    if active_tier == 3:
        native_count = 0
        for entry in raw_items:
            orig_type = entry.get("orig_type") or entry.get("type")
            if orig_type in {"heading", "title", "section_header"}:
                entry["type"] = "heading"
                entry["heading_level"] = entry.get("level") or 1
                entry["heading_source"] = "docling_native_tier3"
                entry["match_confidence"] = 0.85
                native_count += 1

        if native_count == 0:
            logger.warning("Tier 3 (Docling native) found 0 headings. Falling back to Tier 4 (Unstructured).")

    # Tier 4: Check if anything became a heading
    total_headings_found = sum(1 for b in raw_items if b.get("type") == "heading")
    if total_headings_found == 0:
        logger.warning("Tier 4 reached: Document has no structure detected. Marking as unstructured.")

    blocks = assemble_normalized_blocks(raw_items)
    # Generate markdown directly from blocks for tiered path
    markdown_text = generate_markdown_from_blocks(blocks)

    return blocks, markdown_text, offset, unmatched_entries


# =========================================================================
# MAIN ROUTER: PROCESS_PDF
# =========================================================================
def process_pdf(
    pdf_path: Path,
    output_dir: Path,
    config: Optional[PipelineConfig] = None
) -> ProcessingResult:
    """
    Single public entry point for PDF processing with intelligent routing:
    - Page count threshold routing (> 300 pages uses Tiered Bookmark pipeline)
    - Post-hoc sanity check with automatic escalation
    - Shared flat-block JSON, hierarchical markdown, and QA report generation
    """
    if config is None:
        config = PipelineConfig()

    pdf_path = Path(pdf_path).resolve()
    output_dir = Path(output_dir).resolve()
    output_dir.mkdir(parents=True, exist_ok=True)

    if not pdf_path.exists():
        raise FileNotFoundError(f"PDF file not found: {pdf_path}")

    # 1. Check page count cheaply up front
    page_count = get_pdf_page_count(pdf_path)
    logger.info("Loaded '%s' with %d pages (Threshold: %d)", pdf_path.name, page_count, config.page_count_threshold)

    pipeline_used = ""
    escalated = False
    blocks: List[Dict[str, Any]] = []
    markdown_text = ""
    detected_offset = None
    unmatched_entries: List[Dict[str, Any]] = []
    extra_warnings: List[str] = []

    # 2. Routing decision
    if page_count <= config.page_count_threshold:
        pipeline_used = "docling_hierarchical"
        try:
            blocks, markdown_text, meta = run_docling_hierarchical_pipeline(pdf_path, config)
        except Exception as e:
            logger.error("Main pipeline threw an exception: %s; Escalating to tiered pipeline.", e)
            escalated = True
            extra_warnings.append(f"ESCALATION: Main pipeline failed with error: {e}")

        # Post-hoc sanity check for <= 300 page documents
        if not escalated:
            num_headings = sum(1 for b in blocks if b.get("type") == "heading")
            min_expected = max(1.0, (page_count / 20.0) * config.min_headings_per_20_pages)
            
            is_suspiciously_low = (num_headings < min_expected)
            is_near_zero = (page_count > 20 and num_headings < 3)

            if is_suspiciously_low or is_near_zero:
                warn = (
                    f"ESCALATION TRIGGERED: Detected headings ({num_headings}) suspiciously low "
                    f"relative to {page_count} pages (expected >= {min_expected:.1f}). "
                    f"Escalating document to tiered_bookmark_fallback pipeline."
                )
                logger.warning(warn)
                extra_warnings.append(warn)
                escalated = True

        # Run escalation if triggered
        if escalated:
            pipeline_used = "tiered_bookmark_fallback"
            preconverted = meta.get("docling_document") if "meta" in locals() and meta else None
            blocks, markdown_text, detected_offset, unmatched_entries = run_tiered_bookmark_pipeline(
                pdf_path, config, preconverted_doc=preconverted
            )

    else:
        # > 300 pages: route directly to tiered bookmark pipeline
        logger.info("Page count (%d) exceeds threshold (%d). Routing directly to tiered_bookmark_fallback.", page_count, config.page_count_threshold)
        pipeline_used = "tiered_bookmark_fallback"
        blocks, markdown_text, detected_offset, unmatched_entries = run_tiered_bookmark_pipeline(
            pdf_path, config
        )

    # 3. Generate QA Report
    qa_report = generate_qa_report(
        pipeline_used=pipeline_used,
        escalated_from_main=escalated,
        page_count=page_count,
        blocks=blocks,
        markdown_text=markdown_text,
        detected_page_offset=detected_offset,
        unmatched_entries=unmatched_entries,
        extra_warnings=extra_warnings
    )

    # 4. Save Artifacts
    stem = pdf_path.stem
    md_file = output_dir / f"{stem}.hierarchical.md"
    json_file = output_dir / f"{stem}.hierarchical.json"
    qa_file = output_dir / f"{stem}.qa_report.json"

    with open(md_file, "w", encoding="utf-8") as f:
        f.write(markdown_text)

    with open(json_file, "w", encoding="utf-8") as f:
        json.dump(blocks, f, indent=2, ensure_ascii=False)

    with open(qa_file, "w", encoding="utf-8") as f:
        json.dump(qa_report, f, indent=2, ensure_ascii=False)

    logger.info("Outputs written to:")
    logger.info("  Markdown : %s", md_file)
    logger.info("  JSON     : %s", json_file)
    logger.info("  QA Report: %s", qa_file)

    return ProcessingResult(
        pdf_path=pdf_path,
        output_dir=output_dir,
        pipeline_used=pipeline_used,
        escalated_from_main=escalated,
        page_count=page_count,
        total_blocks=qa_report["total_blocks"],
        total_headings=qa_report["total_headings"],
        total_tables=qa_report["total_tables"],
        heading_source_breakdown=qa_report["heading_source_breakdown"],
        detected_page_offset=detected_offset,
        unmatched_entries=unmatched_entries,
        warnings=qa_report["warnings"],
        markdown_path=md_file,
        json_path=json_file,
        qa_report_path=qa_file
    )
