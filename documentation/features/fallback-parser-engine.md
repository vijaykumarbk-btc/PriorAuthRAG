# Fallback Non-OCR Parser Engine

The `fallback/` pipeline is a specialized extraction engine created to solve processing timeouts and layout corruption on large, complex tabular PDF guidelines (such as the 400+ page Clinical Lab Management guideline).

## Problem Addressed
Standard document parsers relying on full OCR frequently freeze or time out when encountering complex multi-page tables, nested CPT code matrices, and dense clinical eligibility checklists. Furthermore, OCR engines often flatten indented criteria trees.

## Architecture

The fallback engine uses a modular architecture:
- [`fallback/extractors.py`](../../fallback/extractors.py): Direct layout-aware text and tabular extractor operating without OCR. Extracts bounding box hierarchies, text flow, and cell alignments directly from native PDF streams.
- [`fallback/builder.py`](../../fallback/builder.py): Reconstructs hierarchical markdown and structured JSON trees from the raw text blocks.
- [`fallback/pipeline.py`](../../fallback/pipeline.py): End-to-end execution coordinator managing parsing, TOC detection, QA validation, and fallback triggers.
- [`fallback/config.py`](../../fallback/config.py): Parser parameters, heading patterns, and table thresholds.

## Usage

```bash
# Run the fallback pipeline on a specific guideline PDF
python fallback/run_test.py
```
