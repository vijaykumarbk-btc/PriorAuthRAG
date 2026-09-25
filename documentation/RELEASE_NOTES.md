# PriorAuthRAG Release Notes

Summary of major releases and milestones across the project lifecycle.

---

## Version 1.0.0 (Pre-release Baseline) - 2026-09-24

This release marks the functional completion of the **Prior Authorization Hierarchical Retrieval-Augmented Generation (RAG)** system for clinical insurance policies.

### Highlights
- **Multi-Policy Clinical Coverage**: Full automated ingestion pipelines for **Cigna Lumbar Fusion**, **Lab Management**, **Radiation Oncology**, and **Knee** clinical policies.
- **Hierarchical Document Chunking**: Clinical guidelines are parsed into multi-tiered chunks preserving heading ancestry, clause hierarchies, and tabular CPT code requirements.
- **Hybrid Retrieval Architecture**: Combines BM25 lexical keyword matching with dense vector embeddings (using Reciprocal Rank Fusion / linear interpolation) to pinpoint medical necessity criteria.
- **Fallback Non-OCR Parser**: Direct PDF layout extractor capable of processing 400+ page clinical guideline documents without OCR bottlenecks.
- **Automated Documentation Suite**: Full dual-engine auto-documentation tracking project structure and complete Git evolution from day one.

---

## Version 0.5.0 - 2026-09-22

- Added Cigna Radiation Oncology guideline processing.
- Integrated Knowledge Graph generation via Graphify.
- Completed 30-question retrieval benchmark evaluation and validation.

---

## Version 0.3.0 - 2026-09-18

- Implemented modular `fallback/` parser pipeline to resolve table parsing timeouts on large medical documents.
- Generated enriched chunks and embeddings for Cigna Clinical Lab Management.

---

## Version 0.1.0 - 2026-09-08

- Initial project setup with PDF parsing, basic chunking, and BM25 indexing.
