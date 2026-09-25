# Hierarchical Prior Authorization RAG Engine

The Hierarchical Prior Authorization RAG Engine enables accurate medical necessity verification against dense, structured insurance clinical guidelines (e.g. Cigna policies).

## Architecture

Traditional chunking splits documents into fixed-size character windows, which cuts through medical criteria lists, contraindications, and CPT code tables. This engine instead parses clinical guidelines into a **hierarchical tree**:

1. **Document Tree & TOC Extraction**: Identifies the hierarchical Table of Contents (policy title, section, subsection, clause, and subclause).
2. **Context-Preserving Hierarchical Chunks**: Every chunk retains its complete breadcrumb ancestry (e.g. `Coverage Policy > General Considerations > Lumbar Fusion > Spondylolisthesis > Criteria`).
3. **Dual-Index Generation**: Each policy produces:
   - A **BM25 Lexical Index** (for exact medical terms, acronyms, and CPT/HCPCS codes).
   - A **Dense Vector Embedding Matrix** (for semantic concept matching).

## Usage

Query the hierarchical retrieval system via the CLI:

```bash
# Query with specific policy scope
python retrieval-hierarchical.py --query "conservative treatment duration before spinal fusion" --policy "Lumbar"

# General search across loaded guidelines
python retrieval-hierarchical.py --query "BRCA1 genetic testing coverage criteria"
```

## Key Files
- [`retrieval-hierarchical.py`](../../retrieval-hierarchical.py): Main retrieval CLI with candidate re-ranking.
- [`hierarchical-processing/chunking_heirarchical.py`](../../hierarchical-processing/chunking_heirarchical.py): Hierarchical chunk splitter.
- [`hierarchical-processing/chunk_toc_mapper.py`](../../hierarchical-processing/chunk_toc_mapper.py): Maps chunks to TOC headings.
