"""
Extractors and text utilities:
- Page counting via pypdf
- Tier 1: Outline / Bookmarks via pypdf reader.outline
- Tier 2: Visual Table of Contents page text via regex
- Calibration: Page-offset discovery
- Fuzzy matching
"""

import re
import difflib
import logging
from pathlib import Path
from typing import List, Dict, Optional, Tuple, Any
import pypdf

logger = logging.getLogger("fallback_pipeline")


def get_pdf_page_count(pdf_path: Path) -> int:
    """Cheaply count pages using pypdf without full Docling conversion."""
    reader = pypdf.PdfReader(str(pdf_path))
    return len(reader.pages)


def extract_bookmarks_tier1(pdf_path: Path) -> List[Dict[str, Any]]:
    """
    Tier 1: Real PDF bookmarks/outline via pypdf reader.outline,
    recursively flattened to {title, level, page}. Page is 1-indexed.
    """
    reader = pypdf.PdfReader(str(pdf_path))
    outline = reader.outline

    if not outline:
        logger.info("Tier 1: No bookmarks found in PDF outline.")
        return []

    entries: List[Dict[str, Any]] = []

    def _traverse(node_list: list, level: int = 1):
        for elem in node_list:
            if isinstance(elem, list):
                _traverse(elem, level + 1)
            else:
                title = getattr(elem, "title", str(elem))
                page_idx = None
                try:
                    page_idx = reader.get_destination_page_number(elem)
                except Exception as e:
                    logger.debug("Failed resolving page number for bookmark '%s': %s", title, e)
                
                page_num = (page_idx + 1) if page_idx is not None else None
                if title and title.strip():
                    entries.append({
                        "title": title.strip(),
                        "level": level,
                        "page": page_num,
                        "source": "bookmark_tier1"
                    })

    _traverse(outline, level=1)
    logger.info("Tier 1: Extracted %d flattened bookmarks from outline.", len(entries))
    return entries


def extract_toc_regex_tier2(pdf_path: Path, max_pages: int = 15) -> List[Dict[str, Any]]:
    """
    Tier 2: Visual Table-of-Contents page text, parsed via regex for dot-leader
    patterns ('Section Title.......123') on the first ~15 pages.
    Handles wrapped titles across lines.
    """
    reader = pypdf.PdfReader(str(pdf_path))
    num_pages = len(reader.pages)
    search_limit = min(max_pages, num_pages)

    toc_pages = []
    # Find TOC pages
    for pno in range(search_limit):
        text = reader.pages[pno].extract_text() or ""
        lower = text.lower()
        if "table of contents" in lower or "contents" in lower:
            toc_pages.append(pno)
        elif toc_pages and pno == toc_pages[-1] + 1:
            if re.search(r"[\.·…]{2,}\s*\d+", text) or "guideline" in lower:
                toc_pages.append(pno)

    if not toc_pages:
        logger.info("Tier 2: No TOC pages identified in first %d pages.", search_limit)
        return []

    entries: List[Dict[str, Any]] = []
    for pno in toc_pages:
        text = reader.pages[pno].extract_text() or ""
        lines = text.splitlines()
        buffer_title = ""

        for line in lines:
            line_str = line.strip()
            if not line_str:
                continue

            # Skip header/footer noise
            lower_line = line_str.lower()
            if any(h in lower_line for h in ["table of contents", "cigna:", "guideline", "v1.", "page"]):
                if not re.search(r"[\.·…]{2,}\s*\d+$", line_str):
                    continue

            # Dot leader regex: title followed by 2 or more dots/spaces and ending in a number
            match = re.search(r"^(.+?)[\.·…\s]{2,}\s*(\d+)$", line_str)
            if match:
                title_part = match.group(1).strip(". ")
                page_num = int(match.group(2))
                full_title = f"{buffer_title} {title_part}".strip()
                buffer_title = ""
                entries.append({
                    "title": full_title,
                    "level": 1,
                    "page": page_num,
                    "source": "toc_tier2"
                })
            else:
                # Potential wrapped title line
                if len(line_str) > 3 and not line_str.isdigit():
                    buffer_title = f"{buffer_title} {line_str}".strip()

    logger.info("Tier 2: TOC regex matched %d candidate lines across %d pages.", len(entries), len(toc_pages))
    return entries


def normalize_for_matching(text: str) -> str:
    """Normalize titles and candidate block text: lowercase, collapse whitespace, strip punctuation."""
    if not text:
        return ""
    # remove punctuation, keep alphanumeric and spaces
    cleaned = re.sub(r"[^\w\s]", " ", text.lower())
    # collapse multiple whitespaces
    return " ".join(cleaned.split())


def compute_string_similarity(a: str, b: str) -> float:
    """Compute string similarity using difflib.SequenceMatcher."""
    norm_a = normalize_for_matching(a)
    norm_b = normalize_for_matching(b)
    if not norm_a or not norm_b:
        return 0.0
    # Exact substring match check
    if norm_a in norm_b or norm_b in norm_a:
        shorter = min(len(norm_a), len(norm_b))
        longer = max(len(norm_a), len(norm_b))
        if shorter / longer >= 0.7:
            return max(0.85, difflib.SequenceMatcher(None, norm_a, norm_b).ratio())
    return difflib.SequenceMatcher(None, norm_a, norm_b).ratio()


def calibrate_page_offset(
    candidate_entries: List[Dict[str, Any]],
    docling_items: List[Dict[str, Any]],
    sample_count: int = 5
) -> Optional[int]:
    """
    Page-offset calibration: sample 2-5 bookmark/TOC entries,
    compare their stated page against where Docling placed matching block text,
    and compute a constant offset: offset = actual_page - stated_page.
    """
    offsets = []
    samples = [e for e in candidate_entries if e.get("page") is not None and len(e.get("title", "")) > 5][:sample_count]

    if not samples:
        return 0

    for s in samples:
        stated_page = s["page"]
        title = s["title"]
        # Search blocks within ±10 pages of stated page
        search_window = [
            b for b in docling_items
            if b.get("page") is not None and abs(b["page"] - stated_page) <= 10
        ]

        best_page = None
        best_ratio = 0.0

        for b in search_window:
            ratio = compute_string_similarity(title, b.get("text", ""))
            if ratio > best_ratio and ratio >= 0.75:
                best_ratio = ratio
                best_page = b["page"]

        if best_page is not None:
            offsets.append(best_page - stated_page)

    if not offsets:
        logger.info("Page offset calibration found no clear match; defaulting to offset 0.")
        return 0

    # Most frequent offset
    consensus_offset = max(set(offsets), key=offsets.count)
    logger.info("Calibrated page offset: %d (from sample offsets: %s)", consensus_offset, offsets)
    return consensus_offset
