# Integrations & External Interfaces

## Cloud LLM Services
- **Groq API**:
  - Environment key: `GROQ_API_KEY`
  - Models used: `llama-3.1-8b-instant`, `groq/compound-mini`, `openai/gpt-oss-120b`
  - Purpose: Stage 2 TOC section routing & Stage 4 clinical JSON determination synthesis.

## Local Services
- **Ollama Engine**:
  - Environment key / Base URL: `OLLAMA_BASE_URL` (default `http://localhost:11434`)
  - Model: `medgemma-1.5-4b-it-GGUF:Q8_0`
  - Role: Offline/local fallback for clinical JSON synthesis when cloud APIs are unconfigured or fail.

## Embedding Models
- **EmbeddingGemma / BGE**:
  - Vector Dimension: 768-dim dense embeddings.
  - Role: Dense vector representation for policy chunk retrieval.

## Document Processing Libraries
- **Docling API / Parser**:
  - Input: Medical policy PDFs (e.g. Cigna ACDF, Cigna Lumbar Fusion).
  - Output: Structured visual heading tree and Markdown blocks.
- **Tiered PDF Outline Extractor (`fallback/`)**:
  - Strategy: Regex-based visual TOC matching + PyPDF / PDFPlumber bookmark scanning for dense policy manuals (>300 pages, e.g. 910-page Cigna Lab Management).

## Data Inputs & Outputs
- **Input Queries**: Natural language clinical scenarios and CPT code queries.
- **Master CPT Table**: `output/table.json` containing prior authorization lookup data.
- **Policy Registry**: `hierarchical-processing/policies_manifest.json`.
- **Output Artifacts**: Validated structured JSON clinical determinations saved to `data/results_new/`.
