# Key Technical Concerns & Risks

## 1. Scale & Context Constraints on Dense Clinical Manuals
- **Problem**: Payers publish massive multi-policy manuals (e.g., Cigna Lab Management at 910 pages, 30MB+).
- **Risk**: Standard PDF parsers crash from memory allocation or fail to extract visual TOC subtrees.
- **Mitigation**: Implemented dual-strategy router in `fallback/` using regex outline matchers and page-offset calibration.

## 2. Dynamic Routing Accuracy
- **Problem**: Broad clinical queries may match multiple overlapping policies or sections.
- **Risk**: Missed section IDs during Stage 2 routing truncate the retrieval scope in Stage 3.
- **Mitigation**: Standardized `get_descendant_toc_ids()` subtree expansion and Sibling Condition Completion.

## 3. Dependency on External Cloud API & Rate Limits
- **Problem**: Groq API rate limits or network unavailability could interrupt automated evaluation pipelines.
- **Mitigation**: Local Ollama fallback (`medgemma-1.5-4b-it-GGUF:Q8_0`) configured for offline resilience.

## 4. Maintenance of Preprocessed Embeddings & Indexes
- **Problem**: Indexing scripts (`build_bm25.py`, `embedding_with_section.py`) must be rerun manually when adding new policy documents.
- **Mitigation**: Automate pipeline registration via CLI workflow tools.
