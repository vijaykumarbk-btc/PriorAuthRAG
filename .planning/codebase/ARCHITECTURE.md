# Architecture Overview

## 4-Stage TOC-Guided Hierarchical Clinical RAG Pipeline

```
[Clinical Query / CPT Code]
          │
          ▼
┌──────────────────────────────────────────────────────────────┐
│ Stage 1: Master CPT Table Prior Auth Lookup                  │
│ Matches CPT codes in output/table.json -> Yes / No / Add-On  │
└──────────────────────────────┬───────────────────────────────┘
                               │
                               ▼
┌──────────────────────────────────────────────────────────────┐
│ Stage 2: Dynamic TOC Policy & Section Routing                │
│ Routes query to target policy document & specific TOC IDs    │
│ via policies_manifest.json and DocumentRegistry              │
└──────────────────────────────┬───────────────────────────────┘
                               │
                               ▼
┌──────────────────────────────────────────────────────────────┐
│ Stage 3: Scoped Hybrid Retrieval (BM25 + Dense)              │
│ Searches strictly within candidate TOC subtrees with         │
│ automatic Sibling Condition Completion                       │
└──────────────────────────────┬───────────────────────────────┘
                               │
                               ▼
┌──────────────────────────────────────────────────────────────┐
│ Stage 4: Structured Clinical JSON Synthesis                  │
│ Resilient LLM generation with multi-tier JSON repair &       │
│ schema normalization                                         │
└──────────────────────────────────────────────────────────────┘
```

## Core Architectural Modules

1. **Stage 1 — Master CPT Table Lookup** (`hierarchical-processing/cpt_table_lookup.py`):
   - Fast exact/fuzzy matching against `output/table.json`.
   - Resolves surgical concept synonyms and procedure categories.

2. **Stage 2 — Policy & TOC Routing** (`hierarchical-processing/document_registry.py` & `retrieval-hierarchical.py`):
   - Manages multi-document registry (`policies_manifest.json`).
   - Generates compact TOC tree representations for LLM router context.
   - Outputs target policy document key and candidate `toc_ids`.

3. **Stage 3 — Scoped Hybrid Retrieval** (`hybrid_search_hierarchical.py` & `hierarchical-processing/retrieve.py`):
   - `get_descendant_toc_ids()` automatically resolves child nodes within candidate TOC subtrees.
   - Reciprocal Rank Fusion (RRF) combines BM25 keyword scores and dense cosine similarities.
   - Sibling condition completion pulls related clinical diagnostic alternatives (e.g. Radiculopathy + Myelopathy).

4. **Stage 4 — Clinical JSON Synthesis & JSON Repair** (`retrieval-hierarchical.py`):
   - Generates structured prior authorization determination (status, indications, non-indications, exceptions, required documentation).
   - Multi-tier JSON extraction: thinking tag stripping, brace extraction, `json_repair` normalization.
   - Primary cloud Groq LLM with local Ollama MedGemma fallback.

5. **Dense PDF Fallback Pipeline** (`fallback/`):
   - Router selects between Docling (<=300 pages) and tiered outline/bookmark extraction (>300 pages) to handle 900+ page clinical manuals without memory overflow or visual tree loss.
