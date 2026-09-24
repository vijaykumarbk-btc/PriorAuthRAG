# Project: TOC-Guided Hierarchical Clinical RAG Pipeline

## Vision & Objective
A high-precision, multi-document **Hierarchical Retrieval-Augmented Generation (RAG)** pipeline designed for medical necessity determination, clinical prior authorization verification, and coverage criteria synthesis from complex payer policies (e.g., Cigna / EviCore clinical guidelines).

## Key Architecture & Components
1. **Stage 1: Master CPT Table Lookup** (`cpt_table_lookup.py`) - Quick resolution of prior authorization requirements and procedure CPT codes.
2. **Stage 2: TOC-Guided Policy & Section Routing** (`document_registry.py` & `retrieval-hierarchical.py`) - Multi-document routing to target policy keys and section nodes.
3. **Stage 3: Scoped Hybrid Search with Sibling Condition Completion** (`hybrid_search_hierarchical.py`) - Candidate search bounded by TOC subtrees with reciprocal rank fusion (BM25 + Dense).
4. **Stage 4: Resilient Structured Clinical JSON Synthesis** - Fail-safe LLM prompt execution with multi-tier JSON repair (`json_repair`).
5. **Dense PDF Ingestion Fallback Pipeline** (`fallback/`) - Dual-strategy parsing for documents up to 900+ pages.

## Project Structure
- Core Pipeline: `retrieval-hierarchical.py`, `hybrid_search_hierarchical.py`, `hierarchical-processing/`
- Fallback Engine: `fallback/`
- Benchmarks: `eval_lab_management_benchmark.py`
- Codebase Planning Artifacts: `.planning/codebase/`
