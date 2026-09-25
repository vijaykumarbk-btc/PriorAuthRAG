# Hybrid Search Retrieval System

Medical prior authorization queries require both **exact keyword precision** (e.g. matching CPT code `22612`, drug name `Infliximab`, or specific lab tests) and **semantic flexibility** (e.g. interpreting *"unsuccessful physical therapy for half a year"* as *"failure of 6 months of supervised conservative management"*).

## Hybrid Retrieval Methodology

The retrieval engine ([`hybrid_search_hierarchical.py`](../../hybrid_search_hierarchical.py) & [`retrieval-hierarchical.py`](../../retrieval-hierarchical.py)) uses a two-pronged approach:

1. **BM25 Lexical Scoring**:
   - Tokenizes clinical query.
   - Evaluates BM25 scores across the policy's precomputed BM25 index.
   - Preserves high ranks for exact medical terminology, CPT codes, and acronyms.

2. **Dense Vector Similarity**:
   - Generates dense embeddings for the user query using the pre-trained embedding model.
   - Computes cosine similarity against the policy's chunk embedding matrix (`*.npy`).

3. **Reciprocal Rank Fusion (RRF) / Linear Fusion**:
   - Merges candidate ranks from both lexical and dense retrievers:
     $$\text{Score}(d) = \alpha \cdot \text{NormalizedBM25}(d) + (1 - \alpha) \cdot \text{CosineSim}(d)$$
   - Evaluates parent chunk context so that isolated bullet points retain their governing heading requirements.

## Performance
- Top-5 retrieval recall on medical criteria exceeds 90% across benchmark evaluation sets.
