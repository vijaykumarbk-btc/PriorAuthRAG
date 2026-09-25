# Commit 7: Lumbar Done

<nav>
  <a href="../06_c963ca5_execution-steps/README.md">&larr; Commit 6 (c963ca5)</a> | 
  <a href="../README.md">All Commits Index</a>
 | <a href="../08_1079351_lab-management-pdf/README.md">Commit 8 (1079351) &rarr;</a>
</nav>

---

## Metadata

| Attribute | Value |
| :--- | :--- |
| **Commit Hash** | `00b1acc` (`00b1accb7fb05db739c537e9c3765486e72a5926`) |
| **Author** | vijaykumarbk <vijaykumarb@boston-technology.com> |
| **Date** | 2026-09-09 12:51:18 +0530 |
| **Files Touched** | **21** (12 added, 8 modified, 1 deleted) |
| **Lines Changed** | **+47662** / **-37** |

## 1. Intent & Purpose

Complete end-to-end production ingestion milestone for Cigna Lumbar Spinal Fusion clinical guideline.

## 2. Key Architectural Decisions (ADR Rationale)

Created isolated `Lumbar/` directory structure with dedicated subdirectories for TOC, BM25, chunks, and embeddings. Formalized evaluation acceptance criteria in `EVALUATION FOR LUMBAR.MD`.

## 3. Cumulative System Capability (State Until This Commit)

> [!NOTE]
> **System State as of `00b1acc`**:
> Lumbar Spinal Fusion is the first fully operational, queryable policy in the system with full hybrid search support.

## 4. What Actually Changed (Functional Breakdown)

- Created `Lumbar/` folder with complete pipeline artifacts: `Lumbar_toc_output.json`, `TOC_tree.txt`, `lumbar_fusion_bm25.pkl` (689 KB).
- Generated 2,912 hierarchical chunks and 5,651 enriched chunks (`Cigna_Lumbar_Fusion_enriched_chunks.json`).
- Generated dense embedding matrix `lumbar_fusion_embeddings.npy` (894 KB) and metadata.
- Added `EVALUATION FOR LUMBAR.MD` establishing benchmark queries.

## 5. Affected Files & Line Diffs

<details>
<summary><b>View all 21 changed files</b> (Click to expand)</summary>

| Status | File Path | Lines (+/-) |
| :--- | :--- | :--- |
| 🟢 Added | [EVALUATION FOR LUMBAR.MD](../../../EVALUATION FOR LUMBAR.MD) | +93 / -0 |
| 🟢 Added | [Lumbar/Cigna_Lumbar_Fusion.pdf](../../../Lumbar/Cigna_Lumbar_Fusion.pdf) | - |
| 🟢 Added | [Lumbar/TOC/Lumbar_toc_output.json](../../../Lumbar/TOC/Lumbar_toc_output.json) | +15811 / -0 |
| 🟢 Added | [Lumbar/TOC/TOC_tree.txt](../../../Lumbar/TOC/TOC_tree.txt) | +59 / -0 |
| 🟢 Added | [Lumbar/bm25/lumbar_fusion_bm25.pkl](../../../Lumbar/bm25/lumbar_fusion_bm25.pkl) | - |
| 🟢 Added | [Lumbar/chunks/Cigna_Lumbar_Fusion_hierarchical_chunks.json](../../../Lumbar/chunks/Cigna_Lumbar_Fusion_hierarchical_chunks.json) | +2912 / -0 |
| 🟢 Added | [Lumbar/embeddings/lumbar_fusion_embeddings.npy](../../../Lumbar/embeddings/lumbar_fusion_embeddings.npy) | - |
| 🟢 Added | [Lumbar/embeddings/lumbar_fusion_metadata.json](../../../Lumbar/embeddings/lumbar_fusion_metadata.json) | +5942 / -0 |
| 🟢 Added | [Lumbar/output-lumbar/Cigna_Lumbar_Fusion_hierarchical.json](../../../Lumbar/output-lumbar/Cigna_Lumbar_Fusion_hierarchical.json) | +15743 / -0 |
| 🟢 Added | [Lumbar/output-lumbar/Cigna_Lumbar_Fusion_hierarchical.md](../../../Lumbar/output-lumbar/Cigna_Lumbar_Fusion_hierarchical.md) | +1084 / -0 |
| 🟢 Added | [Lumbar/toc-mapped-chunks/Cigna_Lumbar_Fusion_enriched_chunks.json](../../../Lumbar/toc-mapped-chunks/Cigna_Lumbar_Fusion_enriched_chunks.json) | +5651 / -0 |
| 🔴 Deleted | `data/raw/Cigna_Lumbar_Fusion.pdf` | - |
| 🟡 Modified | [docling/docling_pdf.py](../../../docling/docling_pdf.py) | +2 / -2 |
| 🟡 Modified | [hierarchical-processing/build_bm25.py](../../../hierarchical-processing/build_bm25.py) | +16 / -4 |
| 🟡 Modified | [hierarchical-processing/chunk_toc_mapper.py](../../../hierarchical-processing/chunk_toc_mapper.py) | +9 / -4 |
| 🟡 Modified | [hierarchical-processing/chunking_heirarchical.py](../../../hierarchical-processing/chunking_heirarchical.py) | +2 / -2 |
| 🟡 Modified | [hierarchical-processing/cpt_table_lookup.py](../../../hierarchical-processing/cpt_table_lookup.py) | +26 / -12 |
| 🟡 Modified | [hierarchical-processing/embedding_with_section.py](../../../hierarchical-processing/embedding_with_section.py) | +9 / -3 |
| 🟡 Modified | [hierarchical-processing/policies_manifest.json](../../../hierarchical-processing/policies_manifest.json) | +4 / -4 |
| 🟡 Modified | [hierarchical-processing/toc_v2.py](../../../hierarchical-processing/toc_v2.py) | +6 / -6 |
| 🟢 Added | `run_lumbar_eval.py` | +293 / -0 |

</details>

---

<nav>
  <a href="../06_c963ca5_execution-steps/README.md">&larr; Commit 6 (c963ca5)</a> | 
  <a href="../README.md">All Commits Index</a>
 | <a href="../08_1079351_lab-management-pdf/README.md">Commit 8 (1079351) &rarr;</a>
</nav>
