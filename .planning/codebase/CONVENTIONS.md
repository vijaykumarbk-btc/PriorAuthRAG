# Coding Conventions & Design Patterns

## Architectural Patterns
- **4-Stage Sequential Pipeline**: Modular separation between master table lookup, document routing, scoped search, and clinical JSON synthesis.
- **Dynamic Policy Registry**: All policy documents are registered in `policies_manifest.json` with explicit metadata paths (`TOC`, `chunks`, `embeddings`, `bm25`), enabling dynamic multi-policy routing.
- **Fail-Safe & Tiered Fallbacks**:
  - Large document ingestion: Docling router falls back to PyPDF/regex outline extraction for PDFs > 300 pages.
  - LLM Inference: Primary cloud LLM via Groq falls back to local Ollama (`medgemma-1.5-4b-it-GGUF:Q8_0`).
  - JSON Parsing: Multi-stage extraction (tag stripping, substring slicing) with `json_repair` normalization.

## Code & Naming Style
- **Python**: PEP8 compliant, modular functions with clear docstrings and typing annotations where critical.
- **File Naming**: snake_case for modules (`cpt_table_lookup.py`, `hybrid_search_hierarchical.py`, `retrieval-hierarchical.py`).
- **Data Structures**: Uses Python `dataclass` and `Pydantic` models for structured configs and schemas.

## Configuration & Secrets Management
- Secrets and API credentials (`GROQ_API_KEY`, base URLs) are loaded exclusively via `python-dotenv` from `.env`.
- System settings and threshold defaults are centralized in `fallback/config.py` and manifest files.
