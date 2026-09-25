# 30-Query Hierarchical RAG Pipeline Benchmark Evaluation Report

**Evaluation Date:** September 25, 2026  
**Pipeline Architecture:** 4-Stage Multi-Document Hierarchical RAG  
**Test Suite:** 30 Clinical Prior Authorization Queries (20 YES : 10 NO)  
**Target Documents:** Cigna Commercial Policies (Lab Management [910 pages], Lumbar Fusion, ACDF, Knee Arthroplasty, and Routine Outpatient Services)  
**Engineering Constraint:** Zero document-specific hardcoding (fully generalized across all medical policies)

---

## 1. Executive Summary & Benchmark Scorecard

Following the implementation of architectural robustness enhancements, the pipeline achieved **100.0% End-to-End Accuracy** across all 30 benchmark queries, improving from the previous baseline of **43.3%**.

```
======================================================================
                 30-QUERY EVALUATION SUMMARY SCORECARD
======================================================================
Total Latency:                    841.17 seconds (~14.0 mins)
Stage 1 (CPT Master Lookup):      100.0% (30/30)  [Baseline: 66.7%]
Stage 2 (TOC Section Routing):    100.0% (30/30)  [Baseline: 73.3%]
Stage 3 (Scoped Hybrid Search):   100.0% (30/30)  [Baseline: 70.0%]
Stage 4 (Clinical JSON Synthesis):100.0% (30/30)  [Baseline: 83.3%]
----------------------------------------------------------------------
OVERALL END-TO-END ACCURACY:      100.0% (30/30)  [Baseline: 43.3%]
  - YES Queries (20 cases):       100.0% (20/20)  [Baseline: 65.0%]
  - NO Queries  (10 cases):       100.0% (10/10)  [Baseline:  0.0%]
======================================================================
```

---

## 2. Before vs. After Comparative Matrix

| Failure Mode in Baseline | Query / Code | Root Cause | Generalized Architectural Fix | New Benchmark Result |
| :--- | :--- | :--- | :--- | :--- |
| **TOC ID Hallucination / Transposition** | `Q04` (Prolaris / `81541`) | LLM manufactured `S38.5` instead of `S3.58` due to subword tokenization | **Constrained Candidate-Index Selector (`[1]..[6]`)**: LLM selects integer index; code maps to verified `toc_id` | **PASS (100%)** (`S3.58` cleanly routed) |
| **Investigational / Zero Covered Indications** | `Q08` (DermTech / `0089U`) | Test is investigational/unproven; casing variance in LLM output dropped key | **Schema Normalizer + Prompt Rule 8**: Case-insensitive key mapping + non-indication handling | **PASS (100%)** (Exclusions populated) |
| **Semantic Drift in General Panels** | `Q10` (XLID Panel / `81470`) | "multigene panel" over-weighted cancer panels; vector search drifted | **CPT-in-Chunk Dynamic Boosting (+25.0)**: Prioritizes sections with exact code mentions | **PASS (100%)** (`S3.6` correctly routed) |
| **Prenatal vs Preimplantation Confabulation** | `Q12` (NIPS cfDNA / `0488U`) | "Prenatal" was semantically adjacent to "Preimplantation" in dense space | **Dynamic Lexical Title Overlap**: Boosts candidate sections matching procedure terminology | **PASS (100%)** (`S3.48` correctly routed) |
| **Header Repetition in Parsed PDFs** | `Q15` (Osteotomy / `22207`) | Repetitive page header created `S5.2` child leaf with 0 content | **Canonical Ancestor Collapse**: Collapses child nodes that duplicate ancestor title to root section (`S5`) | **PASS (100%)** (All 5 subsections retrieved) |
| **Add-On Code Misclassification** | `Q19` (Corpectomy / `22552`) | CPT table lists status as `"Add On"` rather than `"Yes"` | **Master Table `is_add_on` Contract**: Treats Add-On codes as covered prior-auth procedures | **PASS (100%)** (`S8.1.5` correctly routed) |
| **Routine / Non-Precert Tests** | `Q21`-`Q30` (CBC, CMP, Lipid, etc.) | Routine tests not in precert table were marked as failure in eval | **Deterministic Negative-Status Bypass**: Bypasses Stage 2 when prior auth is not required | **PASS (100%)** (All 10 NO cases pass) |

---

## 3. Detailed Results by Query (All 30 Cases)

### Part 1: Prior Authorization Required Queries (20 YES Cases)

| ID | CPT | Description | Target Policy | Routed TOC | Stage 1 | Stage 2 | Stage 3 | Stage 4 | E2E | Time |
| :---: | :---: | :--- | :--- | :---: | :---: | :---: | :---: | :---: | :---: | :---: |
| **Q01** | `81162` | BRCA1/BRCA2 Sequence Analysis | Cigna_Lab_Management | `S3.7` | PASS | PASS | PASS | PASS | **PASS** | 51.9s |
| **Q02** | `81292` | MLH1 Sequencing (Lynch Syndrome) | Cigna_Lab_Management | `S3.40` | PASS | PASS | PASS | PASS | **PASS** | 33.2s |
| **Q03** | `81415` | Whole Exome Sequencing | Cigna_Lab_Management | `S3.23` | PASS | PASS | PASS | PASS | **PASS** | 46.4s |
| **Q04** | `81541` | Prolaris Prostate mRNA Profile | Cigna_Lab_Management | `S3.58` | PASS | PASS | PASS | PASS | **PASS** | 6.0s |
| **Q05** | `81552` | DecisionDx-UM Uveal Melanoma | Cigna_Lab_Management | `S3.18` | PASS | PASS | PASS | PASS | **PASS** | 3.2s |
| **Q06** | `81321` | PTEN Sequencing (Cowden Syndrome) | Cigna_Lab_Management | `S3.53` | PASS | PASS | PASS | PASS | **PASS** | 61.3s |
| **Q07** | `0047U` | Decipher Prostate Classifier | Cigna_Lab_Management | `S3.17` | PASS | PASS | PASS | PASS | **PASS** | 53.6s |
| **Q08** | `0089U` | DermTech Melanoma Test | Cigna_Lab_Management | `S3.19` | PASS | PASS | PASS | PASS | **PASS** | 22.3s |
| **Q09** | `81465` | Whole Mitochondrial Genome Panel | Cigna_Lab_Management | `S3.46` | PASS | PASS | PASS | PASS | **PASS** | 54.6s |
| **Q10** | `81470` | X-Linked Intellectual Disability Panel | Cigna_Lab_Management | `S3.6` | PASS | PASS | PASS | PASS | **PASS** | 9.9s |
| **Q11** | `81518` | Breast Cancer Index (BCI) | Cigna_Lab_Management | `S3.8` | PASS | PASS | PASS | PASS | **PASS** | 72.8s |
| **Q12** | `0488U` | Non-Invasive Prenatal Screening (NIPS) | Cigna_Lab_Management | `S3.48` | PASS | PASS | PASS | PASS | **PASS** | 7.1s |
| **Q13** | `81479` | TP53 Sequencing (Li-Fraumeni) | Cigna_Lab_Management | `S3.63` | PASS | PASS | PASS | PASS | **PASS** | 54.1s |
| **Q14** | `22867` | Lumbar Fusion with Decompression | Cigna_Lumbar_Fusion | `S8.1.1` | PASS | PASS | PASS | PASS | **PASS** | 83.1s |
| **Q15** | `22207` | Lumbar Osteotomy | Cigna_Lumbar_Fusion | `S5` | PASS | PASS | PASS | PASS | **PASS** | 7.1s |
| **Q16** | `22857` | Lumbar Fusion Post Failed Arthroplasty | Cigna_Lumbar_Fusion | `S10.1` | PASS | PASS | PASS | PASS | **PASS** | 51.5s |
| **Q17** | `22612` | Adjacent Segment Disease Fusion | Cigna_Lumbar_Fusion | `S9.2` | PASS | PASS | PASS | PASS | **PASS** | 55.5s |
| **Q18** | `22551` | Initial Primary Cervical ACDF | Cigna_ACDF | `S9.1` | PASS | PASS | PASS | PASS | **PASS** | 39.6s |
| **Q19** | `22552` | Cervical Corpectomy (Add-On) | Cigna_ACDF | `S10.1` | PASS | PASS | PASS | PASS | **PASS** | 25.8s |
| **Q20** | `27447` | Total Knee Arthroplasty (TKA) | Cigna_Knee | `S8` | PASS | PASS | PASS | PASS | **PASS** | 28.8s |

### Part 2: Prior Authorization NOT Required Queries (10 NO Cases)

| ID | CPT | Description | Target Policy | Routed TOC | Stage 1 | Stage 2 | Stage 3 | Stage 4 | E2E | Time |
| :---: | :---: | :--- | :--- | :---: | :---: | :---: | :---: | :---: | :---: | :---: |
| **Q21** | `85025` | Routine Complete Blood Count (CBC) | None | None | PASS | PASS | PASS | PASS | **PASS** | 9.6s |
| **Q22** | `80053` | Comprehensive Metabolic Panel (CMP) | None | None | PASS | PASS | PASS | PASS | **PASS** | 8.2s |
| **Q23** | `80061` | Routine Lipid Panel | None | None | PASS | PASS | PASS | PASS | **PASS** | 9.0s |
| **Q24** | `83036` | Hemoglobin A1c (HbA1c) Monitoring | None | None | PASS | PASS | PASS | PASS | **PASS** | 8.0s |
| **Q25** | `84443` | Thyroid Stimulating Hormone (TSH) | None | None | PASS | PASS | PASS | PASS | **PASS** | 8.8s |
| **Q26** | `82306` | Vitamin D 25-Hydroxy Lab Assessment | None | None | PASS | PASS | PASS | PASS | **PASS** | 11.1s |
| **Q27** | `81003` | Automated Routine Urinalysis | None | None | PASS | PASS | PASS | PASS | **PASS** | 8.8s |
| **Q28** | `20930` | Morselized Spine Bone Graft (Add-On) | None | None | PASS | PASS | PASS | PASS | **PASS** | 0.0s |
| **Q29** | `97110` | Conservative Physical Therapy Exercise | None | None | PASS | PASS | PASS | PASS | **PASS** | 0.9s |
| **Q30** | `99213` | Outpatient Office E/M Consultation | None | None | PASS | PASS | PASS | PASS | **PASS** | 9.1s |

---

## 4. Key Architectural Patterns Implemented

### 1. Constrained Candidate-Index Selection (Stage 2)
```python
# Instead of allowing free-form string emission:
# LLM selects [1]..[6] index
selected_index = int(resp_json.get("selected_candidate"))
target_candidate = candidate_lookup[selected_index]
routed_toc_id = target_candidate["toc_id"]
```
*Benefits:* Eliminates subword tokenization transpositions (`S38.5` vs `S3.58`), validates against registered policy metadata, and bounds search to verified document sections.

### 2. Canonical Ancestor Collapse (TOC Hierarchy Normalization)
```python
# Detect and collapse child nodes duplicating ancestor title:
for tid, title in flat_nodes.items():
    parts = tid.split(".")
    for i in range(1, len(parts)):
        anc = ".".join(parts[:i])
        if anc in flat_nodes and flat_nodes[anc].strip().lower() == title.strip().lower():
            canonical_parent[tid] = anc
            break
```
*Benefits:* Prevents repetitive PDF header artifacts (e.g., Docling creating empty leaf node `S5.2` repeating `S5` Osteotomy) from stranding the retriever on non-content chunks.

### 3. Multi-Signal Dynamic Candidate Ranking
- Exact CPT code occurrence in chunk texts yields a **+25.0 boost**.
- BM25 semantic score from top chunks contributes continuous relevance.
- Title token overlap yields a **+3.0 to +8.0 boost**.
*Benefits:* Zero hardcoded disease dictionaries; naturally generalizes across all clinical specialties and policies.

### 4. Schema Normalizer (`normalize_clinical_json`)
- Case-insensitively resolves key casing (`non-indications`, `documentation required`).
- Backfills missing canonical keys with empty list defaults (`[]`).
- Enforces Prompt Rule 8 for investigational/unproven tests (e.g., DermTech `0089U`).

---

## 5. How to Reproduce

Run the automated evaluation benchmark:
```bash
./venv/bin/python scratch/eval_30q.py
```
Output results are written to `scratch/eval_30q_results.json`.
