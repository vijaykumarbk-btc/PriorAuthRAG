# Technical Stack

## Core Technologies
- **Language**: Python 3.10+
- **Environment**: Virtual Environment (`venv/`), Linux x86_64

## Key Libraries & Dependencies
- **RAG & Search**:
  - `rank_bm25`: Fast BM25 keyword index implementation (`RankBM25Okapi`)
  - `numpy`: Array storage and vector math for dense embeddings
  - `scikit-learn` / `scipy`: Cosine similarity computation
- **Document Processing**:
  - `docling` & `docling-hierarchical-pdf`: PDF visual heading tree extraction (<= 300 pages)
  - `pdfplumber` / `pypdf`: Fallback outline and bookmark extraction for dense PDFs (> 300 pages)
- **LLM Integrations & APIs**:
  - `groq`: Primary cloud LLM inference API (`llama-3.1-8b-instant`, `groq/compound-mini`, `openai/gpt-oss-120b`)
  - `ollama`: Local LLM fallback engine (`medgemma-1.5-4b-it-GGUF:Q8_0`)
- **Data Engineering & Utilities**:
  - `pydantic`: Schema validation and structured dataclass configs
  - `json_repair`: Resilient JSON extraction and syntax repair for LLM outputs
  - `python-dotenv`: Environment configuration management

## Storage & File Artifacts
- **Embeddings**: `.npy` binary arrays (e.g. `embeddings/lumbar_embeddings.npy`)
- **BM25 Index**: `.pkl` serialized pickle files (e.g. `bm25/lumbar_bm25.pkl`)
- **TOC Trees & Chunks**: JSON format (`TOC/*.json`, `chunks/*.json`)
- **Structured Outputs**: JSON records stored in `data/results_new/`
