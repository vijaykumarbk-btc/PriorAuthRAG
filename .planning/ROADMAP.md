# Project Roadmap & Milestones

## Completed Milestones
- **Milestone 1: 4-Stage Hierarchical RAG Core Architecture**
  - Implement Stage 1 CPT Master Table lookup engine (`cpt_table_lookup.py`).
  - Implement Stage 2 Dynamic TOC Router & Document Registry (`document_registry.py`).
  - Implement Stage 3 Scoped Hybrid Retrieval with Sibling Condition Completion (`hybrid_search_hierarchical.py`).
  - Implement Stage 4 Clinical JSON Synthesis with multi-tier JSON repair (`retrieval-hierarchical.py`).
- **Milestone 2: Dense PDF Fallback Ingestion Pipeline**
  - Dual-strategy router for large (>300 page) policy manuals (`fallback/`).
  - Successfully ingested Cigna Laboratory Management policy (910 pages).
- **Milestone 3: Evaluation Benchmark Infrastructure**
  - 20-query evaluation suite (`eval_lab_management_benchmark.py`).

## Active & Upcoming Milestones
- **Milestone 4: Codebase Onboarding & Standardized GSD Planning Setup**
  - Phase 1: Codebase Mapping (`.planning/codebase/` STACK, ARCHITECTURE, STRUCTURE, etc.).
  - Phase 2: Project Setup (`PROJECT.md`, `REQUIREMENTS.md`, `ROADMAP.md`, `STATE.md`).
  - Phase 3: Automated Policy Ingestion CLI Tooling.
