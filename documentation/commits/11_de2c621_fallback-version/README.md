# Commit 11: fallback version

<nav>
  <a href="../10_ddb23b3_noocr/README.md">&larr; Commit 10 (ddb23b3)</a> | 
  <a href="../README.md">All Commits Index</a>
 | <a href="../12_c13c799_after-falbback-execution-for-lab/README.md">Commit 12 (c13c799) &rarr;</a>
</nav>

---

## Metadata

| Attribute | Value |
| :--- | :--- |
| **Commit Hash** | `de2c621` (`de2c62179120eb81eca3c0731a1098b7d6ed53f1`) |
| **Author** | vijaykumarbk <vijaykumarb@boston-technology.com> |
| **Date** | 2026-09-17 12:30:59 +0530 |
| **Files Touched** | **12** (12 added, 0 modified, 0 deleted) |
| **Lines Changed** | **+58895** / **-0** |

## 1. Intent & Purpose

Implement a resilient rule-based fallback pipeline to recover from Docling parsing failures on complex tabular guidelines.

## 2. Key Architectural Decisions (ADR Rationale)

Built modular `fallback/` framework (`extractors.py`, `builder.py`, `pipeline.py`, `config.py`, `run_test.py`). Acts as an autonomous fallback when primary parsers misclassify table headers or criteria indentations.

## 3. Cumulative System Capability (State Until This Commit)

> [!NOTE]
> **System State as of `de2c621`**:
> Dual-pipeline resilience: Primary Docling extractor + modular fallback layout builder with automated QA report validation.

## 4. What Actually Changed (Functional Breakdown)

- Created `fallback/` package with layout extraction, hierarchical markdown builder, and QA report generation.
- Validated fallback pipeline against Lumbar policy, producing QA report (`Cigna_Lumbar_Fusion.qa_report.json`).

## 5. Affected Files & Line Diffs

| Status | File Path | Lines (+/-) |
| :--- | :--- | :--- |
| 🟢 Added | [fallback/__init__.py](../../../fallback/__init__.py) | +10 / -0 |
| 🟢 Added | [fallback/builder.py](../../../fallback/builder.py) | +252 / -0 |
| 🟢 Added | [fallback/config.py](../../../fallback/config.py) | +36 / -0 |
| 🟢 Added | [fallback/extractors.py](../../../fallback/extractors.py) | +199 / -0 |
| 🟢 Added | [fallback/pipeline.py](../../../fallback/pipeline.py) | +477 / -0 |
| 🟢 Added | [fallback/run_test.py](../../../fallback/run_test.py) | +80 / -0 |
| 🟢 Added | [fallback/test_results_lumbar/Cigna_Lumbar_Fusion.hierarchical.json](../../../fallback/test_results_lumbar/Cigna_Lumbar_Fusion.hierarchical.json) | +39747 / -0 |
| 🟢 Added | [fallback/test_results_lumbar/Cigna_Lumbar_Fusion.hierarchical.md](../../../fallback/test_results_lumbar/Cigna_Lumbar_Fusion.hierarchical.md) | +1084 / -0 |
| 🟢 Added | [fallback/test_results_lumbar/Cigna_Lumbar_Fusion.qa_report.json](../../../fallback/test_results_lumbar/Cigna_Lumbar_Fusion.qa_report.json) | +17 / -0 |
| 🟢 Added | [fallback/test_results_lumbar_tiered/Cigna_Lumbar_Fusion.hierarchical.json](../../../fallback/test_results_lumbar_tiered/Cigna_Lumbar_Fusion.hierarchical.json) | +15861 / -0 |
| 🟢 Added | [fallback/test_results_lumbar_tiered/Cigna_Lumbar_Fusion.hierarchical.md](../../../fallback/test_results_lumbar_tiered/Cigna_Lumbar_Fusion.hierarchical.md) | +1117 / -0 |
| 🟢 Added | [fallback/test_results_lumbar_tiered/Cigna_Lumbar_Fusion.qa_report.json](../../../fallback/test_results_lumbar_tiered/Cigna_Lumbar_Fusion.qa_report.json) | +15 / -0 |

---

<nav>
  <a href="../10_ddb23b3_noocr/README.md">&larr; Commit 10 (ddb23b3)</a> | 
  <a href="../README.md">All Commits Index</a>
 | <a href="../12_c13c799_after-falbback-execution-for-lab/README.md">Commit 12 (c13c799) &rarr;</a>
</nav>
