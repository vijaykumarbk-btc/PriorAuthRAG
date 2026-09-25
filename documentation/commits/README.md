# Commits Evolution Documentation Index

**Project**: `PriorAuthRAG`  
**Total Commits Analyzed**: 20  
**Timeline**: 2026-09-08 to 2026-09-24  

Each commit below has its own dedicated folder containing **intent**, **architectural decisions (ADR rationale)**, **cumulative system capability up to that point**, and **detailed file diffs**.

| # | Hash | Date | Commit Message | Cumulative System Capability | Folder |
| :-: | :--- | :--- | :--- | :--- | :--- |
| 1 | `5d00445` | 2026-09-08 | copy project | The project can ingest initial PDF policies (Cigna ACDF, Lumbar) and execute prototyp... | [📂 01_5d00445_copy-project/](./01_5d00445_copy-project/README.md) |
| 2 | `a7b0a69` | 2026-09-08 | 2nd | Standalone CLI retrieval scripts can be invoked from the terminal against early proto... | [📂 02_a7b0a69_2nd/](./02_a7b0a69_2nd/README.md) |
| 3 | `9c6bc65` | 2026-09-08 | working- | ACDF and Lumbar chunks now retain parent headings and ancestry breadcrumbs. Retrieval... | [📂 03_9c6bc65_working/](./03_9c6bc65_working/README.md) |
| 4 | `0c3d41e` | 2026-09-08 | removed unnecessary files | Repository size reduced drastically; clean architecture documented in `architecture.m... | [📂 04_0c3d41e_removed-unnecessary-files/](./04_0c3d41e_removed-unnecessary-files/README.md) |
| 5 | `5bf450b` | 2026-09-08 | idk | Automated script to convert chunk trees into standardized JSON manifests with token t... | [📂 05_5bf450b_idk/](./05_5bf450b_idk/README.md) |
| 6 | `c963ca5` | 2026-09-08 | execution-steps | Standardized developer runbook allowing team members to ingest new clinical guideline... | [📂 06_c963ca5_execution-steps/](./06_c963ca5_execution-steps/README.md) |
| 7 | `00b1acc` | 2026-09-09 | Lumbar Done | Lumbar Spinal Fusion is the first fully operational, queryable policy in the system w... | [📂 07_00b1acc_lumbar-done/](./07_00b1acc_lumbar-done/README.md) |
| 8 | `1079351` | 2026-09-11 | lab-management-pdf | System has 1 completed policy (Lumbar) and formal architecture blueprint for scaling ... | [📂 08_1079351_lab-management-pdf/](./08_1079351_lab-management-pdf/README.md) |
| 9 | `214a6d4` | 2026-09-11 | no change | Raw `Cigna_Lab_Management.pdf` committed into `Lab_Management/raw/`; workspace saniti... | [📂 09_214a6d4_no-change/](./09_214a6d4_no-change/README.md) |
| 10 | `ddb23b3` | 2026-09-15 | noocr | High-speed non-OCR PDF parsing engine capable of processing hundreds of pages without... | [📂 10_ddb23b3_noocr/](./10_ddb23b3_noocr/README.md) |
| 11 | `de2c621` | 2026-09-17 | fallback version | Dual-pipeline resilience: Primary Docling extractor + modular fallback layout builder... | [📂 11_de2c621_fallback-version/](./11_de2c621_fallback-version/README.md) |
| 12 | `c13c799` | 2026-09-17 | after falbback execution for lab | Two major guidelines fully operational and queryable: Lumbar Spinal Fusion and Clinic... | [📂 12_c13c799_after-falbback-execution-for-lab/](./12_c13c799_after-falbback-execution-for-lab/README.md) |
| 13 | `eb6d9dc` | 2026-09-18 | fallback commit | Three guidelines fully indexed (Lumbar, Lab Management, Knee). Automated policy inges... | [📂 13_eb6d9dc_fallback-commit/](./13_eb6d9dc_fallback-commit/README.md) |
| 14 | `06638e4` | 2026-09-18 | 5:00 ending commit | Stabilized Lab Management index with higher heading accuracy for genetic testing clau... | [📂 14_06638e4_5-00-ending-commit/](./14_06638e4_5-00-ending-commit/README.md) |
| 15 | `df5ef5f` | 2026-09-18 | Same day last | Technical decisions and edge-case rationale documented for team reference.... | [📂 15_df5ef5f_same-day-last/](./15_df5ef5f_same-day-last/README.md) |
| 16 | `5b3c2e0` | 2026-09-22 | 22Sept | Hybrid retrieval engine now cross-references procedural CPT/HCPCS codes and scores pr... | [📂 16_5b3c2e0_22sept/](./16_5b3c2e0_22sept/README.md) |
| 17 | `ae27c3d` | 2026-09-22 | sept22 | Production-clean retrieval CLI with quiet execution and structured JSON return suppor... | [📂 17_ae27c3d_sept22/](./17_ae27c3d_sept22/README.md) |
| 18 | `97b0ac3` | 2026-09-24 | Radiation also Done | Four clinical guidelines fully operational: Lumbar Spinal Fusion, Lab Management, Kne... | [📂 18_97b0ac3_radiation-also-done/](./18_97b0ac3_radiation-also-done/README.md) |
| 19 | `ccb759a` | 2026-09-24 | graphified | Dual knowledge representation: RAG chunk store + cross-guideline entity knowledge gra... | [📂 19_ccb759a_graphified/](./19_ccb759a_graphified/README.md) |
| 20 | `882a68c` | 2026-09-24 | BEFORE FIXES EVERYTHING IS WORKING | Solidified baseline: all 4 guidelines, hybrid retrieval, non-OCR fallback parser, ben... | [📂 20_882a68c_before-fixes-everything-is-working/](./20_882a68c_before-fixes-everything-is-working/README.md) |

---
<a href="../README.md">&larr; Back to Main Documentation Index</a>
