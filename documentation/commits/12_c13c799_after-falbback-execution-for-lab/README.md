# Commit 12: after falbback execution for lab

<nav>
  <a href="../11_de2c621_fallback-version/README.md">&larr; Commit 11 (de2c621)</a> | 
  <a href="../README.md">All Commits Index</a>
 | <a href="../13_eb6d9dc_fallback-commit/README.md">Commit 13 (eb6d9dc) &rarr;</a>
</nav>

---

## Metadata

| Attribute | Value |
| :--- | :--- |
| **Commit Hash** | `c13c799` (`c13c799eae8cb73cab3218f10822c568d6ea636e`) |
| **Author** | vijaykumarbk <vijaykumarb@boston-technology.com> |
| **Date** | 2026-09-17 14:57:28 +0530 |
| **Files Touched** | **18** (12 added, 6 modified, 0 deleted) |
| **Lines Changed** | **+776459** / **-44** |

## 1. Intent & Purpose

Execute full end-to-end extraction and indexing of the 400+ page Cigna Lab Management policy using the fallback pipeline.

## 2. Key Architectural Decisions (ADR Rationale)

Processed entire Lab Management guideline into 378K lines of TOC output, 482-node TOC tree, 9,212 hierarchical chunks, 17,222 enriched chunks, BM25 index (3.9 MB), and embedding matrix (2.8 MB).

## 3. Cumulative System Capability (State Until This Commit)

> [!NOTE]
> **System State as of `c13c799`**:
> Two major guidelines fully operational and queryable: Lumbar Spinal Fusion and Clinical Lab Management.

## 4. What Actually Changed (Functional Breakdown)

- Generated `Lab_Management/TOC/Lab_Management_toc_output.json` (378K lines) and `Lab_Management_toc_tree.txt` (482 lines).
- Generated 9,212 hierarchical chunks and 17,222 enriched chunks for Lab Management.
- Built serialized BM25 index `Lab_Management/bm25/lab_management_bm25.pkl` (3.9 MB) and embeddings `lab_management_embeddings.npy` (2.8 MB).

## 5. Affected Files & Line Diffs

<details>
<summary><b>View all 18 changed files</b> (Click to expand)</summary>

| Status | File Path | Lines (+/-) |
| :--- | :--- | :--- |
| 🟢 Added | [Lab_Management/TOC/Lab_Management_toc_output.json](../../../Lab_Management/TOC/Lab_Management_toc_output.json) | +378588 / -0 |
| 🟢 Added | [Lab_Management/TOC/Lab_Management_toc_tree.txt](../../../Lab_Management/TOC/Lab_Management_toc_tree.txt) | +482 / -0 |
| 🟢 Added | [Lab_Management/bm25/lab_management_bm25.pkl](../../../Lab_Management/bm25/lab_management_bm25.pkl) | - |
| 🟢 Added | [Lab_Management/chunks/Cigna_Lab_Management.hierarchical_chunks.json](../../../Lab_Management/chunks/Cigna_Lab_Management.hierarchical_chunks.json) | +9212 / -0 |
| 🟢 Added | [Lab_Management/chunks/Cigna_Lab_Management_enriched_chunks.json](../../../Lab_Management/chunks/Cigna_Lab_Management_enriched_chunks.json) | +17222 / -0 |
| 🟢 Added | [Lab_Management/embeddings/lab_management_embeddings.npy](../../../Lab_Management/embeddings/lab_management_embeddings.npy) | - |
| 🟢 Added | [Lab_Management/embeddings/lab_management_metadata.json](../../../Lab_Management/embeddings/lab_management_metadata.json) | +18143 / -0 |
| 🟢 Added | [Lab_Management/output_tiered/Cigna_Lab_Management.hierarchical.json](../../../Lab_Management/output_tiered/Cigna_Lab_Management.hierarchical.json) | +324878 / -0 |
| 🟢 Added | [Lab_Management/output_tiered/Cigna_Lab_Management.hierarchical.md](../../../Lab_Management/output_tiered/Cigna_Lab_Management.hierarchical.md) | +25713 / -0 |
| 🟢 Added | [Lab_Management/output_tiered/Cigna_Lab_Management.qa_report.json](../../../Lab_Management/output_tiered/Cigna_Lab_Management.qa_report.json) | +14 / -0 |
| 🟢 Added | [data/benchmark_results_lab_management_20q.json](../../../data/benchmark_results_lab_management_20q.json) | +1581 / -0 |
| 🟢 Added | [eval_lab_management_benchmark.py](../../../eval_lab_management_benchmark.py) | +486 / -0 |
| 🟡 Modified | [hierarchical-processing/chunking_heirarchical.py](../../../hierarchical-processing/chunking_heirarchical.py) | +2 / -2 |
| 🟡 Modified | [hierarchical-processing/cpt_table_lookup.py](../../../hierarchical-processing/cpt_table_lookup.py) | +1 / -1 |
| 🟡 Modified | [hierarchical-processing/document_registry.py](../../../hierarchical-processing/document_registry.py) | +33 / -33 |
| 🟡 Modified | [hierarchical-processing/policies_manifest.json](../../../hierarchical-processing/policies_manifest.json) | +8 / -0 |
| 🟡 Modified | [hybrid_search_hierarchical.py](../../../hybrid_search_hierarchical.py) | +4 / -0 |
| 🟡 Modified | [retrieval-hierarchical.py](../../../retrieval-hierarchical.py) | +92 / -8 |

</details>

---

<nav>
  <a href="../11_de2c621_fallback-version/README.md">&larr; Commit 11 (de2c621)</a> | 
  <a href="../README.md">All Commits Index</a>
 | <a href="../13_eb6d9dc_fallback-commit/README.md">Commit 13 (eb6d9dc) &rarr;</a>
</nav>
