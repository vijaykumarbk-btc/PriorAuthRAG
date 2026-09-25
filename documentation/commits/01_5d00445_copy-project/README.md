# Commit 1: copy project

<nav>
  <a href="../README.md">All Commits Index</a>
 | <a href="../02_a7b0a69_2nd/README.md">Commit 2 (a7b0a69) &rarr;</a>
</nav>

---

## Metadata

| Attribute | Value |
| :--- | :--- |
| **Commit Hash** | `5d00445` (`5d0044598e3cd33b05afea3afe839a126efe2532`) |
| **Author** | vijaykumarbk <vijaykumarb@boston-technology.com> |
| **Date** | 2026-09-08 10:46:04 +0530 |
| **Files Touched** | **226** (226 added, 0 modified, 0 deleted) |
| **Lines Changed** | **+1367050** / **-0** |

## 1. Intent & Purpose

Initialize the repository baseline by importing early prototype code for medical clinical policy parsing and embedding generation.

## 2. Key Architectural Decisions (ADR Rationale)

Eschewed flat character-window chunking in favor of exploring hierarchical chunking (`chunking.py`) to preserve medical policy clause ancestry. Established parallel tracks for BM25 lexical search (`bm25_index.py`) and vector embeddings.

## 3. Cumulative System Capability (State Until This Commit)

> [!NOTE]
> **System State as of `5d00445`**:
> The project can ingest initial PDF policies (Cigna ACDF, Lumbar) and execute prototype chunking and standalone vector embedding scripts. No unified retrieval CLI or automated pipeline exists yet.

## 4. What Actually Changed (Functional Breakdown)

- Imported core PDF documents (`Cigna_ACDF.pdf`, `Cigna_Lumbar_Fusion.pdf`) into `data/raw/`.
- Added `chunking.py` implementing initial parent-child chunk mapping experiments.
- Added `bm25_index.py` for early lexical search prototyping.
- Drafted initial `architecture.md` outlining the end-to-end vision for Prior Authorization retrieval.

## 5. Affected Files & Line Diffs

<details>
<summary><b>View all 226 changed files</b> (Click to expand)</summary>

| Status | File Path | Lines (+/-) |
| :--- | :--- | :--- |
| 🟢 Added | [.env.example](../../../.env.example) | +14 / -0 |
| 🟢 Added | [.gitignore](../../../.gitignore) | +8 / -0 |
| 🟢 Added | [.vscode/settings.json](../../../.vscode/settings.json) | +3 / -0 |
| 🟢 Added | `Cigna_ACDF_embeddings.json` | +43012 / -0 |
| 🟢 Added | `LiteParse.py` | +53 / -0 |
| 🟢 Added | `SPECIAL OUT.json` | +36 / -0 |
| 🟢 Added | `SPECIAL_OUT.json` | +36 / -0 |
| 🟢 Added | [architecture.md](../../../architecture.md) | +231 / -0 |
| 🟢 Added | [bm25_index.py](../../../bm25_index.py) | +53 / -0 |
| 🟢 Added | `check.py` | +9 / -0 |
| 🟢 Added | `check_embeddings.py` | +6 / -0 |
| 🟢 Added | [chunking.py](../../../chunking.py) | +783 / -0 |
| 🟢 Added | `chunking_langchain.py` | +17 / -0 |
| 🟢 Added | [csv_to_json.py](../../../csv_to_json.py) | +96 / -0 |
| 🟢 Added | [data/chunks/Cigna_ACDF_chunks.json](../../../data/chunks/Cigna_ACDF_chunks.json) | +552 / -0 |
| 🟢 Added | [data/chunks/Cigna_Lumbar_Fusion_chunks.json](../../../data/chunks/Cigna_Lumbar_Fusion_chunks.json) | +732 / -0 |
| 🟢 Added | [data/chunks/new/ACDF_CLOUDCONVERT_chunks.json](../../../data/chunks/new/ACDF_CLOUDCONVERT_chunks.json) | +542 / -0 |
| 🟢 Added | [data/chunks/new/Lumbar_CLOUDCONVERT_chunks.json](../../../data/chunks/new/Lumbar_CLOUDCONVERT_chunks.json) | +752 / -0 |
| 🟢 Added | [data/embeddings/new_embeddings/Cigna_ACDF_bm25.pkl](../../../data/embeddings/new_embeddings/Cigna_ACDF_bm25.pkl) | - |
| 🟢 Added | [data/embeddings/new_embeddings/Cigna_ACDF_embeddings.npy](../../../data/embeddings/new_embeddings/Cigna_ACDF_embeddings.npy) | - |
| 🟢 Added | [data/embeddings/new_embeddings/Cigna_ACDF_metadata.json](../../../data/embeddings/new_embeddings/Cigna_ACDF_metadata.json) | +607 / -0 |
| 🟢 Added | [data/embeddings/new_embeddings_CLOUDCONVERT/ACDF_CLOUDCONVERT_bm25.pkl](../../../data/embeddings/new_embeddings_CLOUDCONVERT/ACDF_CLOUDCONVERT_bm25.pkl) | - |
| 🟢 Added | [data/embeddings/new_embeddings_CLOUDCONVERT/ACDF_CLOUDCONVERT_embeddings.npy](../../../data/embeddings/new_embeddings_CLOUDCONVERT/ACDF_CLOUDCONVERT_embeddings.npy) | - |
| 🟢 Added | [data/embeddings/new_embeddings_CLOUDCONVERT/ACDF_CLOUDCONVERT_metadata.json](../../../data/embeddings/new_embeddings_CLOUDCONVERT/ACDF_CLOUDCONVERT_metadata.json) | +596 / -0 |
| 🟢 Added | [data/embeddings/new_embeddings_CLOUDCONVERT/Lumbar_CLOUDCONVERT_bm25.pkl](../../../data/embeddings/new_embeddings_CLOUDCONVERT/Lumbar_CLOUDCONVERT_bm25.pkl) | - |
| 🟢 Added | [data/embeddings/new_embeddings_CLOUDCONVERT/Lumbar_CLOUDCONVERT_embeddings.npy](../../../data/embeddings/new_embeddings_CLOUDCONVERT/Lumbar_CLOUDCONVERT_embeddings.npy) | - |
| 🟢 Added | [data/embeddings/new_embeddings_CLOUDCONVERT/Lumbar_CLOUDCONVERT_metadata.json](../../../data/embeddings/new_embeddings_CLOUDCONVERT/Lumbar_CLOUDCONVERT_metadata.json) | +827 / -0 |
| 🟢 Added | [data/embeddings/old_embeddings/Cigna_ACDF_embeddings.npy](../../../data/embeddings/old_embeddings/Cigna_ACDF_embeddings.npy) | - |
| 🟢 Added | [data/embeddings/old_embeddings/Cigna_ACDF_metadata.json](../../../data/embeddings/old_embeddings/Cigna_ACDF_metadata.json) | +552 / -0 |
| 🟢 Added | [data/embeddings/old_embeddings/Cigna_Lumbar_Fusion_embeddings.npy](../../../data/embeddings/old_embeddings/Cigna_Lumbar_Fusion_embeddings.npy) | - |
| 🟢 Added | [data/embeddings/old_embeddings/Cigna_Lumbar_Fusion_metadata.json](../../../data/embeddings/old_embeddings/Cigna_Lumbar_Fusion_metadata.json) | +732 / -0 |
| 🟢 Added | [data/markdown/Cigna_ACDF.md](../../../data/markdown/Cigna_ACDF.md) | +1516 / -0 |
| 🟢 Added | [data/markdown/Cigna_Lumbar_Fusion.md](../../../data/markdown/Cigna_Lumbar_Fusion.md) | +1759 / -0 |
| 🟢 Added | [data/markdown/new/ACDF_CLOUDCONVERT.md](../../../data/markdown/new/ACDF_CLOUDCONVERT.md) | +1063 / -0 |
| 🟢 Added | [data/markdown/new/Lumbar_CLOUDCONVERT.md](../../../data/markdown/new/Lumbar_CLOUDCONVERT.md) | +1359 / -0 |
| 🟢 Added | [data/raw/Cigna_ACDF.pdf](../../../data/raw/Cigna_ACDF.pdf) | - |
| 🟢 Added | `data/raw/Cigna_Lumbar_Fusion.pdf` | - |
| 🟢 Added | [data/result-old/20260818_152553_requirements_for_CMM6017_Adjacent_Segment_Disease.md](../../../data/result-old/20260818_152553_requirements_for_CMM6017_Adjacent_Segment_Disease.md) | +134 / -0 |
| 🟢 Added | [data/result-old/20260818_153849_requirements_for_Adjacent_Segment_Disease.md](../../../data/result-old/20260818_153849_requirements_for_Adjacent_Segment_Disease.md) | +133 / -0 |
| 🟢 Added | [data/result-old/20260818_154014_requirements_for_Adjacent_Segment_Disease_radiculo.md](../../../data/result-old/20260818_154014_requirements_for_Adjacent_Segment_Disease_radiculo.md) | +185 / -0 |
| 🟢 Added | [data/result-old/20260818_161245_documents_required_for_adjacent_segment_disease.md](../../../data/result-old/20260818_161245_documents_required_for_adjacent_segment_disease.md) | +172 / -0 |
| 🟢 Added | [data/result-old/20260818_161456_requirements_for_adjacent_segment_disease.md](../../../data/result-old/20260818_161456_requirements_for_adjacent_segment_disease.md) | +121 / -0 |
| 🟢 Added | [data/result-old/20260818_162101_requirements_for_adjacent_segment_disease.md](../../../data/result-old/20260818_162101_requirements_for_adjacent_segment_disease.md) | +121 / -0 |
| 🟢 Added | [data/result-old/20260818_162140_requirements_for_adjacent_segment_disease_radiculo.md](../../../data/result-old/20260818_162140_requirements_for_adjacent_segment_disease_radiculo.md) | +213 / -0 |
| 🟢 Added | [data/result-old/20260818_162657_requirements_for_adjacent_segment_disease.md](../../../data/result-old/20260818_162657_requirements_for_adjacent_segment_disease.md) | +121 / -0 |
| 🟢 Added | [data/result-old/20260818_163730_requirements_for_adjacent_segment_disease.md](../../../data/result-old/20260818_163730_requirements_for_adjacent_segment_disease.md) | +133 / -0 |
| 🟢 Added | [data/result-old/20260818_163805_requirements_for_Adjacent_Segment_Disease.md](../../../data/result-old/20260818_163805_requirements_for_Adjacent_Segment_Disease.md) | +135 / -0 |
| 🟢 Added | [data/result-old/20260818_163916_document_requirements_for_adjacent_segment_disease.md](../../../data/result-old/20260818_163916_document_requirements_for_adjacent_segment_disease.md) | +115 / -0 |
| 🟢 Added | [data/result-old/20260818_164001_requirements_for_adjacent_segment_disease.md](../../../data/result-old/20260818_164001_requirements_for_adjacent_segment_disease.md) | +133 / -0 |
| 🟢 Added | [data/result-old/20260818_164150_requirements_for_adjacent_segment_disease.md](../../../data/result-old/20260818_164150_requirements_for_adjacent_segment_disease.md) | +133 / -0 |
| 🟢 Added | [data/result-old/20260818_164344_requirements_for_adjacent_segment_disease.md](../../../data/result-old/20260818_164344_requirements_for_adjacent_segment_disease.md) | +133 / -0 |
| 🟢 Added | `docling/TOC.py` | +17 / -0 |
| 🟢 Added | [docling/docling_pdf.py](../../../docling/docling_pdf.py) | +732 / -0 |
| 🟢 Added | [docling/docling_plain.py](../../../docling/docling_plain.py) | +38 / -0 |
| 🟢 Added | [docling/pdf_json.py](../../../docling/pdf_json.py) | +57 / -0 |
| 🟢 Added | [docling/pdf_new.py](../../../docling/pdf_new.py) | +102 / -0 |
| 🟢 Added | [docling/table.py](../../../docling/table.py) | +256 / -0 |
| 🟢 Added | [embedding.py](../../../embedding.py) | +126 / -0 |
| 🟢 Added | [embedding_with_section.py](../../../embedding_with_section.py) | +110 / -0 |
| 🟢 Added | `embeddings_json.json` | +746868 / -0 |
| 🟢 Added | `evaluate_benchmark.py` | +244 / -0 |
| 🟢 Added | [extra_pdfs/Cigna_Knee.cleaned.pdf](../../../extra_pdfs/Cigna_Knee.cleaned.pdf) | - |
| 🟢 Added | [extra_pdfs/Cigna_Knee.pdf](../../../extra_pdfs/Cigna_Knee.pdf) | - |
| 🟢 Added | `extra_pdfs/Cigna_Lab Mgmt.pdf` | - |
| 🟢 Added | [extra_pdfs/Cigna_Radiation_Oncology.cleaned.pdf](../../../extra_pdfs/Cigna_Radiation_Oncology.cleaned.pdf) | - |
| 🟢 Added | [extra_pdfs/Cigna_Radiation_Oncology.pdf](../../../extra_pdfs/Cigna_Radiation_Oncology.pdf) | - |
| 🟢 Added | [extra_pdfs/Table.pdf](../../../extra_pdfs/Table.pdf) | - |
| 🟢 Added | [extra_pdfs/Table_table_1.csv](../../../extra_pdfs/Table_table_1.csv) | +65 / -0 |
| 🟢 Added | [extra_pdfs/Table_table_10.csv](../../../extra_pdfs/Table_table_10.csv) | +82 / -0 |
| 🟢 Added | [extra_pdfs/Table_table_11.csv](../../../extra_pdfs/Table_table_11.csv) | +77 / -0 |
| 🟢 Added | [extra_pdfs/Table_table_12.csv](../../../extra_pdfs/Table_table_12.csv) | +76 / -0 |
| 🟢 Added | [extra_pdfs/Table_table_13.csv](../../../extra_pdfs/Table_table_13.csv) | +72 / -0 |
| 🟢 Added | [extra_pdfs/Table_table_14.csv](../../../extra_pdfs/Table_table_14.csv) | +69 / -0 |
| 🟢 Added | [extra_pdfs/Table_table_15.csv](../../../extra_pdfs/Table_table_15.csv) | +70 / -0 |
| 🟢 Added | [extra_pdfs/Table_table_16.csv](../../../extra_pdfs/Table_table_16.csv) | +75 / -0 |
| 🟢 Added | [extra_pdfs/Table_table_17.csv](../../../extra_pdfs/Table_table_17.csv) | +68 / -0 |
| 🟢 Added | [extra_pdfs/Table_table_18.csv](../../../extra_pdfs/Table_table_18.csv) | +78 / -0 |
| 🟢 Added | [extra_pdfs/Table_table_19.csv](../../../extra_pdfs/Table_table_19.csv) | +74 / -0 |
| 🟢 Added | [extra_pdfs/Table_table_2.csv](../../../extra_pdfs/Table_table_2.csv) | +88 / -0 |
| 🟢 Added | [extra_pdfs/Table_table_20.csv](../../../extra_pdfs/Table_table_20.csv) | +77 / -0 |
| 🟢 Added | [extra_pdfs/Table_table_21.csv](../../../extra_pdfs/Table_table_21.csv) | +84 / -0 |
| 🟢 Added | [extra_pdfs/Table_table_22.csv](../../../extra_pdfs/Table_table_22.csv) | +64 / -0 |
| 🟢 Added | [extra_pdfs/Table_table_23.csv](../../../extra_pdfs/Table_table_23.csv) | +48 / -0 |
| 🟢 Added | [extra_pdfs/Table_table_24.csv](../../../extra_pdfs/Table_table_24.csv) | +49 / -0 |
| 🟢 Added | [extra_pdfs/Table_table_25.csv](../../../extra_pdfs/Table_table_25.csv) | +43 / -0 |
| 🟢 Added | [extra_pdfs/Table_table_26.csv](../../../extra_pdfs/Table_table_26.csv) | +85 / -0 |
| 🟢 Added | [extra_pdfs/Table_table_27.csv](../../../extra_pdfs/Table_table_27.csv) | +91 / -0 |
| 🟢 Added | [extra_pdfs/Table_table_28.csv](../../../extra_pdfs/Table_table_28.csv) | +92 / -0 |
| 🟢 Added | [extra_pdfs/Table_table_29.csv](../../../extra_pdfs/Table_table_29.csv) | +97 / -0 |
| 🟢 Added | [extra_pdfs/Table_table_3.csv](../../../extra_pdfs/Table_table_3.csv) | +88 / -0 |
| 🟢 Added | [extra_pdfs/Table_table_30.csv](../../../extra_pdfs/Table_table_30.csv) | +85 / -0 |
| 🟢 Added | [extra_pdfs/Table_table_31.csv](../../../extra_pdfs/Table_table_31.csv) | +84 / -0 |
| 🟢 Added | [extra_pdfs/Table_table_32.csv](../../../extra_pdfs/Table_table_32.csv) | +77 / -0 |
| 🟢 Added | [extra_pdfs/Table_table_33.csv](../../../extra_pdfs/Table_table_33.csv) | +83 / -0 |
| 🟢 Added | [extra_pdfs/Table_table_34.csv](../../../extra_pdfs/Table_table_34.csv) | +63 / -0 |
| 🟢 Added | [extra_pdfs/Table_table_35.csv](../../../extra_pdfs/Table_table_35.csv) | +81 / -0 |
| 🟢 Added | [extra_pdfs/Table_table_36.csv](../../../extra_pdfs/Table_table_36.csv) | +81 / -0 |
| 🟢 Added | [extra_pdfs/Table_table_37.csv](../../../extra_pdfs/Table_table_37.csv) | +73 / -0 |
| 🟢 Added | [extra_pdfs/Table_table_38.csv](../../../extra_pdfs/Table_table_38.csv) | +69 / -0 |
| 🟢 Added | [extra_pdfs/Table_table_39.csv](../../../extra_pdfs/Table_table_39.csv) | +91 / -0 |
| 🟢 Added | [extra_pdfs/Table_table_4.csv](../../../extra_pdfs/Table_table_4.csv) | +81 / -0 |
| 🟢 Added | [extra_pdfs/Table_table_40.csv](../../../extra_pdfs/Table_table_40.csv) | +77 / -0 |
| 🟢 Added | [extra_pdfs/Table_table_41.csv](../../../extra_pdfs/Table_table_41.csv) | +100 / -0 |
| 🟢 Added | [extra_pdfs/Table_table_42.csv](../../../extra_pdfs/Table_table_42.csv) | +76 / -0 |
| 🟢 Added | [extra_pdfs/Table_table_43.csv](../../../extra_pdfs/Table_table_43.csv) | +72 / -0 |
| 🟢 Added | [extra_pdfs/Table_table_44.csv](../../../extra_pdfs/Table_table_44.csv) | +67 / -0 |
| 🟢 Added | [extra_pdfs/Table_table_45.csv](../../../extra_pdfs/Table_table_45.csv) | +73 / -0 |
| 🟢 Added | [extra_pdfs/Table_table_46.csv](../../../extra_pdfs/Table_table_46.csv) | +73 / -0 |
| 🟢 Added | [extra_pdfs/Table_table_47.csv](../../../extra_pdfs/Table_table_47.csv) | +71 / -0 |
| 🟢 Added | [extra_pdfs/Table_table_48.csv](../../../extra_pdfs/Table_table_48.csv) | +67 / -0 |
| 🟢 Added | [extra_pdfs/Table_table_49.csv](../../../extra_pdfs/Table_table_49.csv) | +73 / -0 |
| 🟢 Added | [extra_pdfs/Table_table_5.csv](../../../extra_pdfs/Table_table_5.csv) | +78 / -0 |
| 🟢 Added | [extra_pdfs/Table_table_50.csv](../../../extra_pdfs/Table_table_50.csv) | +18 / -0 |
| 🟢 Added | [extra_pdfs/Table_table_6.csv](../../../extra_pdfs/Table_table_6.csv) | +78 / -0 |
| 🟢 Added | [extra_pdfs/Table_table_7.csv](../../../extra_pdfs/Table_table_7.csv) | +78 / -0 |
| 🟢 Added | [extra_pdfs/Table_table_8.csv](../../../extra_pdfs/Table_table_8.csv) | +83 / -0 |
| 🟢 Added | [extra_pdfs/Table_table_9.csv](../../../extra_pdfs/Table_table_9.csv) | +76 / -0 |
| 🟢 Added | [extra_pdfs/merged_output.csv](../../../extra_pdfs/merged_output.csv) | +3544 / -0 |
| 🟢 Added | [extra_pdfs/merged_output.json](../../../extra_pdfs/merged_output.json) | +15112 / -0 |
| 🟢 Added | [extra_pdfs/output.md](../../../extra_pdfs/output.md) | +7416 / -0 |
| 🟢 Added | [hierarchical-processing/ACDF_toc_output_new.json](../../../hierarchical-processing/ACDF_toc_output_new.json) | +16169 / -0 |
| 🟢 Added | [hierarchical-processing/Cigna_ACDF_enriched_chunks.json](../../../hierarchical-processing/Cigna_ACDF_enriched_chunks.json) | +3057 / -0 |
| 🟢 Added | [hierarchical-processing/Cigna_ACDF_hierarchical.json](../../../hierarchical-processing/Cigna_ACDF_hierarchical.json) | +15220 / -0 |
| 🟢 Added | [hierarchical-processing/Cigna_ACDF_hierarchical.md](../../../hierarchical-processing/Cigna_ACDF_hierarchical.md) | +1189 / -0 |
| 🟢 Added | [hierarchical-processing/Cigna_ACDF_hierarchical_chunks.json](../../../hierarchical-processing/Cigna_ACDF_hierarchical_chunks.json) | +1772 / -0 |
| 🟢 Added | [hierarchical-processing/Cigna_Lumbar_Fusion_enriched_chunks.json](../../../hierarchical-processing/Cigna_Lumbar_Fusion_enriched_chunks.json) | +5220 / -0 |
| 🟢 Added | [hierarchical-processing/acdf_bm25.pkl](../../../hierarchical-processing/acdf_bm25.pkl) | - |
| 🟢 Added | [hierarchical-processing/acdf_embeddings.npy](../../../hierarchical-processing/acdf_embeddings.npy) | - |
| 🟢 Added | [hierarchical-processing/acdf_metadata.json](../../../hierarchical-processing/acdf_metadata.json) | +3234 / -0 |
| 🟢 Added | [hierarchical-processing/build_bm25.py](../../../hierarchical-processing/build_bm25.py) | +62 / -0 |
| 🟢 Added | [hierarchical-processing/chunk_toc_mapper.py](../../../hierarchical-processing/chunk_toc_mapper.py) | +202 / -0 |
| 🟢 Added | [hierarchical-processing/chunking_heirarchical.py](../../../hierarchical-processing/chunking_heirarchical.py) | +783 / -0 |
| 🟢 Added | [hierarchical-processing/cpt_table_lookup.py](../../../hierarchical-processing/cpt_table_lookup.py) | +153 / -0 |
| 🟢 Added | [hierarchical-processing/document_registry.py](../../../hierarchical-processing/document_registry.py) | +183 / -0 |
| 🟢 Added | [hierarchical-processing/embedding_with_section.py](../../../hierarchical-processing/embedding_with_section.py) | +137 / -0 |
| 🟢 Added | [hierarchical-processing/generate_policy_json.py](../../../hierarchical-processing/generate_policy_json.py) | +186 / -0 |
| 🟢 Added | [hierarchical-processing/md/Cigna_Lumbar_Fusion_hierarchical.json](../../../hierarchical-processing/md/Cigna_Lumbar_Fusion_hierarchical.json) | +16896 / -0 |
| 🟢 Added | [hierarchical-processing/md/Cigna_Lumbar_Fusion_hierarchical.md](../../../hierarchical-processing/md/Cigna_Lumbar_Fusion_hierarchical.md) | +1177 / -0 |
| 🟢 Added | [hierarchical-processing/md/Lumbar_toc_output.json](../../../hierarchical-processing/md/Lumbar_toc_output.json) | +16965 / -0 |
| 🟢 Added | [hierarchical-processing/md/bm25/lumbar_fusion_bm25.pkl](../../../hierarchical-processing/md/bm25/lumbar_fusion_bm25.pkl) | - |
| 🟢 Added | [hierarchical-processing/md/chunks/Cigna_Lumbar_Fusion_hierarchical_chunks.json](../../../hierarchical-processing/md/chunks/Cigna_Lumbar_Fusion_hierarchical_chunks.json) | +3022 / -0 |
| 🟢 Added | [hierarchical-processing/md/embeddings/lumbar_fusion_embeddings.npy](../../../hierarchical-processing/md/embeddings/lumbar_fusion_embeddings.npy) | - |
| 🟢 Added | [hierarchical-processing/md/embeddings/lumbar_fusion_metadata.json](../../../hierarchical-processing/md/embeddings/lumbar_fusion_metadata.json) | +5220 / -0 |
| 🟢 Added | [hierarchical-processing/md/toc_tree.txt](../../../hierarchical-processing/md/toc_tree.txt) | +70 / -0 |
| 🟢 Added | [hierarchical-processing/policies_manifest.json](../../../hierarchical-processing/policies_manifest.json) | +21 / -0 |
| 🟢 Added | [hierarchical-processing/retrieve.py](../../../hierarchical-processing/retrieve.py) | +429 / -0 |
| 🟢 Added | [hierarchical-processing/toc_output.json](../../../hierarchical-processing/toc_output.json) | +15721 / -0 |
| 🟢 Added | [hierarchical-processing/toc_tree.txt](../../../hierarchical-processing/toc_tree.txt) | +51 / -0 |
| 🟢 Added | [hierarchical-processing/toc_v2.py](../../../hierarchical-processing/toc_v2.py) | +405 / -0 |
| 🟢 Added | [hybrid_search.py](../../../hybrid_search.py) | +127 / -0 |
| 🟢 Added | [hybrid_search_hierarchical.py](../../../hybrid_search_hierarchical.py) | +523 / -0 |
| 🟢 Added | `hypothermia_checking.py` | +44 / -0 |
| 🟢 Added | `issues.md` | +509 / -0 |
| 🟢 Added | `new_embedding.py` | +291 / -0 |
| 🟢 Added | [next_step.md](../../../next_step.md) | +1067 / -0 |
| 🟢 Added | [node_modules/.bin/lit](../../../node_modules/.bin/lit) | +1 / -0 |
| 🟢 Added | [node_modules/.bin/liteparse](../../../node_modules/.bin/liteparse) | +1 / -0 |
| 🟢 Added | [node_modules/.package-lock.json](../../../node_modules/.package-lock.json) | +71 / -0 |
| 🟢 Added | [node_modules/@llamaindex/liteparse-linux-x64-gnu/libpdfium.so](../../../node_modules/@llamaindex/liteparse-linux-x64-gnu/libpdfium.so) | - |
| 🟢 Added | [node_modules/@llamaindex/liteparse-linux-x64-gnu/liteparse.linux-x64-gnu.node](../../../node_modules/@llamaindex/liteparse-linux-x64-gnu/liteparse.linux-x64-gnu.node) | - |
| 🟢 Added | [node_modules/@llamaindex/liteparse-linux-x64-gnu/package.json](../../../node_modules/@llamaindex/liteparse-linux-x64-gnu/package.json) | +14 / -0 |
| 🟢 Added | [node_modules/@llamaindex/liteparse-linux-x64-musl/libpdfium.so](../../../node_modules/@llamaindex/liteparse-linux-x64-musl/libpdfium.so) | - |
| 🟢 Added | [node_modules/@llamaindex/liteparse-linux-x64-musl/liteparse.linux-x64-musl.node](../../../node_modules/@llamaindex/liteparse-linux-x64-musl/liteparse.linux-x64-musl.node) | - |
| 🟢 Added | [node_modules/@llamaindex/liteparse-linux-x64-musl/package.json](../../../node_modules/@llamaindex/liteparse-linux-x64-musl/package.json) | +14 / -0 |
| 🟢 Added | [node_modules/@llamaindex/liteparse-wasm/README.md](../../../node_modules/@llamaindex/liteparse-wasm/README.md) | +121 / -0 |
| 🟢 Added | [node_modules/@llamaindex/liteparse-wasm/package.json](../../../node_modules/@llamaindex/liteparse-wasm/package.json) | +48 / -0 |
| 🟢 Added | [node_modules/@llamaindex/liteparse-wasm/pkg/liteparse_wasm.d.ts](../../../node_modules/@llamaindex/liteparse-wasm/pkg/liteparse_wasm.d.ts) | +726 / -0 |
| 🟢 Added | [node_modules/@llamaindex/liteparse-wasm/pkg/liteparse_wasm.js](../../../node_modules/@llamaindex/liteparse-wasm/pkg/liteparse_wasm.js) | +1088 / -0 |
| 🟢 Added | [node_modules/@llamaindex/liteparse-wasm/pkg/liteparse_wasm_bg.wasm](../../../node_modules/@llamaindex/liteparse-wasm/pkg/liteparse_wasm_bg.wasm) | - |
| 🟢 Added | [node_modules/@llamaindex/liteparse-wasm/pkg/liteparse_wasm_bg.wasm.d.ts](../../../node_modules/@llamaindex/liteparse-wasm/pkg/liteparse_wasm_bg.wasm.d.ts) | +31 / -0 |
| 🟢 Added | [node_modules/@llamaindex/liteparse-wasm/pkg/package.json](../../../node_modules/@llamaindex/liteparse-wasm/pkg/package.json) | +21 / -0 |
| 🟢 Added | [node_modules/@llamaindex/liteparse/README.md](../../../node_modules/@llamaindex/liteparse/README.md) | +213 / -0 |
| 🟢 Added | [node_modules/@llamaindex/liteparse/dist/cli-json.d.ts](../../../node_modules/@llamaindex/liteparse/dist/cli-json.d.ts) | +154 / -0 |
| 🟢 Added | [node_modules/@llamaindex/liteparse/dist/cli-json.d.ts.map](../../../node_modules/@llamaindex/liteparse/dist/cli-json.d.ts.map) | +1 / -0 |
| 🟢 Added | [node_modules/@llamaindex/liteparse/dist/cli-json.js](../../../node_modules/@llamaindex/liteparse/dist/cli-json.js) | +241 / -0 |
| 🟢 Added | [node_modules/@llamaindex/liteparse/dist/cli-json.js.map](../../../node_modules/@llamaindex/liteparse/dist/cli-json.js.map) | +1 / -0 |
| 🟢 Added | [node_modules/@llamaindex/liteparse/dist/cli.d.ts](../../../node_modules/@llamaindex/liteparse/dist/cli.d.ts) | +3 / -0 |
| 🟢 Added | [node_modules/@llamaindex/liteparse/dist/cli.d.ts.map](../../../node_modules/@llamaindex/liteparse/dist/cli.d.ts.map) | +1 / -0 |
| 🟢 Added | [node_modules/@llamaindex/liteparse/dist/cli.js](../../../node_modules/@llamaindex/liteparse/dist/cli.js) | +430 / -0 |
| 🟢 Added | [node_modules/@llamaindex/liteparse/dist/cli.js.map](../../../node_modules/@llamaindex/liteparse/dist/cli.js.map) | +1 / -0 |
| 🟢 Added | [node_modules/@llamaindex/liteparse/dist/lib.d.ts](../../../node_modules/@llamaindex/liteparse/dist/lib.d.ts) | +610 / -0 |
| 🟢 Added | [node_modules/@llamaindex/liteparse/dist/lib.d.ts.map](../../../node_modules/@llamaindex/liteparse/dist/lib.d.ts.map) | +1 / -0 |
| 🟢 Added | [node_modules/@llamaindex/liteparse/dist/lib.js](../../../node_modules/@llamaindex/liteparse/dist/lib.js) | +347 / -0 |
| 🟢 Added | [node_modules/@llamaindex/liteparse/dist/lib.js.map](../../../node_modules/@llamaindex/liteparse/dist/lib.js.map) | +1 / -0 |
| 🟢 Added | [node_modules/@llamaindex/liteparse/dist/native.d.ts](../../../node_modules/@llamaindex/liteparse/dist/native.d.ts) | +345 / -0 |
| 🟢 Added | [node_modules/@llamaindex/liteparse/dist/native.d.ts.map](../../../node_modules/@llamaindex/liteparse/dist/native.d.ts.map) | +1 / -0 |
| 🟢 Added | [node_modules/@llamaindex/liteparse/dist/native.js](../../../node_modules/@llamaindex/liteparse/dist/native.js) | +71 / -0 |
| 🟢 Added | [node_modules/@llamaindex/liteparse/dist/native.js.map](../../../node_modules/@llamaindex/liteparse/dist/native.js.map) | +1 / -0 |
| 🟢 Added | [node_modules/@llamaindex/liteparse/libpdfium.so](../../../node_modules/@llamaindex/liteparse/libpdfium.so) | - |
| 🟢 Added | [node_modules/@llamaindex/liteparse/liteparse.linux-x64-gnu.node](../../../node_modules/@llamaindex/liteparse/liteparse.linux-x64-gnu.node) | - |
| 🟢 Added | [node_modules/@llamaindex/liteparse/package.json](../../../node_modules/@llamaindex/liteparse/package.json) | +82 / -0 |
| 🟢 Added | [node_modules/commander/LICENSE](../../../node_modules/commander/LICENSE) | +22 / -0 |
| 🟢 Added | [node_modules/commander/Readme.md](../../../node_modules/commander/Readme.md) | +1157 / -0 |
| 🟢 Added | [node_modules/commander/esm.mjs](../../../node_modules/commander/esm.mjs) | +16 / -0 |
| 🟢 Added | [node_modules/commander/index.js](../../../node_modules/commander/index.js) | +24 / -0 |
| 🟢 Added | [node_modules/commander/lib/argument.js](../../../node_modules/commander/lib/argument.js) | +149 / -0 |
| 🟢 Added | [node_modules/commander/lib/command.js](../../../node_modules/commander/lib/command.js) | +2509 / -0 |
| 🟢 Added | [node_modules/commander/lib/error.js](../../../node_modules/commander/lib/error.js) | +39 / -0 |
| 🟢 Added | [node_modules/commander/lib/help.js](../../../node_modules/commander/lib/help.js) | +520 / -0 |
| 🟢 Added | [node_modules/commander/lib/option.js](../../../node_modules/commander/lib/option.js) | +330 / -0 |
| 🟢 Added | [node_modules/commander/lib/suggestSimilar.js](../../../node_modules/commander/lib/suggestSimilar.js) | +101 / -0 |
| 🟢 Added | [node_modules/commander/package-support.json](../../../node_modules/commander/package-support.json) | +16 / -0 |
| 🟢 Added | [node_modules/commander/package.json](../../../node_modules/commander/package.json) | +84 / -0 |
| 🟢 Added | [node_modules/commander/typings/esm.d.mts](../../../node_modules/commander/typings/esm.d.mts) | +3 / -0 |
| 🟢 Added | [node_modules/commander/typings/index.d.ts](../../../node_modules/commander/typings/index.d.ts) | +969 / -0 |
| 🟢 Added | [output/Cigna_ACDF.json](../../../output/Cigna_ACDF.json) | +29021 / -0 |
| 🟢 Added | [output/Cigna_ACDF.md](../../../output/Cigna_ACDF.md) | +957 / -0 |
| 🟢 Added | [output/Cigna_Knee.cleaned_hierarchical.json](../../../output/Cigna_Knee.cleaned_hierarchical.json) | +9207 / -0 |
| 🟢 Added | [output/Cigna_Knee.cleaned_hierarchical.md](../../../output/Cigna_Knee.cleaned_hierarchical.md) | +407 / -0 |
| 🟢 Added | [output/Cigna_Radiation_Oncology.cleaned_hierarchical.json](../../../output/Cigna_Radiation_Oncology.cleaned_hierarchical.json) | +156632 / -0 |
| 🟢 Added | [output/Cigna_Radiation_Oncology.cleaned_hierarchical.md](../../../output/Cigna_Radiation_Oncology.cleaned_hierarchical.md) | +3866 / -0 |
| 🟢 Added | [output/Cigna_Radiation_Oncology_hierarchical.json](../../../output/Cigna_Radiation_Oncology_hierarchical.json) | +188961 / -0 |
| 🟢 Added | [output/Cigna_Radiation_Oncology_hierarchical.md](../../../output/Cigna_Radiation_Oncology_hierarchical.md) | +4653 / -0 |
| 🟢 Added | [output/table.json](../../../output/table.json) | +14025 / -0 |
| 🟢 Added | [output/table_issues.json](../../../output/table_issues.json) | +1153 / -0 |
| 🟢 Added | [package-lock.json](../../../package-lock.json) | +137 / -0 |
| 🟢 Added | [package.json](../../../package.json) | +6 / -0 |
| 🟢 Added | `parser_CLOUDCONVERT.py` | +0 / -0 |
| 🟢 Added | `parser_marker.py` | +61 / -0 |
| 🟢 Added | [pdf_plumber](../../../pdf_plumber) | +34 / -0 |
| 🟢 Added | [requirements.txt](../../../requirements.txt) | +13 / -0 |
| 🟢 Added | [retireval.py](../../../retireval.py) | +129 / -0 |
| 🟢 Added | [retrieval-hierarchical.py](../../../retrieval-hierarchical.py) | +557 / -0 |
| 🟢 Added | `strip_boilerplate.py` | +252 / -0 |
| 🟢 Added | `toc.md` | +5 / -0 |
| 🟢 Added | [tokens-being-used.md](../../../tokens-being-used.md) | +0 / -0 |

</details>

---

<nav>
  <a href="../README.md">All Commits Index</a>
 | <a href="../02_a7b0a69_2nd/README.md">Commit 2 (a7b0a69) &rarr;</a>
</nav>
