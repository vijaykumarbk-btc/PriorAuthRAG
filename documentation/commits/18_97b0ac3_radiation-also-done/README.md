# Commit 18: Radiation also Done

<nav>
  <a href="../17_ae27c3d_sept22/README.md">&larr; Commit 17 (ae27c3d)</a> | 
  <a href="../README.md">All Commits Index</a>
 | <a href="../19_ccb759a_graphified/README.md">Commit 19 (ccb759a) &rarr;</a>
</nav>

---

## Metadata

| Attribute | Value |
| :--- | :--- |
| **Commit Hash** | `97b0ac3` (`97b0ac35ecb3d1aa1e1a6971f44722ab78f2bd3c`) |
| **Author** | vijaykumarbk <vijaykumarb@boston-technology.com> |
| **Date** | 2026-09-24 11:45:54 +0530 |
| **Files Touched** | **13** (11 added, 2 modified, 0 deleted) |
| **Lines Changed** | **+264962** / **-1** |

## 1. Intent & Purpose

Complete end-to-end ingestion and indexing milestone for Cigna Radiation Oncology guideline.

## 2. Key Architectural Decisions (ADR Rationale)

Created isolated `Radiation/` directory structure with TOC, BM25, chunks, embeddings, and QA report, mirroring Lumbar and Lab Management.

## 3. Cumulative System Capability (State Until This Commit)

> [!NOTE]
> **System State as of `97b0ac3`**:
> Four clinical guidelines fully operational: Lumbar Spinal Fusion, Lab Management, Knee, and Radiation Oncology.

## 4. What Actually Changed (Functional Breakdown)

- Ingested `Radiation/raw/Cigna_Radiation_Oncology.pdf` (1.39 MB).
- Generated 2,742 hierarchical chunks and 5,136 enriched chunks.
- Built serialized BM25 index `Cigna_Radiation_Oncology_bm25.pkl` (1.8 MB) and embeddings `Cigna_Radiation_Oncology_embeddings.npy` (841 KB).

## 5. Affected Files & Line Diffs

<details>
<summary><b>View all 13 changed files</b> (Click to expand)</summary>

| Status | File Path | Lines (+/-) |
| :--- | :--- | :--- |
| 🟢 Added | [Radiation/bm25/Cigna_Radiation_Oncology_bm25.pkl](../../../Radiation/bm25/Cigna_Radiation_Oncology_bm25.pkl) | - |
| 🟢 Added | [Radiation/chunks/Cigna_Radiation_Oncology.hierarchical_chunks.json](../../../Radiation/chunks/Cigna_Radiation_Oncology.hierarchical_chunks.json) | +2742 / -0 |
| 🟢 Added | [Radiation/chunks/Cigna_Radiation_Oncology_enriched_chunks.json](../../../Radiation/chunks/Cigna_Radiation_Oncology_enriched_chunks.json) | +5136 / -0 |
| 🟢 Added | [Radiation/embeddings/Cigna_Radiation_Oncology_embeddings.npy](../../../Radiation/embeddings/Cigna_Radiation_Oncology_embeddings.npy) | - |
| 🟢 Added | [Radiation/embeddings/Cigna_Radiation_Oncology_metadata.json](../../../Radiation/embeddings/Cigna_Radiation_Oncology_metadata.json) | +5410 / -0 |
| 🟢 Added | [Radiation/output/Cigna_Radiation_Oncology.hierarchical.json](../../../Radiation/output/Cigna_Radiation_Oncology.hierarchical.json) | +111665 / -0 |
| 🟢 Added | [Radiation/output/Cigna_Radiation_Oncology.hierarchical.md](../../../Radiation/output/Cigna_Radiation_Oncology.hierarchical.md) | +8795 / -0 |
| 🟢 Added | [Radiation/output/Cigna_Radiation_Oncology.qa_report.json](../../../Radiation/output/Cigna_Radiation_Oncology.qa_report.json) | +27 / -0 |
| 🟢 Added | [Radiation/raw/Cigna_Radiation_Oncology.pdf](../../../Radiation/raw/Cigna_Radiation_Oncology.pdf) | - |
| 🟢 Added | [Radiation/toc/Cigna_Radiation_Oncology_toc_output.json](../../../Radiation/toc/Cigna_Radiation_Oncology_toc_output.json) | +131027 / -0 |
| 🟢 Added | [Radiation/toc/Cigna_Radiation_Oncology_toc_tree.txt](../../../Radiation/toc/Cigna_Radiation_Oncology_toc_tree.txt) | +144 / -0 |
| 🟡 Modified | [hierarchical-processing/policies_manifest.json](../../../hierarchical-processing/policies_manifest.json) | +8 / -0 |
| 🟡 Modified | [hierarchical-processing/policies_manifest.json.bak](../../../hierarchical-processing/policies_manifest.json.bak) | +8 / -1 |

</details>

---

<nav>
  <a href="../17_ae27c3d_sept22/README.md">&larr; Commit 17 (ae27c3d)</a> | 
  <a href="../README.md">All Commits Index</a>
 | <a href="../19_ccb759a_graphified/README.md">Commit 19 (ccb759a) &rarr;</a>
</nav>
