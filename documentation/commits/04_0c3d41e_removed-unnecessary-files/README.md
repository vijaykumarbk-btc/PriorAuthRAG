# Commit 4: removed unnecessary files

<nav>
  <a href="../03_9c6bc65_working/README.md">&larr; Commit 3 (9c6bc65)</a> | 
  <a href="../README.md">All Commits Index</a>
 | <a href="../05_5bf450b_idk/README.md">Commit 5 (5bf450b) &rarr;</a>
</nav>

---

## Metadata

| Attribute | Value |
| :--- | :--- |
| **Commit Hash** | `0c3d41e` (`0c3d41e59b504832aa220fd731307700e7516fa2`) |
| **Author** | vijaykumarbk <vijaykumarb@boston-technology.com> |
| **Date** | 2026-09-08 11:55:54 +0530 |
| **Files Touched** | **11** (0 added, 1 modified, 10 deleted) |
| **Lines Changed** | **+136** / **-790726** |

## 1. Intent & Purpose

Major repository hygiene and architecture cleanup. Removed over 746,000 lines of stale monolithic JSON files and obsolete scripts.

## 2. Key Architectural Decisions (ADR Rationale)

Abandoned single giant JSON stores in favor of modular, per-policy serialized numpy matrices (`*.npy`) and metadata JSONs. Pruned unmaintained OCR/parser prototypes (`LiteParse.py`, `check.py`, `hypothermia_checking.py`).

## 3. Cumulative System Capability (State Until This Commit)

> [!NOTE]
> **System State as of `0c3d41e`**:
> Repository size reduced drastically; clean architecture documented in `architecture.md` with modular directory expectations.

## 4. What Actually Changed (Functional Breakdown)

- Deleted legacy monolithic dumps: `embeddings_json.json` (746K lines), `Cigna_ACDF_embeddings.json` (43K lines), `SPECIAL OUT.json`.
- Removed obsolete scripts `LiteParse.py`, `check.py`, `hypothermia_checking.py`.
- Rewrote `architecture.md` to reflect true multi-tier hierarchical retrieval flow.

## 5. Affected Files & Line Diffs

| Status | File Path | Lines (+/-) |
| :--- | :--- | :--- |
| 🔴 Deleted | `Cigna_ACDF_embeddings.json` | +0 / -43012 |
| 🔴 Deleted | `LiteParse.py` | +0 / -53 |
| 🔴 Deleted | `SPECIAL OUT.json` | +0 / -36 |
| 🔴 Deleted | `SPECIAL_OUT.json` | +0 / -36 |
| 🟡 Modified | [architecture.md](../../../architecture.md) | +136 / -97 |
| 🔴 Deleted | `check.py` | +0 / -9 |
| 🔴 Deleted | `embeddings_json.json` | +0 / -746868 |
| 🔴 Deleted | `hypothermia_checking.py` | +0 / -44 |
| 🔴 Deleted | `issues.md` | +0 / -566 |
| 🔴 Deleted | `parser_CLOUDCONVERT.py` | +0 / -0 |
| 🔴 Deleted | `toc.md` | +0 / -5 |

---

<nav>
  <a href="../03_9c6bc65_working/README.md">&larr; Commit 3 (9c6bc65)</a> | 
  <a href="../README.md">All Commits Index</a>
 | <a href="../05_5bf450b_idk/README.md">Commit 5 (5bf450b) &rarr;</a>
</nav>
