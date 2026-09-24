# Functional & Quality Requirements

## 1. Prior Auth Determination Accuracy
- **Req-1.1**: Accurately flag "Prior Auth Required" status (Yes/No/Add-On) for 100% of CPT codes registered in `output/table.json`.
- **Req-1.2**: Support multi-CPT procedure lookup and synonym expansion (e.g. ACDF -> CPT 22551, Lumbar Fusion -> CPT 22612).

## 2. Multi-Document Routing & TOC Preservation
- **Req-2.1**: Route clinical queries to correct target policy document registered in `policies_manifest.json`.
- **Req-2.2**: Preserve hierarchical section IDs (`S1`, `S2.1`, `S7.1.6`) during chunking and vector embedding.
- **Req-2.3**: Automatically expand candidate section nodes to include all nested child descendant nodes via `get_descendant_toc_ids()`.

## 3. Hybrid Search & Sibling Condition Completion
- **Req-3.1**: Compute Reciprocal Rank Fusion (RRF) over BM25 keyword rankings and dense vector cosine similarities strictly bounded to candidate TOC sections.
- **Req-3.2**: Automatically retrieve clinical sibling conditions (e.g. Radiculopathy + Myelopathy) when one condition is retrieved, eliminating criteria incompleteness.

## 4. Resilient JSON Generation & Fallback
- **Req-4.1**: Produce valid, schema-compliant clinical JSON determination objects with all required fields.
- **Req-4.2**: Gracefully recover from LLM output formatting errors via `json_repair` and regex substring extraction.
- **Req-4.3**: Fallback seamlessly from primary cloud API (Groq) to local LLM endpoint (Ollama MedGemma) on API failure.

## 5. Large Document Ingestion Fallback
- **Req-5.1**: Route documents > 300 pages to tiered outline and regex bookmark extractor to prevent memory exhaustion and preserve visual TOC trees.
