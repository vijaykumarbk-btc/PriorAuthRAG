# Commit 14: 5:00 ending commit

<nav>
  <a href="../13_eb6d9dc_fallback-commit/README.md">&larr; Commit 13 (eb6d9dc)</a> | 
  <a href="../README.md">All Commits Index</a>
 | <a href="../15_df5ef5f_same-day-last/README.md">Commit 15 (df5ef5f) &rarr;</a>
</nav>

---

## Metadata

| Attribute | Value |
| :--- | :--- |
| **Commit Hash** | `06638e4` (`06638e406ff0027dc5fc446f6b36b8d60cba8c64`) |
| **Author** | vijaykumarbk <vijaykumarb@boston-technology.com> |
| **Date** | 2026-09-18 16:55:23 +0530 |
| **Files Touched** | **17** (7 added, 10 modified, 0 deleted) |
| **Lines Changed** | **+367133** / **-535** |

## 1. Intent & Purpose

Refine Lab Management TOC tree hierarchy and chunk boundaries; ensure safety with backup files.

## 2. Key Architectural Decisions (ADR Rationale)

Tuned section header boundaries for genetic testing panels. Preserved `.bak` backups of primary JSON outputs for recovery.

## 3. Cumulative System Capability (State Until This Commit)

> [!NOTE]
> **System State as of `06638e4`**:
> Stabilized Lab Management index with higher heading accuracy for genetic testing clauses.

## 4. What Actually Changed (Functional Breakdown)

- Refined Lab Management TOC output and tree mappings.
- Created `Cigna_Lab_Management.hierarchical.json.bak` and `.md.bak` for reproducibility.

## 5. Affected Files & Line Diffs

<details>
<summary><b>View all 17 changed files</b> (Click to expand)</summary>

| Status | File Path | Lines (+/-) |
| :--- | :--- | :--- |
| 🟡 Modified | [Lab_Management/TOC/Lab_Management_toc_output.json](../../../Lab_Management/TOC/Lab_Management_toc_output.json) | +462 / -337 |
| 🟡 Modified | [Lab_Management/TOC/Lab_Management_toc_tree.txt](../../../Lab_Management/TOC/Lab_Management_toc_tree.txt) | +4 / -4 |
| 🟡 Modified | [Lab_Management/bm25/lab_management_bm25.pkl](../../../Lab_Management/bm25/lab_management_bm25.pkl) | - |
| 🟡 Modified | [Lab_Management/chunks/Cigna_Lab_Management.hierarchical_chunks.json](../../../Lab_Management/chunks/Cigna_Lab_Management.hierarchical_chunks.json) | +11 / -11 |
| 🟡 Modified | [Lab_Management/chunks/Cigna_Lab_Management_enriched_chunks.json](../../../Lab_Management/chunks/Cigna_Lab_Management_enriched_chunks.json) | +17 / -17 |
| 🟡 Modified | [Lab_Management/embeddings/lab_management_embeddings.npy](../../../Lab_Management/embeddings/lab_management_embeddings.npy) | - |
| 🟡 Modified | [Lab_Management/embeddings/lab_management_metadata.json](../../../Lab_Management/embeddings/lab_management_metadata.json) | +20 / -20 |
| 🟡 Modified | [Lab_Management/output_tiered/Cigna_Lab_Management.hierarchical.json](../../../Lab_Management/output_tiered/Cigna_Lab_Management.hierarchical.json) | +151 / -130 |
| 🟢 Added | [Lab_Management/output_tiered/Cigna_Lab_Management.hierarchical.json.bak](../../../Lab_Management/output_tiered/Cigna_Lab_Management.hierarchical.json.bak) | +324878 / -0 |
| 🟡 Modified | [Lab_Management/output_tiered/Cigna_Lab_Management.hierarchical.md](../../../Lab_Management/output_tiered/Cigna_Lab_Management.hierarchical.md) | +2 / -2 |
| 🟢 Added | [Lab_Management/output_tiered/Cigna_Lab_Management.hierarchical.md.bak](../../../Lab_Management/output_tiered/Cigna_Lab_Management.hierarchical.md.bak) | +25713 / -0 |
| 🟢 Added | [Lab_Management/output_tiered/Cigna_Lab_Management.qa_report.json.bak](../../../Lab_Management/output_tiered/Cigna_Lab_Management.qa_report.json.bak) | +14 / -0 |
| 🟡 Modified | [fallback/pipeline.py](../../../fallback/pipeline.py) | +17 / -14 |
| 🟢 Added | [test_fallback_acdf/Cigna_ACDF.hierarchical.json](../../../test_fallback_acdf/Cigna_ACDF.hierarchical.json) | +14676 / -0 |
| 🟢 Added | [test_fallback_acdf/Cigna_ACDF.hierarchical.md](../../../test_fallback_acdf/Cigna_ACDF.hierarchical.md) | +1072 / -0 |
| 🟢 Added | [test_fallback_acdf/Cigna_ACDF.qa_report.json](../../../test_fallback_acdf/Cigna_ACDF.qa_report.json) | +21 / -0 |
| 🟢 Added | [test_fallback_acdf/compare_acdf.py](../../../test_fallback_acdf/compare_acdf.py) | +75 / -0 |

</details>

---

<nav>
  <a href="../13_eb6d9dc_fallback-commit/README.md">&larr; Commit 13 (eb6d9dc)</a> | 
  <a href="../README.md">All Commits Index</a>
 | <a href="../15_df5ef5f_same-day-last/README.md">Commit 15 (df5ef5f) &rarr;</a>
</nav>
