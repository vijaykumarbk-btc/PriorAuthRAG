# Codebase Directory Structure

```
project2/
├── README.md                                # Main project documentation
├── architecture.md                          # Comprehensive pipeline architecture spec
├── next_step.md                             # Roadmap and future engineering tasks
├── EXECUTION-STEPS.md                       # Ingestion & evaluation instructions
├── CONTEXT_HISTORY.md                       # Historical context & decision records
├── requirements.txt                         # Python dependencies
├── .env / .env.example                      # Environment variables
│
├── hierarchical-processing/                 # Core processing & ingestion pipeline
│   ├── policies_manifest.json               # Policy document registry metadata
│   ├── document_registry.py                 # Multi-policy dynamic registry loader
│   ├── cpt_table_lookup.py                  # Stage 1: CPT master table lookup engine
│   ├── toc_v2.py                            # Stage 2: TOC tree generator from JSON blocks
│   ├── chunking_heirarchical.py             # Stage 3: Criteria-aware markdown chunker
│   ├── chunk_toc_mapper.py                  # Stage 4: Stamps chunks with TOC section IDs
│   ├── embedding_with_section.py            # Stage 5: Dense embedding generator
│   └── build_bm25.py                        # Stage 6: Section-aware BM25 index builder
│
├── fallback/                                # Tiered fallback pipeline for large PDFs (>300p)
│   ├── pipeline.py                          # Dual-strategy router & fallback orchestrator
│   ├── extractors.py                        # PDF outline, bookmark & regex extractors
│   ├── builder.py                           # Block normalizer & QA report builder
│   └── config.py                            # Dataclasses & threshold configuration
│
├── output/
│   └── table.json                           # Master CPT / HCPCS Prior Auth Table
│
├── hybrid_search_hierarchical.py            # Scoped hybrid search & sibling completion
├── retrieval-hierarchical.py                # Main end-to-end multi-document RAG pipeline
├── eval_lab_management_benchmark.py         # 20-query clinical evaluation benchmark
│
├── Lumbar/                                  # Cigna Lumbar Fusion policy artifacts
│   ├── TOC/                                 # Lumbar TOC JSON tree
│   ├── chunks/                              # Enriched chunks & metadata
│   ├── embeddings/                          # Dense embedding vectors (.npy)
│   └── bm25/                                # BM25 index (.pkl)
│
├── Lab_Management/                          # Cigna Laboratory Management policy artifacts (910p)
│   ├── raw/                                 # Raw policy PDF
│   ├── output_tiered/                       # Tiered markdown and JSON blocks
│   ├── TOC/                                 # Visual TOC JSON tree
│   ├── chunks/                              # Enriched chunks & metadata
│   ├── embeddings/                          # Dense embeddings (.npy)
│   └── bm25/                                # BM25 index (.pkl)
│
├── Radiation/                               # Cigna Radiation Therapy policy artifacts
│   └── ...                                  # Preprocessed artifacts & embeddings
│
└── data/
    └── results_new/                         # Output clinical JSON determination files
```
