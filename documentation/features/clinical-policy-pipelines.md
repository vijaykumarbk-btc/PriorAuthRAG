# Clinical Policy Ingestion Pipelines

The project maintains dedicated ingestion pipelines for major insurance guidelines, converting raw policy PDFs into indexed vector and lexical stores.

## Supported Guidelines

### 1. Lumbar Spinal Fusion ([`Lumbar/`](../../Lumbar/))
- **Source**: `Cigna_Lumbar_Fusion.pdf`
- **TOC Tree**: [`Lumbar/TOC/TOC_tree.txt`](../../Lumbar/TOC/TOC_tree.txt)
- **Hierarchical Chunks**: [`Lumbar/chunks/Cigna_Lumbar_Fusion_hierarchical_chunks.json`](../../Lumbar/chunks/Cigna_Lumbar_Fusion_hierarchical_chunks.json)
- **BM25 Index**: [`Lumbar/bm25/lumbar_fusion_bm25.pkl`](../../Lumbar/bm25/lumbar_fusion_bm25.pkl)
- **Dense Embeddings**: [`Lumbar/embeddings/lumbar_fusion_embeddings.npy`](../../Lumbar/embeddings/lumbar_fusion_embeddings.npy)

### 2. Clinical Lab Management ([`Lab_Management/`](../../Lab_Management/))
- **Source**: `Cigna_Lab_Management.pdf` (over 400 pages)
- **TOC Tree**: [`Lab_Management/TOC/Lab_Management_toc_tree.txt`](../../Lab_Management/TOC/Lab_Management_toc_tree.txt)
- **Hierarchical Chunks**: [`Lab_Management/chunks/Cigna_Lab_Management.hierarchical_chunks.json`](../../Lab_Management/chunks/Cigna_Lab_Management.hierarchical_chunks.json)
- **BM25 Index**: [`Lab_Management/bm25/lab_management_bm25.pkl`](../../Lab_Management/bm25/lab_management_bm25.pkl)
- **Dense Embeddings**: [`Lab_Management/embeddings/lab_management_embeddings.npy`](../../Lab_Management/embeddings/lab_management_embeddings.npy)

### 3. Radiation Oncology ([`Radiation/`](../../Radiation/))
- **Source**: `Cigna_Radiation_Oncology.pdf`
- **TOC Tree**: [`Radiation/toc/Cigna_Radiation_Oncology_toc_tree.txt`](../../Radiation/toc/Cigna_Radiation_Oncology_toc_tree.txt)
- **Hierarchical Chunks**: [`Radiation/chunks/Cigna_Radiation_Oncology.hierarchical_chunks.json`](../../Radiation/chunks/Cigna_Radiation_Oncology.hierarchical_chunks.json)
- **BM25 Index**: [`Radiation/bm25/Cigna_Radiation_Oncology_bm25.pkl`](../../Radiation/bm25/Cigna_Radiation_Oncology_bm25.pkl)
- **Dense Embeddings**: [`Radiation/embeddings/Cigna_Radiation_Oncology_embeddings.npy`](../../Radiation/embeddings/Cigna_Radiation_Oncology_embeddings.npy)

### 4. Knee Arthroscopy & Reconstruction ([`data/policies/Cigna_Knee/`](../../data/policies/Cigna_Knee/))
- Ingested via automated ingestion script [`ingest_policy.py`](../../ingest_policy.py).

## Ingestion Command

To ingest a new clinical guideline PDF:

```bash
python ingest_policy.py --pdf path/to/policy.pdf --name "Policy_Name"
```
