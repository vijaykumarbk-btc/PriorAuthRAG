# Codebase Onboarding Summary

## Executive Overview
The **TOC-Guided Hierarchical Clinical RAG Pipeline** is a specialized, high-precision clinical decision engine designed to verify prior authorization requirements and evaluate medical necessity criteria against complex payer coverage policies (e.g. Cigna ACDF, Lumbar Fusion, Laboratory Management, and Radiation Therapy).

## 4-Stage Core Architecture
1. **Stage 1 (Master CPT Table Lookup)**: Matches surgical CPT codes in `output/table.json`.
2. **Stage 2 (Dynamic Policy & Section Routing)**: Identifies candidate policy documents and section subtrees from `policies_manifest.json` using LLM routing.
3. **Stage 3 (Scoped Hybrid Search)**: RRF combining BM25 keyword scoring and dense vector embeddings, strictly bounded by candidate TOC subtrees and augmented with Sibling Condition Completion.
4. **Stage 4 (Structured Clinical JSON Synthesis)**: Generates validated JSON prior auth determinations with multi-stage syntax repair (`json_repair`) and local Ollama MedGemma fallback.

## Artifact Index & Initialized Setup
- **Codebase Mapping**: `.planning/codebase/` (`STACK.md`, `INTEGRATIONS.md`, `ARCHITECTURE.md`, `STRUCTURE.md`, `CONVENTIONS.md`, `TESTING.md`, `CONCERNS.md`)
- **Project Governance**: `.planning/PROJECT.md`, `.planning/REQUIREMENTS.md`, `.planning/ROADMAP.md`, `.planning/STATE.md`

## Next Steps & Commands
- `/gsd-plan-phase`: Plan the next milestone phase.
- `/gsd-next`: Let GSD auto-detect current project state and suggest the optimal next step.
