"""
Fallback PDF processing package.
Provides intelligent page-count routing, tiered bookmark/TOC extraction,
and shared JSON/Markdown output contracts.
"""

from fallback.config import PipelineConfig, ProcessingResult
from fallback.pipeline import process_pdf

__all__ = ["PipelineConfig", "ProcessingResult", "process_pdf"]
