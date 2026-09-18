# TOC-Guided Hierarchical Clinical RAG Pipeline

A high-precision, multi-document **Hierarchical Retrieval-Augmented Generation (RAG)** pipeline designed for medical necessity determination, clinical prior authorization verification, and coverage criteria synthesis from complex payer policies (e.g., Cigna / EviCore clinical guidelines).

---

## Architecture Overview

Traditional RAG fails on dense clinical policies due to ambiguous heading hierarchies, loss of nested conditional criteria (*"ALL of the following"*, *"ANY of the following"*), and retrieval dilution over large manuals.

This pipeline solves these challenges using a 4-stage hierarchical retrieval architecture guided by an authoritative **Table of Contents (TOC) tree**:

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
│ Stage 2: TOC-Guided Policy & Section Routing                 │
│ Routes query to target policy document & specific TOC IDs    │
│ (e.g., Cigna_ACDF [S9.1] or Cigna_Lab_Management [S3.7])      │
└──────────────────────────────┬───────────────────────────────┘
                               │
                               ▼
┌──────────────────────────────────────────────────────────────┐
│ Stage 3: Scoped Hybrid Retrieval (BM25 + Dense)              │
│ Searches strictly within candidate TOC sections with         │
│ automatic sibling condition completion (Radiculopathy +     │
│ Myelopathy)                                                  │
└──────────────────────────────┬───────────────────────────────┘
                               │
                               ▼
┌──────────────────────────────────────────────────────────────┐
│ Stage 4: Structured Clinical JSON Synthesis                  │
│ Outputs standardized prior auth status, indications,         │
│ non-indications, exceptions, and required documentation     │
└──────────────────────────────────────────────────────────────┘
```

---

## Key Features

- **Document-Adaptive Ingestion**:
  - **Standard Documents (<= 300 pages)**: Uses Docling + `docling-hierarchical-pdf` to recover visual heading trees.
  - **Dense Manuals (> 300 pages, e.g. 910-page Lab Management)**: Routes to a tiered bookmark/outline extractor with visual TOC regex and page-offset calibration.
- **Authoritative TOC Tree**: Extracts hierarchical section nodes (`S1`, `S2`, `S2.1`, `S3.7.1`) and stamps each chunk with its exact `toc_id`.
- **Hybrid Scoped Search**: Combines EmbeddingGemma dense vectors (768-dim) and Rank-BM25 keyword scoring, strictly bounded to candidate TOC subtrees.
- **Sibling Condition Completion**: Ensures that when one diagnostic indication is retrieved (e.g., *Radiculopathy*), its clinical sibling alternatives (e.g., *Myelopathy*) are pulled together so the LLM sees complete coverage logic.
- **Multi-Document Registry**: Dynamically routes across multiple registered policies (`Cigna_ACDF`, `Cigna_Lumbar_Fusion`, `Cigna_Lab_Management`) without hardcoded string matching.

---

## Directory Structure

```plaintext
project2/
├── README.md                                # Project documentation
├── requirements.txt                         # Python dependencies
├── .env                                     # Environment variables (LLM & Ollama config)
│
├── output/
│   └── table.json                           # Master CPT / HCPCS Prior Authorization Table
│
├── hierarchical-processing/                 # Core processing scripts
│   ├── policies_manifest.json               # Active policy registry manifest
│   ├── document_registry.py                 # Multi-policy dynamic loader & TOC preview
│   ├── cpt_table_lookup.py                  # Stage 1: CPT table prior auth lookup engine
│   ├── toc_v2.py                            # Stage 2: TOC tree generator from JSON blocks
│   ├── chunking_heirarchical.py             # Stage 3: Criteria-aware Markdown chunker
│   ├── chunk_toc_mapper.py                  # Stage 4: Stamps chunks with TOC section IDs
│   ├── embedding_with_section.py            # Stage 5: EmbeddingGemma contextual vector generator
│   └── build_bm25.py                        # Stage 6: Section-aware Rank-BM25 builder
│
├── hybrid_search_hierarchical.py            # Scoped hybrid search & sibling completion
├── retrieval-hierarchical.py                # Main end-to-end multi-document RAG pipeline
├── eval_lab_management_benchmark.py         # 20-query evaluation benchmark runner
│
├── fallback/                                # Tiered pipeline for large/dense PDFs (>300 pages)
│   ├── pipeline.py                          # Dual-strategy router & fallback orchestrator
│   ├── extractors.py                        # PDF outline, bookmark, and regex extractors
│   ├── builder.py                           # Block normalizer & QA report builder
│   └── config.py                            # Thresholds and configuration dataclasses
│
├── Lab_Management/                          # Cigna Laboratory Management policy (910 pages)
│   ├── raw/                                 # Raw PDF
│   ├── output_tiered/                       # Standardized .hierarchical.md and .json
│   ├── TOC/                                 # TOC JSON tree and text outline
│   ├── chunks/                              # Semantic chunks and TOC-mapped enriched chunks
│   ├── embeddings/                          # lab_management_embeddings.npy and metadata
│   └── bm25/                                # lab_management_bm25.pkl
│
├── Lumbar/                                  # Cigna Lumbar Fusion policy
│   ├── TOC/                                 # Lumbar TOC output
│   ├── chunks/                              # Lumbar chunks
│   ├── embeddings/                          # Dense embeddings & metadata
│   └── bm25/                                # BM25 index
│
└── data/
    ├── results_new/                         # Saved clinical JSON reports from queries
    └── benchmark_results_lab_management_20q.json # Evaluation benchmark results
```

---

## Installation & Setup

### 1. Prerequisites
- Linux OS (Ubuntu 20.04+ recommended)
- Python 3.11 or 3.12
- Local Ollama server (or cloud LLM endpoints)

### 2. Environment Setup
```bash
# Clone the repository
git clone <repo-url>
cd project2

# Create and activate virtual environment
python3 -m venv venv
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt
```

### 3. Environment Variables (`.env`)
Create a `.env` file in the project root:
```ini
# Embedding server (Ollama)
OLLAMA_HOST=http://localhost:11434/v1
MODEL=hf.co/unsloth/embeddinggemma-300m-GGUF:Q8_0

# LLM Generation (Groq API or local Ollama)
GROQ_API_KEY=your_groq_api_key_here
GEN_MODEL=llama-3.3-70b-versatile
CHAT_MODEL=qwen3:14b
```

---

## End-to-End Execution Guide

Bringing any new medical policy PDF into the pipeline involves 7 steps:

```
[Raw PDF]
   │
   ▼  Step 1: Parse PDF
[Normalized JSON + Markdown]
   │
   ├─────────────────────────────────────────┐
   ▼  Step 2: Extract TOC                    ▼  Step 3: Chunk Markdown
[TOC JSON & Text Tree]                     [Raw Semantic Chunks]
   │                                         │
   └────────────────────┬────────────────────┘
                        ▼  Step 4: Map Chunks to TOC
                  [Enriched Chunks JSON]
                        │
                        ▼  Step 5: Generate Dense Embeddings
                  [Dense Matrix (.npy) + Metadata (.json)]
                        │
                        ▼  Step 6: Build BM25 Index
                  [BM25 Lexical Index (.pkl)]
                        │
                        ▼  Step 7: Register in Manifest
                  [Ready for Multi-Document Retrieval]
```

### Step 1: Parse PDF
- **For standard PDFs (<= 300 pages)**:
  ```bash
  ./venv/bin/python docling/docling_pdf.py
  ```
- **For large/dense manuals (> 300 pages)**:
  ```bash
  ./venv/bin/python -c "
  from pathlib import Path
  from fallback.config import PipelineConfig
  from fallback.pipeline import process_document
  process_document(Path('path/to/policy.pdf'), Path('output_folder/'), PipelineConfig())
  "
  ```

### Step 2: Extract the Table of Contents (TOC) Tree
```bash
./venv/bin/python hierarchical-processing/toc_v2.py \
    path/to/policy.hierarchical.json \
    path/to/policy_toc_output.json \
    path/to/policy_toc_tree.txt
```

### Step 3: Chunk the Markdown Document
```bash
CHUNKING_INPUT_DIR="path/to/markdown_dir/" \
CHUNKING_OUTPUT_DIR="path/to/chunks_dir/" \
./venv/bin/python hierarchical-processing/chunking_heirarchical.py
```

### Step 4: Map Chunks to TOC Tree
```bash
./venv/bin/python hierarchical-processing/chunk_toc_mapper.py \
    path/to/chunks.json \
    path/to/policy_toc_output.json \
    path/to/enriched_chunks.json
```

### Step 5: Generate Dense Embeddings
```bash
./venv/bin/python hierarchical-processing/embedding_with_section.py \
    path/to/enriched_chunks.json \
    path/to/embeddings.npy \
    path/to/metadata.json
```

### Step 6: Build the BM25 Lexical Index
```bash
./venv/bin/python hierarchical-processing/build_bm25.py \
    path/to/metadata.json \
    path/to/bm25.pkl
```

### Step 7: Register in `policies_manifest.json`
Add an entry in `hierarchical-processing/policies_manifest.json`:
```json
{
  "doc_key": "Cigna_MyPolicy",
  "display_name": "Cigna Policy Display Name",
  "toc_file": "../MyPolicy/TOC/MyPolicy_toc_output.json",
  "metadata_file": "../MyPolicy/embeddings/mypolicy_metadata.json",
  "embeddings_file": "../MyPolicy/embeddings/mypolicy_embeddings.npy",
  "bm25_file": "../MyPolicy/bm25/mypolicy_bm25.pkl"
}
```

---

## Running Queries

Run queries directly against all registered policies:

```bash
./venv/bin/python retrieval-hierarchical.py "When is anterior cervical discectomy and fusion (ACDF) considered medically necessary for cervical radiculopathy?"
```

```bash
./venv/bin/python retrieval-hierarchical.py "What are the clinical criteria for BRCA1 and BRCA2 full sequence analysis 81162?"
```

```bash
./venv/bin/python retrieval-hierarchical.py "Does routine Complete Blood Count CBC 85025 require prior authorization?"
```

Outputs are printed to the console and automatically saved as structured JSON reports under `data/results_new/`.

---

## Sample JSON Output Schema

```json
{
  "Prior auth required": "Yes",
  "Policy Name": "Cigna ACDF (CMM-601: Anterior Cervical Discectomy and Fusion)",
  "Referred Sections": [
    "CMM-601.4: Initial Primary Anterior Cervical Discectomy and Fusion (ACDF)",
    "Radiculopathy",
    "Myelopathy"
  ],
  "Medical necessity indications": [
    {
      "Guideline Category": "Radiculopathy",
      "Required findings": [
        "Clinically significant daily pain causing functional impairment and unremitting radicular pain to shoulder/arm",
        "Objective exam: dermatomal sensory loss, motor weakness (biceps/triceps), reflex changes, or Spurling's maneuver",
        "MRI/CT showing nerve root compression correlating with clinical findings",
        "Failure of at least 6 weeks of conservative therapy (medications, physical therapy, injections)",
        "Absence of unmanaged behavioral health disorders and documented nicotine-free status (>= 6 weeks)"
      ],
      "Source": "Initial Primary ACDF > Radiculopathy"
    }
  ],
  "Non-Indications": [
    "Absence of objective neurological exam deficit",
    "Incomplete conservative therapy duration (< 6 weeks)",
    "Active unmanaged substance use or psychiatric disorders"
  ],
  "Important criteria & exceptions": [
    "Emergency decompression exceptions for progressive myelopathy or cauda equina syndrome"
  ],
  "Documentation required": [
    "Progress notes documenting 6-week conservative trial",
    "Official MRI or CT radiology report",
    "Objective cotinine test report if smoking history exists"
  ]
}
```

---

## Evaluation & Benchmarks

The project includes an automated 20-query evaluation benchmark (`eval_lab_management_benchmark.py`) testing **13 Prior Auth YES** and **7 Prior Auth NO** questions across all 4 stages:

```bash
./venv/bin/python eval_lab_management_benchmark.py
```

### Benchmark Summary (910-page Cigna Lab Management)

| Stage | Accuracy | Description |
| :--- | :---: | :--- |
| **Stage 1 (CPT Prior Auth Lookup)** | **100.0%** | Exact match on 13 molecular CPTs and 7 routine non-PA lab panels |
| **Stage 2 (TOC Section Routing)** | **80.0%** | 100% on YES queries (exact subsection mapping); administrative matching on NO queries |
| **Stage 3 (Scoped Hybrid Retrieval)** | **95.0%** | Bounded scoped retrieval with high section purity |
| **Stage 4 (Clinical JSON Synthesis)** | **90.0%** | High fidelity clinical indications and criteria extraction |
| **Overall End-to-End Strict Pass** | **70.0%** | All 4 stages passing simultaneously (84.6% on YES sub-group) |

Raw results and timings are preserved in `data/benchmark_results_lab_management_20q.json`.

