"""
Normalized block assembly, section hierarchy tracking, markdown generation, and QA report generation.
"""

import logging
from collections import Counter
from pathlib import Path
from typing import List, Dict, Optional, Any

logger = logging.getLogger("fallback_pipeline")


def detect_section_level(headings: List[Dict[str, Any]]) -> Optional[int]:
    """
    Determine which heading level appears to represent major sections in THIS document.
    """
    if not headings:
        return None

    level_counts = Counter(
        h["heading_level"]
        for h in headings
        if h.get("heading_level") is not None
    )

    if not level_counts:
        return None

    levels = sorted(level_counts.keys())
    for level in levels:
        if level_counts[level] >= 2:
            return level

    return levels[0]


def assemble_normalized_blocks(raw_items: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    """
    Takes flat raw items (with types, heading_level, text, page, bbox, table)
    and constructs the shared flat block contract with:
    - block_id ("b00001")
    - reading_order
    - heading_stack & heading_path
    - parent_heading & parent_heading_id
    - section_id ("s0001") & section_title
    """
    headings = [it for it in raw_items if it.get("type") == "heading"]
    section_level = detect_section_level(headings)
    logger.info("Detected section level for document: %s (from %d headings)", section_level, len(headings))

    blocks: List[Dict[str, Any]] = []
    heading_stack: Dict[int, Dict[str, Any]] = {}
    current_section_id: Optional[str] = None
    current_section_title: Optional[str] = None
    section_counter = 0

    for idx, entry in enumerate(raw_items):
        reading_order = idx + 1
        block_id = f"b{reading_order:05d}"
        item_type = entry.get("type", "paragraph")
        item_text = entry.get("text", "")
        level = entry.get("heading_level")
        page = entry.get("page")
        bbox = entry.get("bbox")
        heading_source = entry.get("heading_source")
        match_confidence = entry.get("match_confidence")

        is_heading = (item_type == "heading" and level is not None)

        if is_heading:
            # Check major section
            if section_level is not None and level == section_level:
                section_counter += 1
                current_section_id = f"s{section_counter:04d}"
                current_section_title = item_text.strip()

            # Clean deeper levels from stack
            for old_level in list(heading_stack.keys()):
                if old_level >= level:
                    del heading_stack[old_level]

            heading_stack[level] = {
                "block_id": block_id,
                "text": item_text.strip(),
                "level": level
            }

            heading_path = [
                heading_stack[lvl]["text"]
                for lvl in sorted(heading_stack)
            ]

            parent_levels = [l for l in heading_stack if l < level]
            if parent_levels:
                parent_lvl = max(parent_levels)
                parent_heading = heading_stack[parent_lvl]["text"]
                parent_heading_id = heading_stack[parent_lvl]["block_id"]
            else:
                parent_heading = None
                parent_heading_id = None

        else:
            # Non-heading item inherits context from current heading stack
            if heading_stack:
                current_top_lvl = max(heading_stack)
                parent_heading = heading_stack[current_top_lvl]["text"]
                parent_heading_id = heading_stack[current_top_lvl]["block_id"]
                heading_path = [
                    heading_stack[lvl]["text"]
                    for lvl in sorted(heading_stack)
                ]
            else:
                parent_heading = None
                parent_heading_id = None
                heading_path = []

        block = {
            "block_id": block_id,
            "reading_order": reading_order,
            "type": item_type,
            "heading_level": level if is_heading else None,
            "heading_source": heading_source if is_heading else None,
            "match_confidence": match_confidence if is_heading else None,
            "text": item_text,
            "page": page,
            "bbox": bbox,
            "section_id": current_section_id,
            "section_title": current_section_title,
            "parent_heading_id": parent_heading_id,
            "parent_heading": parent_heading,
            "heading_path": heading_path,
        }

        if item_type == "table" and "table" in entry:
            block["table"] = entry["table"]

        blocks.append(block)

    return blocks


def generate_markdown_from_blocks(blocks: List[Dict[str, Any]]) -> str:
    """
    Builds markdown directly from the normalized flat blocks:
    - Heading levels produce corresponding '#' count (e.g. 1 -> '#', 2 -> '##')
    - Tables format as markdown tables
    - Paragraphs and lists format with standard double-newlines
    """
    lines: List[str] = []

    for b in blocks:
        b_type = b.get("type")
        text = (b.get("text") or "").strip()

        if b_type == "heading":
            lvl = b.get("heading_level") or 1
            # Bound level between 1 and 6 for markdown standard
            clamped_lvl = max(1, min(lvl, 6))
            hashes = "#" * clamped_lvl
            lines.append(f"\n{hashes} {text}\n")

        elif b_type == "table" and "table" in b and "headers" in b["table"]:
            tbl = b["table"]
            headers = tbl.get("headers", [])
            rows = tbl.get("rows", [])
            if headers:
                header_line = "| " + " | ".join(str(h).replace("\n", " ") for h in headers) + " |"
                separator_line = "| " + " | ".join("---" for _ in headers) + " |"
                tbl_lines = [header_line, separator_line]
                for row in rows:
                    tbl_lines.append("| " + " | ".join(str(cell).replace("\n", " ") for cell in row) + " |")
                lines.append("\n" + "\n".join(tbl_lines) + "\n")
            elif text:
                lines.append(f"\n{text}\n")

        elif b_type == "list":
            lines.append(f"- {text}")

        else:
            if text:
                lines.append(f"\n{text}\n")

    md_content = "\n".join(lines).strip()
    return md_content


def generate_qa_report(
    pipeline_used: str,
    escalated_from_main: bool,
    page_count: int,
    blocks: List[Dict[str, Any]],
    markdown_text: str,
    detected_page_offset: Optional[int],
    unmatched_entries: List[Dict[str, Any]],
    extra_warnings: Optional[List[str]] = None
) -> Dict[str, Any]:
    """
    Generates structured QA report and checks sanity flags:
    - heading count near zero on document >20 pages
    - heading density implausibly high (>1 heading per paragraph)
    - markdown hash-line count not matching JSON heading count
    """
    warnings: List[str] = list(extra_warnings or [])

    total_blocks = len(blocks)
    total_headings = sum(1 for b in blocks if b.get("type") == "heading")
    total_tables = sum(1 for b in blocks if b.get("type") == "table")
    total_paragraphs = sum(1 for b in blocks if b.get("type") == "paragraph")

    # Count sources
    source_counts: Dict[str, int] = {}
    for b in blocks:
        if b.get("type") == "heading":
            src = b.get("heading_source") or "unspecified"
            source_counts[src] = source_counts.get(src, 0) + 1

    # Sanity flag 1: heading count near zero on document >20 pages
    if page_count > 20 and total_headings < 3:
        warn = f"SANITY ALERT: Heading count is suspiciously low ({total_headings}) for a {page_count}-page document."
        warnings.append(warn)
        logger.warning(warn)

    # Sanity flag 2: heading density implausibly high
    if total_paragraphs > 0 and (total_headings / total_paragraphs) > 1.0:
        warn = f"SANITY ALERT: Heading density is implausibly high ({total_headings} headings vs {total_paragraphs} paragraphs)."
        warnings.append(warn)
        logger.warning(warn)

    # Sanity flag 3: markdown hash-line count not matching JSON heading count
    md_hash_lines = sum(
        1 for line in markdown_text.splitlines()
        if line.strip().startswith("#") and len(line.strip().split()[0].replace("#", "")) == 0
    )
    if md_hash_lines != total_headings:
        warn = f"SANITY ALERT: Markdown hash-line count ({md_hash_lines}) does not match JSON heading count ({total_headings})."
        warnings.append(warn)
        logger.warning(warn)

    report = {
        "pipeline_used": pipeline_used,
        "escalated_from_main": escalated_from_main,
        "page_count": page_count,
        "total_blocks": total_blocks,
        "total_headings": total_headings,
        "total_tables": total_tables,
        "heading_source_breakdown": source_counts,
        "detected_page_offset": detected_page_offset,
        "unmatched_entries": unmatched_entries,
        "warnings": warnings
    }

    return report
