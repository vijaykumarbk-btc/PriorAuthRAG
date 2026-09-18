# Project Context & Conversation History Representation
*Comprehensive handoff and state representation for incoming LLMs and agents.*
*Timestamp: 2026-09-17*

---

## 1. Executive Summary & Purpose

This repository (`project2`) contains a production-grade **Medical Coverage Policy Hierarchical Retrieval-Augmented Generation (RAG) System**. Its primary objective is to evaluate clinical queries against private payer coverage guidelines (primarily **Cigna / EviCore** policies) to determine:
1. **Prior Authorization (PA) Requirement**: Whether a procedure/CPT code requires prior authorization (`Yes` or `No`).
2. **Policy Identification & Section Routing**: Which clinical guideline and specific sub-section applies (e.g. Lumbar Fusion vs ACDF vs Lab Management vs Knee Replacement).
3. **Criteria Retrieval**: Exact medical necessity criteria, indications, exclusions, contraindications, and required conservative therapies.
4. **Structured Clinical Synthesis**: Validated, machine-readable clinical decision JSON conforming to a strict healthcare payer schema.

The system handles both short surgical policies (30–60 pages) and massive, complex guideline manuals (e.g. 910-page Laboratory Management Guidelines).

---

## 2. Core Architecture & Pipeline Stages

The inference query pipeline is driven by [`retrieval-hierarchical.py`](file:///home/vijaykumar/Desktop/project2/retrieval-hierarchical.py), executing four sequential stages:

```
                      [User Clinical Query]
                                │
                                ▼
         ┌─────────────────────────────────────────────┐
         │  Stage 1: Master CPT Prior Auth Table LookUp │
         │  (cpt_table_lookup.py / merged_output.json)  │
         └──────────────────────┬──────────────────────┘
                                │ PA Required (Yes/No) + Matched CPTs
                                ▼
         ┌─────────────────────────────────────────────┐
         │  Stage 2: TOC-Level Policy & Section Router │
         │  (document_registry.py + Groq LLM)          │
         └──────────────────────┬──────────────────────┘
                                │ Target Policy (doc_key) + Target TOC IDs (S-IDs)
                                ▼
         ┌─────────────────────────────────────────────┐
         │  Stage 3: Scoped Hybrid Search (BM25+Dense) │
         │  (hybrid_search_hierarchical.py)            │
         └──────────────────────┬──────────────────────┘
                                │ Scoped & Condition-Completed Criteria Chunks
                                ▼
         ┌─────────────────────────────────────────────┐
         │  Stage 4: Structured Clinical JSON Synthesis│
         │  (Groq LLM / qwen/qwen3.6-27b)              │
         └──────────────────────┬──────────────────────┘
                                │
                                ▼
               [Saved Structured Clinical Report]
              (data/results_new/<timestamp>_*.json)
```

### Stage 1: Master CPT Table Lookup (`hierarchical-processing/cpt_table_lookup.py`)
- Matches procedure names, keywords, and 5-character CPT codes against the master coverage dataset (`merged_output.json`).
- Determines initial Prior Authorization status (`Yes` or `No`), matched CPT codes, and procedure descriptions.

### Stage 2: Dynamic Policy & TOC Routing (`hierarchical-processing/document_registry.py`)
- Discovers registered policies from [`policies_manifest.json`](file:///home/vijaykumar/Desktop/project2/hierarchical-processing/policies_manifest.json).
- Inspects the full hierarchical Table of Contents (TOC tree) with assigned section identifiers (e.g., `S1`, `S3.7`, `S609.4`).
- Prompts Groq (`qwen/qwen3.6-27b`) to choose the exact policy `doc_key` and specific `target_section_ids`.

### Stage 3: Scoped Hybrid Retrieval (`hybrid_search_hierarchical.py`)
- Restricts vector and lexical search strictly to the routed TOC subtree and its child/sibling nodes.
- Combines:
  - **Dense Search**: 768-dim embeddings generated via EmbeddingGemma hosted on a local Ollama server.
  - **Lexical Search**: Rank-BM25 index built over section titles and body text.
- **Condition Completion**: Resolves multi-criteria rules by pulling adjacent sibling chunks so boolean logic (`ALL of the following`, `ANY of the following`) is preserved.

### Stage 4: Structured Clinical JSON Synthesis
- Groq LLM parses retrieved chunks and formats the clinical report conforming to:
  ```json
  {
    "Prior auth required": "Yes" | "No",
    "Policy Name": "...",
    "Medical necessity indications": [...],
    "Referred Sections": [...],
    "Important criteria & exceptions": [...],
    "Non-Indications": [...],
    "Documentation required": [...]
  }
  ```

---

## 3. Environment & Hardware Configuration

- **Virtual Environment**: `./venv/bin/python` (Python 3.12, Linux).
- **LLM Provider**: Groq API using `qwen/qwen3.6-27b` (set in `.env` as `GEN_MODEL`).
- **Dense Embeddings Provider**:
  - Ollama OpenAI-compatible endpoint: `http://192.168.0.33:11434/v1`
  - Model: `hf.co/unsloth/embeddinggemma-300m-GGUF:Q8_0` (768 dimensions)
- **Token Limits**: Output token generation capped at 5,000–6,000 tokens to avoid truncation while preventing token explosion.

---

## 4. Chronological Evolution of the Project (Turns 1 to ~106)

### Phase 1: Inception, Schema Standardization & ACDF Foundation (Turns 1–40)
1. **Initial Project State**:
   - The user started with a basic RAG setup on `Cigna_ACDF.pdf` (Anterior Cervical Discectomy and Fusion) and planning document `next_step.md`.
   - The initial target was to replace unstructured chunking with hierarchical parsing that preserves document outline, headings, and clinical tables.
2. **Schema & JSON Formatting**:
   - The user provided a reference JSON format for prior authorization reports.
   - Pipeline stages were separated to ensure high-fidelity JSON generation without hallucinations.
3. **Early Obstacles & Fixes**:
   - **Corrupted Git Index**: `.git/index: index file smaller than expected` occurred. Resolved by deleting `.git/index` and running `git reset`.
   - **Groq Rate Limits & Token Blowups**: Output tokens initially spiked to >5k. Tuned generation parameters and scoped chunk retrieval to prevent prompt overload.
   - **Hardcoding Anti-Patterns**: Early scripts had hardcoded paths to ACDF. The user strictly mandated removing all hardcoded paths to prepare the codebase for multi-document scaling.

### Phase 2: Lumbar Fusion Parity & Dynamic Document Registry (Turns 41–73)
1. **Adding Lumbar Fusion**:
   - The user introduced `Cigna_Lumbar_Fusion.pdf` (50 pages).
   - Executed the 7-step pipeline on Lumbar Fusion:
     1. Docling conversion (`docling_pdf.py`).
     2. TOC extraction (`toc_v2.py`).
     3. Chunking (`chunking_heirarchical.py`).
     4. Chunk-TOC mapping (`chunk_toc_mapper.py`).
     5. Dense vector embeddings (`embedding_with_section.py`).
     6. BM25 indexing (`build_bm25.py`).
     7. Manifest registration (`policies_manifest.json`).
2. **Dynamic Multi-Document Architecture**:
   - Introduced [`document_registry.py`](file:///home/vijaykumar/Desktop/project2/hierarchical-processing/document_registry.py) to replace static file references.
   - `policies_manifest.json` was created as the single source of truth for all available policy assets.
3. **Accuracy & Benchmarking**:
   - User ran 10 clinical test queries across ACDF and Lumbar Fusion.
   - Evaluated accuracy, investigated missing indication chunks, and explored the RAGAS evaluation framework.
   - Documented architecture in `architecture.md` and tracked improvements in `issues.md`.

### Phase 3: The 910-Page Lab Management Challenge & The Tiered Router (Turns 74–105)
1. **The 910-Page Bottleneck**:
   - The user brought `Cigna_Lab_Management.pdf`, a massive 910-page clinical laboratory guidelines document.
   - Attempting to run standard Docling with OCR on CPU resulted in near-infinite runtimes (>3-4 hours or hanging).
   - The user asked repeatedly about progress ("how many minutes remaining", "why is it taking so long").
2. **Root Cause Analysis**:
   - Profiling showed that running full deep-learning table layout models and OCR across 910 pages on CPU was completely intractable.
   - The document already had embedded digital text and existing PDF bookmark structures.
3. **Engineering the Tiered Fallback Router (`fallback/pipeline.py`)**:
   - Built a tiered router:
     - **Page Count Routing**: Cheaply inspects page count via `pypdf`. Documents $\le 300$ pages run Docling; documents $> 300$ pages route to the fast Tiered Bookmark Fallback.
     - **Tier 1 (PDF Bookmarks)**: Extracts native PDF outline bookmarks.
     - **Tier 2 (Regex TOC)**: Scans early pages for Table of Contents patterns if bookmarks are absent.
     - **Page Offset Calibration**: Aligns physical PDF page numbers with printed document page numbers.
     - **Sanity Check & Escalation**: On smaller documents, if Docling produces suspiciously low heading density, the router automatically escalates to bookmark fallback.
   - **Result**: The 910-page `Cigna_Lab_Management.pdf` was parsed into clean hierarchical markdown and JSON in **under 2 minutes** instead of hours.
4. **Complexity Optimization**:
   - User noted an $O(n^2)$ block matching algorithm in postprocessing and requested optimizing it to $O(n)$, which was verified and integrated.

---

## 5. Summary of the Last 10 Chats (Leading to Current State)

| Step / Turn | User Request / Focus | Actions Taken & Outcomes |
| :--- | :--- | :--- |
| **Turn 106–108** | Ingestion of 910-page Lab Management (`EXECUTION-STEPS.md`). | Executed Steps 2 through 7 on `Cigna_Lab_Management`. Created TOC (`80+` major guideline sections), 1,778 chunks, mapped chunks, generated 1,778 dense embeddings via Ollama, built BM25 index, registered `Cigna_Lab_Management` in manifest. |
| **Turn 109–110** | **20-Question Harsh Benchmark Evaluation** (13 Prior Auth YES, 7 Prior Auth NO). | Built `eval_lab_management_benchmark.py`. Scored all 4 stages objectively:<br>• **Stage 1 (CPT Lookup)**: **100.0%** (20/20)<br>• **Stage 2 (TOC Routing)**: **80.0%** (16/20)<br>• **Stage 3 (Scoped Retrieval)**: **95.0%** (19/20)<br>• **Stage 4 (Synthesis)**: **90.0%** (18/20)<br>• **End-to-End Strict Accuracy**: **70.0%** (84.6% on YES queries).<br>Results saved to `data/benchmark_results_lab_management_20q.json`. |
| **Turn 111** | Inquiry into code changes in `retrieval-hierarchical.py` and `hybrid_search_hierarchical.py`. | Explained bug fixes made during the benchmark: scoped sibling condition completion to `allowed_ids` to prevent pulling unrelated test guidelines in a 910-page manual, and eliminated duplicate candidate pre-scoring. |
| **Turn 112** | Run verification for ACDF. | Ran `retrieval-hierarchical.py` on cervical radiculopathy. Completed in 14 seconds, confirming zero regression on ACDF. |
| **Turn 113** | User noted manual path inputs across 7 steps. | Acknowledged that policy ingestion was still manual and proposed a single-command automated tool. |
| **Turn 114** | Request for comprehensive root `README.md`. | Authored comprehensive `README.md` documenting architecture, components, evaluation results, and step-by-step guides. |
| **Turn 115** | Pre-approval requirement for automated ingestion tool. | Presented detailed architecture of `ingest_policy.py`, guaranteeing **zero modifications to existing code**. User's system approved the plan. |
| **Turn 116** | Implementation and live testing of `ingest_policy.py`. | Created `ingest_policy.py`. Tested end-to-end on `extra_pdfs/Cigna_Knee.pdf` (34 pages): parsed with Docling, extracted 80 TOC nodes, created 207 chunks, generated embeddings, built BM25 index, and updated manifest. Verified live retrieval query for knee arthroplasty. |

---

## 6. Current Codebase File Inventory & Roles

```
project2/
├── ingest_policy.py                 # [NEW] Single-command ingestion orchestrator (Steps 1-7)
├── retrieval-hierarchical.py        # Main 4-stage query retrieval & clinical synthesis engine
├── hybrid_search_hierarchical.py    # Reciprocal Rank Fusion (BM25 + Ollama dense) with scoped filtering
├── eval_lab_management_benchmark.py # 20-query automated benchmark test harness
├── README.md                        # Master architectural and operational documentation
├── EXECUTION-STEPS.md               # Step-by-step reference guide for manual & automated ingestion
├── policies_manifest.json           # Backup manifest in project root
│
├── fallback/                        # Fast Tiered PDF Ingestion Engine
│   ├── pipeline.py                  # Main router (process_pdf): Page count check, Docling, Tiered fallback
│   ├── config.py                    # PipelineConfig, ProcessingResult data models
│   ├── extractors.py                # pypdf bookmarks, regex TOC extractors, offset calibration
│   └── builder.py                   # Normalized block builder, markdown generator, QA reports
│
├── hierarchical-processing/         # Core Processing Modules & Registered Indices
│   ├── policies_manifest.json       # Master registration manifest for all active policies
│   ├── document_registry.py         # Dynamic policy discovery and path resolver
│   ├── cpt_table_lookup.py          # Stage 1 CPT Master table lookup engine
│   ├── toc_v2.py                    # Stage 2 Table of Contents tree extractor (assigns S-IDs)
│   ├── chunking_heirarchical.py     # Stage 3 Criteria-aware markdown chunker
│   ├── chunk_toc_mapper.py          # Stage 4 Block-ID & path joiner (stamps chunks with toc_ids)
│   ├── embedding_with_section.py    # Stage 5 Dense embeddings via Ollama EmbeddingGemma
│   ├── build_bm25.py                # Stage 6 Section-aware Rank-BM25 builder
│   └── ACDF_toc_output_new.json     # ACDF Table of Contents data
│
├── data/
│   ├── policies/                    # Standardized storage for newly ingested policies
│   │   └── Cigna_Knee/              # Complete knee policy assets (raw, output, toc, chunks, embeddings, bm25)
│   ├── benchmark_results_*.json     # Benchmark evaluation results
│   └── results_new/                 # Output timestamped structured clinical JSON reports
│
├── Lab_Management/                  # Dedicated assets for 910-page Cigna Lab Management
│   ├── raw/                         # Source PDF
│   ├── output_tiered/               # Hierarchical markdown, JSON, QA report
│   ├── TOC/                         # Lab Management TOC output JSON & text tree
│   ├── chunks/                      # Semantic chunks & TOC-enriched chunks
│   ├── embeddings/                  # Dense embedding vectors & metadata JSON
│   └── bm25/                        # BM25 pickle index
│
├── Lumbar/                          # Dedicated assets for Cigna Lumbar Fusion
└── extra_pdfs/                      # Unprocessed or extra carrier PDFs (Radiation Oncology, etc.)
```

---

## 7. Active Registered Policies in Manifest

| `doc_key` | Display Name | Source PDF | Page Count | Storage Location |
| :--- | :--- | :--- | :--- | :--- |
| `Cigna_ACDF` | Cigna ACDF (CMM-601) | `Cigna_ACDF.pdf` | 33 | `hierarchical-processing/` |
| `Cigna_Lumbar_Fusion` | Cigna Lumbar Fusion (CMM-609) | `Cigna_Lumbar_Fusion.pdf` | 50 | `Lumbar/` |
| `Cigna_Lab_Management` | Cigna Laboratory Management | `Cigna_Lab_Management.pdf` | 910 | `Lab_Management/` |
| `Cigna_Knee` | Cigna Knee Surgery (CMM-312) | `Cigna_Knee.pdf` | 34 | `data/policies/Cigna_Knee/` |

---

## 8. Critical Directives & Guidelines for Incoming LLMs/Agents

1. **User Rule on Code Modifications**:
   - **STRICT MANDATE**: *"dont make changes to the codes other than paths without my permission"*.
   - Never overwrite or refactor existing core scripts (`pipeline.py`, `retrieval-hierarchical.py`, `chunking_heirarchical.py`, etc.) without explaining the exact changes and obtaining the user's manual consent first.
2. **Never Hardcode Policy Keys or Paths**:
   - Do not write code that assumes only ACDF or Lumbar Fusion exist. All documents must be discovered dynamically via [`document_registry.py`](file:///home/vijaykumar/Desktop/project2/hierarchical-processing/document_registry.py) and [`policies_manifest.json`](file:///home/vijaykumar/Desktop/project2/hierarchical-processing/policies_manifest.json).
3. **Ingestion Workflow**:
   - To ingest any new PDF from scratch, use the single automated CLI tool:
     ```bash
     ./venv/bin/python ingest_policy.py <path_to_pdf> --name "<display_name>"
     ```
4. **Execution Python Binary**:
   - Always run with the project's virtualenv: `./venv/bin/python`.
5. **Local Services**:
   - Ollama must remain running at `http://192.168.0.33:11434/v1` for dense embeddings.
   - Groq API credentials in `.env` must remain active for query routing and clinical synthesis.

