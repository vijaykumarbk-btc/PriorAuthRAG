# Commit 3: working-

<nav>
  <a href="../02_a7b0a69_2nd/README.md">&larr; Commit 2 (a7b0a69)</a> | 
  <a href="../README.md">All Commits Index</a>
 | <a href="../04_0c3d41e_removed-unnecessary-files/README.md">Commit 4 (0c3d41e) &rarr;</a>
</nav>

---

## Metadata

| Attribute | Value |
| :--- | :--- |
| **Commit Hash** | `9c6bc65` (`9c6bc65394479355f0c34d1203159fb5fe071456`) |
| **Author** | vijaykumarbk <vijaykumarb@boston-technology.com> |
| **Date** | 2026-09-08 11:42:24 +0530 |
| **Files Touched** | **6** (0 added, 6 modified, 0 deleted) |
| **Lines Changed** | **+4854** / **-3131** |

## 1. Intent & Purpose

Overhaul chunk-to-TOC hierarchy mapping to prevent isolated chunks from losing their parent medical policy headings.

## 2. Key Architectural Decisions (ADR Rationale)

Introduced the Enriched Chunk Schema (`*_enriched_chunks.json`). Each chunk now stores `section_path`, `heading_hierarchy`, `policy_id`, and `cpt_codes` alongside raw text so parent context is never lost during retrieval.

## 3. Cumulative System Capability (State Until This Commit)

> [!NOTE]
> **System State as of `9c6bc65`**:
> ACDF and Lumbar chunks now retain parent headings and ancestry breadcrumbs. Retrieval can inspect parent section context for improved medical necessity matching.

## 4. What Actually Changed (Functional Breakdown)

- Overhauled `hierarchical-processing/chunk_toc_mapper.py` to associate chunks with Table of Contents heading nodes.
- Generated enriched chunks for ACDF (`Cigna_ACDF_enriched_chunks.json`) and Lumbar Fusion (`Cigna_Lumbar_Fusion_enriched_chunks.json`).
- Documented pipeline edge cases and section mapping anomalies in `issues.md`.

## 5. Affected Files & Line Diffs

| Status | File Path | Lines (+/-) |
| :--- | :--- | :--- |
| 🟡 Modified | [hierarchical-processing/Cigna_ACDF_enriched_chunks.json](../../../hierarchical-processing/Cigna_ACDF_enriched_chunks.json) | +711 / -507 |
| 🟡 Modified | [hierarchical-processing/Cigna_Lumbar_Fusion_enriched_chunks.json](../../../hierarchical-processing/Cigna_Lumbar_Fusion_enriched_chunks.json) | +1513 / -887 |
| 🟡 Modified | [hierarchical-processing/acdf_metadata.json](../../../hierarchical-processing/acdf_metadata.json) | +711 / -507 |
| 🟡 Modified | [hierarchical-processing/chunk_toc_mapper.py](../../../hierarchical-processing/chunk_toc_mapper.py) | +37 / -31 |
| 🟡 Modified | [hierarchical-processing/md/embeddings/lumbar_fusion_metadata.json](../../../hierarchical-processing/md/embeddings/lumbar_fusion_metadata.json) | +1513 / -887 |
| 🟡 Modified | `issues.md` | +369 / -312 |

---

<nav>
  <a href="../02_a7b0a69_2nd/README.md">&larr; Commit 2 (a7b0a69)</a> | 
  <a href="../README.md">All Commits Index</a>
 | <a href="../04_0c3d41e_removed-unnecessary-files/README.md">Commit 4 (0c3d41e) &rarr;</a>
</nav>
