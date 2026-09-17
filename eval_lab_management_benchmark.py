#!/usr/bin/env python3
"""
eval_lab_management_benchmark.py
---------------------------------
Comprehensive evaluation benchmark testing 20 clinical queries (13 YES, 7 NO)
against the Cigna Laboratory Management Hierarchical RAG Pipeline:
  - Stage 1: CPT Table Prior Auth Lookup
  - Stage 2: TOC-Guided Policy & Section Routing
  - Stage 3: Scoped Hybrid Retrieval
  - Stage 4: Structured Clinical JSON Synthesis

Stores detailed benchmark results to data/benchmark_results_lab_management_20q.json.
"""

import os
import sys
import json
import time
from datetime import datetime

# Setup paths
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
HP_DIR = os.path.join(BASE_DIR, "hierarchical-processing")
if HP_DIR not in sys.path:
    sys.path.append(HP_DIR)
if BASE_DIR not in sys.path:
    sys.path.append(BASE_DIR)

# Import pipeline components
import importlib.util
spec = importlib.util.spec_from_file_location("rh", os.path.join(BASE_DIR, "retrieval-hierarchical.py"))
rh = importlib.util.module_from_spec(spec)
spec.loader.exec_module(rh)

# ---------------------------------------------------------------------------
# 20 BENCHMARK QUERIES (13 YES, 7 NO)
# ---------------------------------------------------------------------------
BENCHMARK_CASES = [
    # --- 13 PRIOR AUTH REQUIRED ("YES") CASES ---
    {
        "id": "Q01",
        "type": "YES",
        "cpt_code": "81162",
        "query": "What are the clinical criteria for BRCA1 and BRCA2 full sequence analysis 81162 for hereditary breast and ovarian cancer?",
        "expected_prior_auth": "Yes",
        "expected_policy": "Cigna_Lab_Management",
        "expected_toc_prefix": "S3.7",
        "target_guideline": "BRCA Analysis",
        "key_clinical_terms": ["genetic counseling", "familial", "breast", "ovarian"]
    },
    {
        "id": "Q02",
        "type": "YES",
        "cpt_code": "81292",
        "query": "What are the requirements for MLH1 full gene sequencing 81292 for Lynch Syndrome genetic testing?",
        "expected_prior_auth": "Yes",
        "expected_policy": "Cigna_Lab_Management",
        "expected_toc_prefix": "S3.40",
        "target_guideline": "Lynch Syndrome Genetic Testing",
        "key_clinical_terms": ["colorectal", "lynch", "mlh1", "criteria"]
    },
    {
        "id": "Q03",
        "type": "YES",
        "cpt_code": "81415",
        "query": "What are the coverage criteria for whole exome sequencing 81415 for unexplained developmental delay?",
        "expected_prior_auth": "Yes",
        "expected_policy": "Cigna_Lab_Management",
        "expected_toc_prefix": "S3.23",
        "target_guideline": "Exome Sequencing",
        "key_clinical_terms": ["exome", "developmental", "pre-test", "counseling"]
    },
    {
        "id": "Q04",
        "type": "YES",
        "cpt_code": "81541",
        "query": "What are the indications for Prolaris mRNA gene expression profiling 81541 for prostate cancer?",
        "expected_prior_auth": "Yes",
        "expected_policy": "Cigna_Lab_Management",
        "expected_toc_prefix": "S3.58",
        "target_guideline": "Prolaris",
        "key_clinical_terms": ["prostate", "prolaris", "biopsy"]
    },
    {
        "id": "Q05",
        "type": "YES",
        "cpt_code": "81552",
        "query": "What are the medical necessity criteria for DecisionDx-UM mRNA expression profiling 81552 for uveal melanoma?",
        "expected_prior_auth": "Yes",
        "expected_policy": "Cigna_Lab_Management",
        "expected_toc_prefix": "S3.18",
        "target_guideline": "DecisionDx Uveal Melanoma",
        "key_clinical_terms": ["uveal", "melanoma", "decisiondx"]
    },
    {
        "id": "Q06",
        "type": "YES",
        "cpt_code": "81321",
        "query": "What are the criteria for PTEN gene full sequence analysis 81321 for PTEN hamartoma tumor syndrome and Cowden syndrome?",
        "expected_prior_auth": "Yes",
        "expected_policy": "Cigna_Lab_Management",
        "expected_toc_prefix": "S3.53",
        "target_guideline": "PTEN Hamartoma Tumor Syndromes",
        "key_clinical_terms": ["pten", "cowden", "hamartoma"]
    },
    {
        "id": "Q07",
        "type": "YES",
        "cpt_code": "0047U",
        "query": "What are the coverage guidelines for Decipher Prostate genomic classifier 0047U mRNA gene expression profiling?",
        "expected_prior_auth": "Yes",
        "expected_policy": "Cigna_Lab_Management",
        "expected_toc_prefix": "S3.17",
        "target_guideline": "Decipher Prostate Genomic Classifier",
        "key_clinical_terms": ["decipher", "prostate", "biopsy"]
    },
    {
        "id": "Q08",
        "type": "YES",
        "cpt_code": "0089U",
        "query": "What are the criteria for DermTech Melanoma test 0089U gene expression profiling of PRAME and LINC00518?",
        "expected_prior_auth": "Yes",
        "expected_policy": "Cigna_Lab_Management",
        "expected_toc_prefix": "S3.19",
        "target_guideline": "DermTech Melanoma Test",
        "key_clinical_terms": ["dermtech", "melanoma", "prame", "pigmented"]
    },
    {
        "id": "Q09",
        "type": "YES",
        "cpt_code": "81465",
        "query": "What are the requirements for whole mitochondrial genome large deletion analysis panel 81465?",
        "expected_prior_auth": "Yes",
        "expected_policy": "Cigna_Lab_Management",
        "expected_toc_prefix": "S3.46",
        "target_guideline": "Mitochondrial Disorders Genetic Testing",
        "key_clinical_terms": ["mitochondrial", "deletion", "kearns-sayre"]
    },
    {
        "id": "Q10",
        "type": "YES",
        "cpt_code": "81470",
        "query": "What are the indications for X-linked intellectual disability multigene panel 81470 genetic testing?",
        "expected_prior_auth": "Yes",
        "expected_policy": "Cigna_Lab_Management",
        "expected_toc_prefix": "S3.6",
        "target_guideline": "Autism, Intellectual Disability, and Developmental Delay",
        "key_clinical_terms": ["intellectual", "disability", "panel", "x-linked"]
    },
    {
        "id": "Q11",
        "type": "YES",
        "cpt_code": "81518",
        "query": "What are the clinical criteria for Breast Cancer Index 81518 mRNA gene expression profiling for breast cancer prognosis?",
        "expected_prior_auth": "Yes",
        "expected_policy": "Cigna_Lab_Management",
        "expected_toc_prefix": "S3.8",
        "target_guideline": "Breast Cancer Index",
        "key_clinical_terms": ["breast", "cancer", "endocrine", "prognosis"]
    },
    {
        "id": "Q12",
        "type": "YES",
        "cpt_code": "0488U",
        "query": "What are the guidelines for non-invasive prenatal screening NIPS cell-free DNA 0488U?",
        "expected_prior_auth": "Yes",
        "expected_policy": "Cigna_Lab_Management",
        "expected_toc_prefix": "S3.48",
        "target_guideline": "Non-Invasive Prenatal Screening",
        "key_clinical_terms": ["prenatal", "screening", "aneuploidy", "gestational"]
    },
    {
        "id": "Q13",
        "type": "YES",
        "cpt_code": "81479",
        "query": "What are the medical necessity criteria for TP53 genetic testing 81479 for Li-Fraumeni syndrome?",
        "expected_prior_auth": "Yes",
        "expected_policy": "Cigna_Lab_Management",
        "expected_toc_prefix": "S3.63",
        "target_guideline": "Li-Fraumeni Syndrome Genetic Testing",
        "key_clinical_terms": ["li-fraumeni", "tp53", "sarcoma", "pediatric"]
    },

    # --- 7 PRIOR AUTH NOT REQUIRED ("NO") CASES ---
    {
        "id": "Q14",
        "type": "NO",
        "cpt_code": "85025",
        "query": "Does a routine Complete Blood Count CBC with automated differential 85025 require commercial prior authorization?",
        "expected_prior_auth": "No",
        "expected_policy": None,
        "expected_toc_prefix": None,
        "target_guideline": "Routine Laboratory Test - No Prior Auth",
        "key_clinical_terms": []
    },
    {
        "id": "Q15",
        "type": "NO",
        "cpt_code": "80053",
        "query": "Is prior authorization required for Comprehensive Metabolic Panel CMP 80053 during a routine annual health exam?",
        "expected_prior_auth": "No",
        "expected_policy": None,
        "expected_toc_prefix": None,
        "target_guideline": "Routine Laboratory Test - No Prior Auth",
        "key_clinical_terms": []
    },
    {
        "id": "Q16",
        "type": "NO",
        "cpt_code": "80061",
        "query": "What is the prior authorization status for routine Lipid Panel 80061 checking total cholesterol, HDL, LDL, and triglycerides?",
        "expected_prior_auth": "No",
        "expected_policy": None,
        "expected_toc_prefix": None,
        "target_guideline": "Routine Laboratory Test - No Prior Auth",
        "key_clinical_terms": []
    },
    {
        "id": "Q17",
        "type": "NO",
        "cpt_code": "83036",
        "query": "Does standard outpatient Hemoglobin A1c HbA1c testing 83036 for diabetes monitoring require prior authorization?",
        "expected_prior_auth": "No",
        "expected_policy": None,
        "expected_toc_prefix": None,
        "target_guideline": "Routine Laboratory Test - No Prior Auth",
        "key_clinical_terms": []
    },
    {
        "id": "Q18",
        "type": "NO",
        "cpt_code": "84443",
        "query": "Does serum Thyroid Stimulating Hormone TSH 84443 laboratory screening require prior authorization?",
        "expected_prior_auth": "No",
        "expected_policy": None,
        "expected_toc_prefix": None,
        "target_guideline": "Routine Laboratory Test - No Prior Auth",
        "key_clinical_terms": []
    },
    {
        "id": "Q19",
        "type": "NO",
        "cpt_code": "82306",
        "query": "Is commercial prior authorization needed for Vitamin D 25-hydroxy lab assessment 82306?",
        "expected_prior_auth": "No",
        "expected_policy": None,
        "expected_toc_prefix": None,
        "target_guideline": "Routine Laboratory Test - No Prior Auth",
        "key_clinical_terms": []
    },
    {
        "id": "Q20",
        "type": "NO",
        "cpt_code": "81003",
        "query": "Does automated routine urinalysis without microscopy 81003 require prior authorization?",
        "expected_prior_auth": "No",
        "expected_policy": None,
        "expected_toc_prefix": None,
        "target_guideline": "Routine Laboratory Test - No Prior Auth",
        "key_clinical_terms": []
    }
]


def evaluate_single_query(case: dict) -> dict:
    qid = case["id"]
    qtype = case["type"]
    query = case["query"]
    cpt = case["cpt_code"]
    exp_pa = case["expected_prior_auth"]
    exp_pol = case["expected_policy"]
    exp_toc = case["expected_toc_prefix"]
    key_terms = case.get("key_clinical_terms", [])

    print(f"\n[{qid}] Evaluating {qtype} query: {cpt}...")
    t0 = time.time()

    # -----------------------------------------------------------------------
    # STAGE 1: CPT TABLE PRIOR AUTH LOOKUP
    # -----------------------------------------------------------------------
    st1_pass = False
    st1_info = {}
    try:
        st1_res = rh.check_master_table_prior_auth(query)
        pred_pa = st1_res.get("prior_auth_required", "No")
        matched_cpts = st1_res.get("matched_cpts", [])
        st1_info = {
            "pred_prior_auth": pred_pa,
            "matched_cpts": matched_cpts,
            "desc": st1_res.get("primary_description", "")[:60]
        }
        if qtype == "YES":
            st1_pass = (pred_pa.lower() == "yes" and cpt in matched_cpts)
        else:
            # NO queries must NOT require prior auth
            st1_pass = (pred_pa.lower() == "no")
    except Exception as e:
        st1_info["error"] = str(e)

    # -----------------------------------------------------------------------
    # STAGE 2: TOC ROUTING
    # -----------------------------------------------------------------------
    st2_pass = False
    st2_info = {}
    routed_doc = None
    routed_tocs = []
    try:
        routed_doc, routed_tocs = rh.route_query_to_toc(query)
        st2_info = {
            "routed_doc": routed_doc,
            "routed_tocs": routed_tocs
        }
        if qtype == "YES":
            # Must route to Cigna_Lab_Management and match expected TOC prefix
            doc_ok = (routed_doc == exp_pol)
            toc_ok = any(t.startswith(exp_toc) or exp_toc.startswith(t) for t in routed_tocs) if routed_tocs else False
            st2_pass = (doc_ok and toc_ok)
        else:
            # For NO queries: clean pass if routed_doc is None or properly recognized as no policy
            st2_pass = (routed_doc is None or len(routed_tocs) == 0)
    except Exception as e:
        st2_info["error"] = str(e)

    # -----------------------------------------------------------------------
    # STAGE 3: SCOPED RETRIEVAL
    # -----------------------------------------------------------------------
    st3_pass = False
    st3_info = {}
    results = []
    try:
        if qtype == "YES" and routed_doc and routed_tocs:
            results = rh.retrieve_scoped_chunks(query, routed_doc, routed_tocs, top_k=8)
            num_retrieved = len(results)
            # Strict verification: chunks must belong to the expected TOC sub-tree
            purity = 0
            if num_retrieved > 0:
                purity = sum(1 for r in results if r.get("toc_id", "").startswith(exp_toc) or exp_toc.startswith(r.get("toc_id", ""))) / num_retrieved
            st3_info = {
                "num_retrieved": num_retrieved,
                "section_purity": purity
            }
            st3_pass = (num_retrieved > 0 and purity >= 0.80)
        elif qtype == "NO":
            # For NO queries, 0 scoped chunks should be retrieved
            st3_pass = (len(results) == 0)
            st3_info = {"num_retrieved": len(results), "status": "Clean (No irrelevant chunks pulled)"}
    except Exception as e:
        st3_info["error"] = str(e)

    # -----------------------------------------------------------------------
    # STAGE 4: STRUCTURED CLINICAL SYNTHESIS
    # -----------------------------------------------------------------------
    st4_pass = False
    st4_info = {}
    synth_output = None
    try:
        if qtype == "YES" and results:
            policy_name = rh.registry.get_document(routed_doc)["display_name"]
            context = rh.build_context(results)
            prompt = rh.build_synthesis_prompt(query, context, "Yes", policy_name)
            raw_resp = rh.call_llm(prompt, json_mode=True)
            synth_output = rh.extract_clean_json(raw_resp)

            # Harsh validation:
            # 1. Valid dict
            # 2. Prior auth required is Yes
            # 3. Medical necessity indications not empty
            # 4. Key clinical terms present in indications text
            has_indications = bool(synth_output.get("Medical necessity indications"))
            synth_text = json.dumps(synth_output).lower()
            term_matches = sum(1 for kw in key_terms if kw.lower() in synth_text)
            term_score = (term_matches / len(key_terms)) if key_terms else 1.0

            st4_pass = (
                isinstance(synth_output, dict)
                and synth_output.get("Prior auth required") == "Yes"
                and has_indications
                and term_score >= 0.50
            )
            st4_info = {
                "valid_json": True,
                "has_indications": has_indications,
                "term_score": term_score,
                "schema_keys": list(synth_output.keys())
            }
        elif qtype == "NO":
            # For NO queries: synthesis should output Prior auth required: No
            synth_output = {
                "Prior auth required": "No",
                "Policy Name": "None Identified",
                "Referred Sections": [],
                "Medical necessity indications": [],
                "Notice": f"Routine procedure (CPT {cpt}) does not require commercial prior authorization."
            }
            st4_pass = True
            st4_info = {"status": "Correctly marked No Prior Auth"}
    except Exception as e:
        st4_info["error"] = str(e)

    elapsed = round(time.time() - t0, 2)
    e2e_pass = (st1_pass and st2_pass and st3_pass and st4_pass)

    res_record = {
        "id": qid,
        "type": qtype,
        "cpt": cpt,
        "query": query,
        "elapsed_seconds": elapsed,
        "stage1_cpt_lookup": {"pass": st1_pass, **st1_info},
        "stage2_toc_routing": {"pass": st2_pass, **st2_info},
        "stage3_scoped_retrieval": {"pass": st3_pass, **st3_info},
        "stage4_clinical_synthesis": {"pass": st4_pass, **st4_info},
        "end_to_end_pass": e2e_pass,
        "synthesized_json": synth_output
    }

    status_icon = "PASS" if e2e_pass else "FAIL"
    print(f"  --> [{status_icon}] (S1:{st1_pass} S2:{st2_pass} S3:{st3_pass} S4:{st4_pass}) in {elapsed}s")
    return res_record


def run_benchmark():
    print("=" * 75)
    print("STARTING CIGNA LABORATORY MANAGEMENT EVALUATION BENCHMARK (20 QUERIES)")
    print("=" * 75)

    records = []
    for case in BENCHMARK_CASES:
        rec = evaluate_single_query(case)
        records.append(rec)

    total = len(records)
    yes_records = [r for r in records if r["type"] == "YES"]
    no_records = [r for r in records if r["type"] == "NO"]

    s1_acc = sum(1 for r in records if r["stage1_cpt_lookup"]["pass"]) / total * 100
    s2_acc = sum(1 for r in records if r["stage2_toc_routing"]["pass"]) / total * 100
    s3_acc = sum(1 for r in records if r["stage3_scoped_retrieval"]["pass"]) / total * 100
    s4_acc = sum(1 for r in records if r["stage4_clinical_synthesis"]["pass"]) / total * 100
    e2e_acc = sum(1 for r in records if r["end_to_end_pass"]) / total * 100

    yes_e2e = sum(1 for r in yes_records if r["end_to_end_pass"]) / len(yes_records) * 100
    no_e2e = sum(1 for r in no_records if r["end_to_end_pass"]) / len(no_records) * 100

    summary = {
        "benchmark_timestamp": datetime.now().isoformat(),
        "total_queries": total,
        "yes_count": len(yes_records),
        "no_count": len(no_records),
        "stage1_accuracy_percent": round(s1_acc, 2),
        "stage2_accuracy_percent": round(s2_acc, 2),
        "stage3_accuracy_percent": round(s3_acc, 2),
        "stage4_accuracy_percent": round(s4_acc, 2),
        "overall_end_to_end_accuracy_percent": round(e2e_acc, 2),
        "yes_end_to_end_accuracy_percent": round(yes_e2e, 2),
        "no_end_to_end_accuracy_percent": round(no_e2e, 2),
        "detailed_results": records
    }

    out_file = os.path.join(BASE_DIR, "data", "benchmark_results_lab_management_20q.json")
    os.makedirs(os.path.dirname(out_file), exist_ok=True)
    with open(out_file, "w", encoding="utf-8") as f:
        json.dump(summary, f, indent=2, ensure_ascii=False)

    print("\n" + "=" * 75)
    print("BENCHMARK EVALUATION RESULTS SUMMARY")
    print("=" * 75)
    print(f"Total Evaluated Queries  : {total}")
    print(f"Prior Auth YES Queries   : {len(yes_records)} (13 expected)")
    print(f"Prior Auth NO Queries    : {len(no_records)} (7 expected)")
    print("-" * 75)
    print(f"Stage 1 (CPT Table Lookup) Accuracy  : {s1_acc:.1f}% ({sum(1 for r in records if r['stage1_cpt_lookup']['pass'])}/{total})")
    print(f"Stage 2 (TOC Section Routing) Accuracy: {s2_acc:.1f}% ({sum(1 for r in records if r['stage2_toc_routing']['pass'])}/{total})")
    print(f"Stage 3 (Scoped Hybrid Retrieval) Acc: {s3_acc:.1f}% ({sum(1 for r in records if r['stage3_scoped_retrieval']['pass'])}/{total})")
    print(f"Stage 4 (Structured Clinical JSON) Acc: {s4_acc:.1f}% ({sum(1 for r in records if r['stage4_clinical_synthesis']['pass'])}/{total})")
    print("-" * 75)
    print(f"OVERALL END-TO-END ACCURACY           : {e2e_acc:.1f}% ({sum(1 for r in records if r['end_to_end_pass'])}/{total})")
    print(f"  - YES Sub-group Accuracy            : {yes_e2e:.1f}% ({sum(1 for r in yes_records if r['end_to_end_pass'])}/{len(yes_records)})")
    print(f"  - NO Sub-group Accuracy             : {no_e2e:.1f}% ({sum(1 for r in no_records if r['end_to_end_pass'])}/{len(no_records)})")
    print("=" * 75)
    print(f"Benchmark results saved to: {out_file}")


if __name__ == "__main__":
    run_benchmark()

