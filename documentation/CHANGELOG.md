# Changelog

All notable changes to the **PriorAuthRAG** project are documented in this file.
The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/), tracing project evolution from repository inception.

---

## [Unreleased] - 2026-09-24..HEAD

### Added
- **Unified Auto-Documentation System**: Dual-engine documentation generator combining automated project structure scanning, Git commit history logging, and Keep-a-Changelog drafting.
- **Git Post-Commit Hook**: Installed automated post-commit hook (`.git/hooks/post-commit`) to refresh documentation and flag unreviewed diffs.

---

## [0.5.0] - 2026-09-24

### Added
- **Baseline Stabilization & Verification**: Validated complete hierarchical retrieval pipeline prior to refactoring fixes (`882a68c`).
- **GSD Planning Framework**: Ingested project architecture, stack, requirements, conventions, and roadmap in `.planning/`.
- **Knowledge Graph Representation**: Integrated Graphify knowledge graph (`ccb759a`) for entity relationship analysis across clinical guidelines.
- **Radiation Oncology Policy Pipeline**: Added end-to-end ingestion for Cigna Radiation Oncology (`97b0ac3`), including TOC extraction, hierarchical chunking, BM25 indexing, and vector embeddings.

### Changed
- Standardized policy manifest registry under `hierarchical-processing/policies_manifest.json`.

---

## [0.4.0] - 2026-09-22

### Added
- **Knee Policy Pipeline**: Integrated Cigna Knee guideline parsing, TOC generation, chunks, and dual index artifacts (`data/policies/Cigna_Knee/`).
- **Evaluation Reporting Suite**: Benchmark scripts for 30-question medical retrieval accuracy evaluation (`EVALUATION_REPORT_30Q.md`).

### Fixed
- Addressed section hierarchy nesting anomalies in complex multi-level clinical tables.

---

## [0.3.0] - 2026-09-17..2026-09-18

### Added
- **Modular Fallback Parser Engine**: Built `fallback/` pipeline with `extractors.py`, `builder.py`, and `pipeline.py` to process deeply nested PDF structures without OCR timeouts (`de2c621`, `c13c799`).
- **Lab Management Fallback Execution**: Extracted and enriched hierarchical chunks for 400+ page Cigna Clinical Lab Management guidelines (`c13c799`).
- **Enriched Chunks Architecture**: Structured chunk schema with parent metadata, breadcrumb ancestry, and CPT code references.

### Changed
- Migrated away from raw OCR parsing toward direct layout extraction (`docling_pdf_no_ocr.py`) to reduce document parsing runtime by 80%.

---

## [0.2.0] - 2026-09-09..2026-09-15

### Added
- **Lumbar Spinal Fusion Pipeline Complete**: Built complete extraction, TOC tree parsing, and hybrid retrieval indices for Cigna Lumbar Fusion policies (`00b1acc`).
- **Lab Management Document Intake**: Initial extraction and TOC output parsing for Cigna Lab Management PDF (`1079351`).
- **No-OCR Extraction Switch**: Disabled heavy OCR for text-native PDFs (`ddb23b3`) to drastically improve ingestion speed.

### Changed
- Cleaned up obsolete experimental scripts and standardized on hierarchical retrieval architecture.

---

## [0.1.0] - 2026-09-08 (Initial Release)

### Added
- **Repository Inception**: Initialized project baseline (`5d00445`) with core PDF parsers, initial chunking scripts, and embedding generation experiments.
- **Hierarchical Chunking Baseline**: Initial parent-child chunk mapping (`chunking.py`).
- **Lexical BM25 Indexing**: Keyword retrieval index implementation (`bm25_index.py`).
- **Document Registry Architecture**: Initial design specs in `architecture.md`.
