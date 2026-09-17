"""
Pipeline configuration and data contracts.
"""

from dataclasses import dataclass, field
from pathlib import Path
from typing import Optional, List, Dict, Any


@dataclass
class PipelineConfig:
    page_count_threshold: int = 300
    page_search_window: int = 2
    min_match_ratio: float = 0.80
    min_confident_matches_before_fallback: int = 2
    min_headings_per_20_pages: float = 1.0
    enable_ocr: bool = False


@dataclass
class ProcessingResult:
    pdf_path: Path
    output_dir: Path
    pipeline_used: str  # "docling_hierarchical" | "tiered_bookmark_fallback"
    escalated_from_main: bool
    page_count: int
    total_blocks: int
    total_headings: int
    total_tables: int
    heading_source_breakdown: Dict[str, int]
    detected_page_offset: Optional[int]
    unmatched_entries: List[Dict[str, Any]]
    warnings: List[str]
    markdown_path: Path
    json_path: Path
    qa_report_path: Path
