# Commit 2: 2nd

<nav>
  <a href="../01_5d00445_copy-project/README.md">&larr; Commit 1 (5d00445)</a> | 
  <a href="../README.md">All Commits Index</a>
 | <a href="../03_9c6bc65_working/README.md">Commit 3 (9c6bc65) &rarr;</a>
</nav>

---

## Metadata

| Attribute | Value |
| :--- | :--- |
| **Commit Hash** | `a7b0a69` (`a7b0a69cc1be93d412fcda05570e407c0412f2b5`) |
| **Author** | vijaykumarbk <vijaykumarb@boston-technology.com> |
| **Date** | 2026-09-08 10:49:04 +0530 |
| **Files Touched** | **2** (0 added, 2 modified, 0 deleted) |
| **Lines Changed** | **+27** / **-40** |

## 1. Intent & Purpose

Fix runtime import paths and path resolution for standalone retrieval scripts.

## 2. Key Architectural Decisions (ADR Rationale)

Standardized import hierarchy between `retrieval-hierarchical.py` and `hierarchical-processing/retrieve.py` so retrieval CLI scripts can be invoked from the repository root without ModuleNotFoundError.

## 3. Cumulative System Capability (State Until This Commit)

> [!NOTE]
> **System State as of `a7b0a69`**:
> Standalone CLI retrieval scripts can be invoked from the terminal against early prototype embeddings without crashing on import errors.

## 4. What Actually Changed (Functional Breakdown)

- Fixed relative sys.path resolution in `retrieval-hierarchical.py`.
- Aligned argument parsing in `hierarchical-processing/retrieve.py` with root execution expectations.

## 5. Affected Files & Line Diffs

| Status | File Path | Lines (+/-) |
| :--- | :--- | :--- |
| 🟡 Modified | [hierarchical-processing/chunk_toc_mapper.py](../../../hierarchical-processing/chunk_toc_mapper.py) | +12 / -3 |
| 🟡 Modified | [hierarchical-processing/retrieve.py](../../../hierarchical-processing/retrieve.py) | +15 / -37 |

---

<nav>
  <a href="../01_5d00445_copy-project/README.md">&larr; Commit 1 (5d00445)</a> | 
  <a href="../README.md">All Commits Index</a>
 | <a href="../03_9c6bc65_working/README.md">Commit 3 (9c6bc65) &rarr;</a>
</nav>
