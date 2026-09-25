# Commit 10: noocr

<nav>
  <a href="../09_214a6d4_no-change/README.md">&larr; Commit 9 (214a6d4)</a> | 
  <a href="../README.md">All Commits Index</a>
 | <a href="../11_de2c621_fallback-version/README.md">Commit 11 (de2c621) &rarr;</a>
</nav>

---

## Metadata

| Attribute | Value |
| :--- | :--- |
| **Commit Hash** | `ddb23b3` (`ddb23b31d1ae842717d629fd4fb408e896a08084`) |
| **Author** | vijaykumarbk <vijaykumarb@boston-technology.com> |
| **Date** | 2026-09-15 17:25:21 +0530 |
| **Files Touched** | **12** (3 added, 3 modified, 6 deleted) |
| **Lines Changed** | **+978** / **-892** |

## 1. Intent & Purpose

Solve OCR execution bottlenecks on large clinical guidelines by building a non-OCR direct layout extractor.

## 2. Key Architectural Decisions (ADR Rationale)

Created `docling_pdf_no_ocr.py` (741 lines). Bypassed pixel OCR in favor of parsing native PDF font streams and bounding boxes directly, cutting ingestion time by over 80%.

## 3. Cumulative System Capability (State Until This Commit)

> [!NOTE]
> **System State as of `ddb23b3`**:
> High-speed non-OCR PDF parsing engine capable of processing hundreds of pages without memory leaks or OCR timeouts.

## 4. What Actually Changed (Functional Breakdown)

- Implemented `docling/docling_pdf_no_ocr.py` (741 lines).
- Added initial automated benchmark results in `data/benchmark_results.json`.
- Cleaned up unneeded packages and updated `requirements.txt`.

## 5. Affected Files & Line Diffs

| Status | File Path | Lines (+/-) |
| :--- | :--- | :--- |
| 🟡 Modified | [.env.example](../../../.env.example) | +1 / -0 |
| 🟡 Modified | [.gitignore](../../../.gitignore) | +3 / -6 |
| 🔴 Deleted | `check_embeddings.py` | +0 / -6 |
| 🔴 Deleted | `chunking_langchain.py` | +0 / -17 |
| 🟢 Added | [data/benchmark_results.json](../../../data/benchmark_results.json) | +173 / -0 |
| 🟢 Added | [docling/docling_pdf_no_ocr.py](../../../docling/docling_pdf_no_ocr.py) | +741 / -0 |
| 🔴 Deleted | `evaluate_benchmark.py` | +0 / -244 |
| 🔴 Deleted | `parser_marker.py` | +0 / -61 |
| 🟡 Modified | [requirements.txt](../../../requirements.txt) | +30 / -13 |
| 🟢 Added | [requirements2.txt](../../../requirements2.txt) | +30 / -0 |
| 🔴 Deleted | `run_lumbar_eval.py` | +0 / -293 |
| 🔴 Deleted | `strip_boilerplate.py` | +0 / -252 |

---

<nav>
  <a href="../09_214a6d4_no-change/README.md">&larr; Commit 9 (214a6d4)</a> | 
  <a href="../README.md">All Commits Index</a>
 | <a href="../11_de2c621_fallback-version/README.md">Commit 11 (de2c621) &rarr;</a>
</nav>
