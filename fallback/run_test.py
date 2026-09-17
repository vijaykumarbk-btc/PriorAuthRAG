import sys
import os
import json
import argparse
from pathlib import Path

# Add project root to sys.path
PROJECT_ROOT = Path(__file__).resolve().parent.parent
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from fallback.config import PipelineConfig
from fallback.pipeline import process_pdf


def main():
    parser = argparse.ArgumentParser(description="Test runner for intelligent PDF processing pipeline.")
    parser.add_argument("pdf_path", type=str, help="Path to the PDF file to test.")
    parser.add_argument("--threshold", type=int, default=300, help="Page count threshold (default 300).")
    parser.add_argument("--out", type=str, default="fallback/output_test", help="Output directory.")
    parser.add_argument("--ocr", action="store_true", help="Enable OCR (default False).")

    args = parser.parse_args()
    pdf_path = Path(args.pdf_path).resolve()
    out_dir = Path(args.out).resolve()

    if not pdf_path.exists():
        print(f"Error: File not found: {pdf_path}")
        sys.exit(1)

    config = PipelineConfig(
        page_count_threshold=args.threshold,
        enable_ocr=args.ocr
    )

    print("\n" + "=" * 70)
    print(f"TESTING PIPELINE ON: {pdf_path.name}")
    print(f"Routing Threshold  : {config.page_count_threshold} pages")
    print("=" * 70)

    result = process_pdf(pdf_path, out_dir, config)

    # Read the generated QA report
    with open(result.qa_report_path, "r", encoding="utf-8") as f:
        qa_data = json.load(f)

    print("\n" + "=" * 70)
    print("QA REPORT SUMMARY")
    print("=" * 70)
    print(f"Pipeline Used          : {result.pipeline_used}")
    print(f"Escalated from Main    : {result.escalated_from_main}")
    print(f"Page Count             : {result.page_count}")
    print(f"Total Blocks           : {result.total_blocks:,}")
    print(f"Total Headings         : {result.total_headings:,}")
    print(f"Total Tables           : {result.total_tables:,}")
    print(f"Heading Breakdown      : {result.heading_source_breakdown}")
    print(f"Detected Page Offset   : {result.detected_page_offset}")
    print(f"Unmatched Entries Count: {len(result.unmatched_entries)}")

    if result.unmatched_entries:
        print("\nSample Unmatched Entries:")
        for u in result.unmatched_entries[:3]:
            print(f"  - '{u.get('title')}' (stated page: {u.get('stated_page')}, best ratio: {u.get('best_ratio')})")

    if result.warnings:
        print("\nWarnings / Sanity Flags:")
        for w in result.warnings:
            print(f"  [!] {w}")
    else:
        print("\nWarnings / Sanity Flags: None (All sanity checks passed!)")

    print("\nOutputs Saved At:")
    print(f"  Markdown : {result.markdown_path}")
    print(f"  JSON     : {result.json_path}")
    print(f"  QA Report: {result.qa_report_path}")
    print("=" * 70 + "\n")


if __name__ == "__main__":
    main()
