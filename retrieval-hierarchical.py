"""
retrieval-hierarchical.py
-------------------------
Multi-Document TOC-Guided Hierarchical RAG Pipeline.

Pipeline Flow:
  Stage 1: Master Table Check (output/table.json)
    Matches user query to procedure CPT codes and determines: "Prior auth required": "Yes" / "No".
  Stage 2: Table of Contents (TOC) Multi-Document Routing
    Routes user query against available policy TOCs to identify the target document and specific toc_id(s).
  Stage 3: Scoped Hybrid Retrieval
    Runs BM25 + Semantic dense embeddings strictly over candidate chunks matching the routed toc_id(s),
    with automatic sibling condition completion.
  Stage 4: Structured Clinical JSON Synthesis
    Synthesizes the retrieved criteria and master table status into the exact JSON schema requested.
"""

import os
import sys
import json
import re
from datetime import datetime
from dotenv import load_dotenv

# Include hierarchical-processing in path for modules
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
HP_DIR = os.path.join(BASE_DIR, "hierarchical-processing")
if HP_DIR not in sys.path:
    sys.path.append(HP_DIR)

from document_registry import DocumentRegistry
from cpt_table_lookup import CPTTableLookup
from hybrid_search_hierarchical import scoped_search, search

load_dotenv()

GROQ_API_KEY = os.getenv("GROQ_API_KEY")
GEN_MODEL = os.getenv("GEN_MODEL", "groq/compound-mini")
OLLAMA_HOST = os.getenv("OLLAMA_HOST", "http://192.168.0.33:11434/v1")
OLLAMA_MODEL = os.getenv("CHAT_MODEL", "hf.co/unsloth/medgemma-1.5-4b-it-GGUF:Q8_0")

OUTPUT_DIR = os.path.join(BASE_DIR, "data", "results_new")
TABLE_JSON_PATH = os.path.join(BASE_DIR, "output", "table.json")

# Initialize shared registry and CPT lookup
registry = DocumentRegistry(base_dir=HP_DIR)
cpt_lookup = CPTTableLookup(table_json_path=TABLE_JSON_PATH)


# ============================================================
# LLM CALL WITH ROBUST PROVIDER HANDLING
# ============================================================

def call_llm(prompt: str, json_mode: bool = True) -> str:
    """Call Groq API with automatic fallback to local Ollama if rate-limited or unavailable."""
    if GROQ_API_KEY:
        try:
            from groq import Groq
            groq_client = Groq(api_key=GROQ_API_KEY)
            models_to_try = [GEN_MODEL, "qwen/qwen3.8-27b", "llama-3.1-8b-instant", "groq/compound-mini", "openai/gpt-oss-120b"]
            for m in models_to_try:
                if not m:
                    continue
                # Try with json_mode first, then without if Groq rejects the JSON
                for use_json in ([True, False] if json_mode else [False]):
                    try:
                        kwargs = {
                            "model": m,
                            "messages": [
                                {"role": "system", "content": "You are a clinical decision support assistant that outputs strictly valid JSON objects without preamble."},
                                {"role": "user", "content": prompt}
                            ],
                            "temperature": 0.1,
                            "max_tokens": 5000
                        }
                        if use_json:
                            kwargs["response_format"] = {"type": "json_object"}
                        response = groq_client.chat.completions.create(**kwargs)
                        content = response.choices[0].message.content.strip()
                        if content:
                            return content
                    except Exception as m_err:
                        err_str = str(m_err).lower()
                        # Rate limit → sleep briefly and try next model
                        if "429" in str(m_err) or "rate_limit" in err_str:
                            time.sleep(1.5)
                            break
                        # Groq's JSON validator rejected the output → retry same model without json_mode
                        if "json_validate_failed" in err_str or "failed to validate json" in err_str:
                            continue
                        # Model not found or not supported → try next model
                        if "model_not_found" in err_str or "not found" in err_str or "not_supported" in err_str:
                            break
                        # Unknown error → try next model
                        break
        except Exception as e:
            pass  # Fall through to local Ollama

    from openai import OpenAI
    ollama_client = OpenAI(base_url=OLLAMA_HOST, api_key="ollama")
    response = ollama_client.chat.completions.create(
        model=OLLAMA_MODEL,
        messages=[
            {"role": "system", "content": "You are a clinical decision support assistant that outputs strictly valid JSON objects without preamble. Do not output thoughts or reasoning."},
            {"role": "user", "content": prompt}
        ],
        temperature=0.1,
        max_tokens=5000
    )
    return response.choices[0].message.content.strip()


try:
    import json_repair
except ImportError:
    json_repair = None


def extract_clean_json(raw_text: str) -> dict:
    """Extract and clean JSON object from LLM response, handling reasoning models and truncated thinking tags."""
    if not raw_text or not raw_text.strip():
        raise ValueError("Empty LLM response received")

    # 1. Strip closed reasoning / thinking tags
    text = re.sub(r"<(?:thought|think)>.*?</(?:thought|think)>", "", raw_text, flags=re.DOTALL)
    text = re.sub(r"^thought\s+.*?(?=(?:```|\{))", "", text, flags=re.DOTALL | re.IGNORECASE)

    # 2. If <think> or <thought> was left unclosed (due to token limit/formatting), extract from the first '{'
    first_brace = text.find("{")
    if first_brace == -1:
        # Check in raw_text in case it was inside the thinking tag
        first_brace = raw_text.find("{")
        if first_brace != -1:
            text = raw_text[first_brace:]
    else:
        text = text[first_brace:]

    # 3. Extract outermost JSON block if closing brace exists
    match = re.search(r"\{.*\}", text, flags=re.DOTALL)
    candidate = match.group(0).strip() if match else text.strip()

    # 4. Direct standard parse attempt
    try:
        return json.loads(candidate)
    except Exception:
        pass

    # 5. Remove trailing commas before closing braces/brackets
    cleaned_no_trailing = re.sub(r",\s*([\]}])", r"\1", candidate)
    try:
        return json.loads(cleaned_no_trailing)
    except Exception:
        pass

    # 6. Use json_repair (repairs unclosed braces, truncated JSON, and quote issues)
    if json_repair is not None:
        try:
            repaired = json_repair.loads(candidate)
            if isinstance(repaired, dict):
                return repaired
        except Exception:
            pass

        try:
            repaired = json_repair.loads(raw_text)
            if isinstance(repaired, dict):
                return repaired
        except Exception:
            pass

    # 7. Fallback: try to repair trailing text
    if not candidate.endswith("}"):
        candidate_closed = candidate + "\n}"
        try:
            return json.loads(re.sub(r",\s*([\]}])", r"\1", candidate_closed))
        except Exception:
            pass

    raise ValueError(f"Could not find valid JSON object in output: {raw_text[:200]}")


# ============================================================
# STAGE 1: MASTER TABLE PRIOR AUTH CHECK
# ============================================================

def verify_candidate_cpts_with_llm(query: str, candidate_rows: list[dict]) -> dict:
    """Lightweight LLM verifier to prevent false positive keyword overlaps and distinguish procedures from diagnoses."""
    cand_lines = []
    for i, r in enumerate(candidate_rows[:5], 1):
        cpt = r.get("CPT® Code", "")
        desc = r.get("CPT® Code Description", "")[:120]
        pa = r.get("Commercial Prior Authorization Required?", "")
        cand_lines.append(f"{i}. CPT {cpt} (Prior Auth: {pa}): {desc}")
    cand_str = "\n".join(cand_lines) if cand_lines else "No candidate CPT rows found in table."

    prompt = f"""You are a clinical coding and prior authorization verification expert.
User Query: "{query}"

Candidate CPT procedure rows retrieved from the carrier prior authorization table:
{cand_str}

Instructions:
1. Determine if the user's query refers to an actual billable medical procedure, surgery, lab test, or diagnostic service.
   If the query asks about a general illness, medical condition, or symptom (e.g., "common cold", "cough", "hypertension", "diabetes", "fever") rather than a specific procedure, output:
   {{"is_procedure": false, "prior_auth_required": "Not Applicable", "matched_cpt": null, "reason": "Query refers to a medical diagnosis or condition, not a billable procedure code. Commercial prior authorization applies to procedures/tests, not diagnoses."}}
2. If the user is asking about a procedure, verify if ANY of the candidate rows truly represent what the user is asking about.
   - If a candidate truly matches (e.g. "BRCA testing" matching BRCA1/2 sequencing), output:
     {{"is_procedure": true, "prior_auth_required": "<Yes or No based on candidate>", "matched_cpt": "<CPT code>", "reason": "<brief rationale>"}}
   - If candidates are merely accidental word overlaps (e.g. "common cold" matching "common carotid artery stent"), output:
     {{"is_procedure": false, "prior_auth_required": "Not Applicable", "matched_cpt": null, "reason": "Query is a diagnosis with accidental lexical overlap against unrelated procedure."}}
3. If no candidate matches and no prior authorization policy exists for this service, output:
   {{"is_procedure": true, "prior_auth_required": "Not Found", "matched_cpt": null, "reason": "No matching procedure found in prior authorization master table."}}

Output strictly valid JSON with keys: "is_procedure", "prior_auth_required", "matched_cpt", "reason".
"""
    try:
        raw_resp = call_llm(prompt, json_mode=True)
        return extract_clean_json(raw_resp)
    except Exception as e:
        print(f"[Notice] LLM CPT verification fallback: {e}")
        return {
            "is_procedure": True,
            "prior_auth_required": "Not Found",
            "matched_cpt": None,
            "reason": str(e)
        }


def find_policy_for_cpt_code(cpt_code: str) -> list[tuple[str, str, str]]:
    """Scan registered policies to find which policy document contains this CPT code in its text or tables."""
    clean_code = cpt_code.strip()
    matches = []
    for k, doc in registry.documents.items():
        mf = doc.get("metadata_file")
        if mf and os.path.exists(mf):
            try:
                with open(mf, "r", encoding="utf-8") as f:
                    meta = json.load(f)
                for chunk in meta:
                    sec = chunk.get("section", "")
                    text = chunk.get("text", "")
                    if clean_code in text and any(w in sec.lower() for w in ["code", "procedure", "guideline", "criteria"]):
                        matches.append((k, chunk.get("toc_id"), sec))
                        break
            except Exception:
                pass
    return matches


def check_master_table_prior_auth(query: str) -> dict:
    """
    Stage 1: Check output/table.json for procedure matching the query.
    Uses 2-Tier Architecture:
      - Tier 1: Deterministic Fast-Path for explicit CPT/HCPCS codes (0ms), with policy fallback if not in table.json.
      - Tier 2: LLM Clinical Verifier for text-based queries to validate medical procedure vs diagnosis.
    Returns: prior_auth_required ('Yes'/'No'/'Not Applicable'/'Not Found'), matched_cpts, and description.
    """
    analysis = cpt_lookup.analyze_query_prior_auth(query)

    # Tier 1: Fast deterministic bypass if an exact CPT/HCPCS code was queried
    if analysis.get("is_explicit_cpt"):
        # Fallback check: If not found in table.json, check if code exists in policy documents
        if analysis.get("prior_auth_required") == "Not Found" and analysis.get("matched_cpts"):
            for c in analysis["matched_cpts"]:
                hits = find_policy_for_cpt_code(c)
                if hits:
                    doc_k, t_id, sec = hits[0]
                    doc_display = registry.documents.get(doc_k, {}).get("display_name", doc_k)
                    analysis["prior_auth_required"] = "Yes"
                    analysis["primary_description"] = f"CPT {c} identified in policy: {doc_display}"
                    analysis["policy_hint"] = doc_k
                    break
        return analysis

    # Tier 2: Text-based query without explicit CPT code -> Run LLM Clinical Verifier
    candidate_rows = analysis.get("matched_rows", [])
    verified = verify_candidate_cpts_with_llm(query, candidate_rows)

    pa_status = verified.get("prior_auth_required", "Not Found")
    matched_cpt = verified.get("matched_cpt")
    matched_cpts = [str(matched_cpt).strip()] if matched_cpt else []

    desc = ""
    if matched_cpt and candidate_rows:
        for r in candidate_rows:
            if str(r.get("CPT® Code", "")).strip() == str(matched_cpt).strip():
                desc = r.get("CPT® Code Description", "")
                break

    return {
        "prior_auth_required": pa_status,
        "matched_cpts": matched_cpts,
        "primary_description": desc,
        "is_procedure": verified.get("is_procedure", True),
        "explanation": verified.get("reason", ""),
        "is_explicit_cpt": False
    }


# ============================================================
# STAGE 2: MULTI-DOCUMENT TOC ROUTING
# ============================================================

META_QUERY_STOPWORDS = {
    "prior", "auth", "authorization", "require", "required", "commercial",
    "guidelines", "guideline", "policy", "policies", "covered", "coverage",
    "review", "determinations", "determination", "medical", "necessity",
    "criteria", "what", "are", "the", "for", "does", "is", "a", "an",
    "in", "of", "and", "or", "to", "with", "during", "status", "needed",
    "procedure", "procedures", "test", "testing"
}

def get_ranked_candidate_sections(query: str, matched_cpts: list[str] = None, cpt_desc: str = None, max_candidates: int = 6) -> list[dict]:
    """
    Dynamically rank candidate policy sections across all registered documents using:
      1. Direct CPT code mentions in chunk text/tables (highest fidelity)
      2. BM25 keyword matching across chunk metadata
      3. Title token overlap with document flat_toc nodes
    Zero hardcoding: uses document-provided metadata and TOC files.
    """
    import pickle
    search_text = f"{query} {cpt_desc}" if cpt_desc else query
    raw_tokens = re.findall(r"[a-z0-9]+", search_text.lower())
    clean_tokens = [t for t in raw_tokens if t not in META_QUERY_STOPWORDS]
    tokens = clean_tokens if clean_tokens else raw_tokens

    explicit_codes = matched_cpts if matched_cpts else re.findall(r"\b[0-9]{4}[0-9A-Za-z]\b|\b[0-9]{5}\b", query)
    is_admin_query = any(w in query.lower() for w in ["administrative", "billing", "reimbursement", "appeal", "glossary"])

    candidates_by_key = {}

    for k, d in registry.documents.items():
        doc_name = d.get("display_name", k)
        bm_file = d.get("bm25_file")
        meta_file = d.get("metadata_file")
        toc_file = d.get("toc_file")

        flat_nodes = {}
        canonical_parent = {}
        if toc_file and os.path.exists(toc_file):
            try:
                with open(toc_file, "r", encoding="utf-8") as f:
                    t_data = json.load(f)
                for n in t_data.get("flat_toc", []):
                    tid = n.get("toc_id")
                    if tid:
                        flat_nodes[tid] = n.get("title", "")
                # Canonical parent mapping: collapse child nodes that duplicate an ancestor title back to highest ancestor
                for tid, title in flat_nodes.items():
                    parts = tid.split(".")
                    for i in range(1, len(parts)):
                        anc = ".".join(parts[:i])
                        if anc in flat_nodes and flat_nodes[anc].strip().lower() == title.strip().lower():
                            canonical_parent[tid] = anc
                            break
            except Exception:
                pass

        if not bm_file or not meta_file or not os.path.exists(bm_file) or not os.path.exists(meta_file):
            continue

        try:
            with open(bm_file, "rb") as f:
                b = pickle.load(f)
            with open(meta_file, "r", encoding="utf-8") as f:
                m = json.load(f)

            scores = b["bm25"].get_scores(tokens) if tokens else [0] * len(m)

            # 1. Direct CPT Code hits
            for c_code in explicit_codes:
                for idx, chunk in enumerate(m):
                    chunk_text = chunk.get("text", "")
                    if c_code in chunk_text:
                        t_id = chunk.get("toc_id")
                        if t_id:
                            parts = t_id.split(".")
                            primary_t_id = ".".join(parts[:2]) if len(parts) >= 2 else t_id
                            primary_t_id = canonical_parent.get(primary_t_id, primary_t_id)
                            sec = chunk.get("section", "")
                            sec_lower = sec.lower()
                            if not is_admin_query and any(term in sec_lower for term in [
                                "administrative guidelines", "glossary", "guideline page"
                            ]):
                                continue
                            title = flat_nodes.get(primary_t_id, flat_nodes.get(t_id, sec.split(">")[-1].strip()))
                            c_key = (k, primary_t_id)
                            if c_key not in candidates_by_key:
                                candidates_by_key[c_key] = {
                                    "doc_key": k,
                                    "doc_name": doc_name,
                                    "toc_id": primary_t_id,
                                    "title": title,
                                    "score": 25.0
                                }
                            else:
                                candidates_by_key[c_key]["score"] += 10.0

            # 2. BM25 top chunks
            top_indices = sorted(range(len(scores)), key=lambda i: scores[i], reverse=True)[:15]
            for idx in top_indices:
                sc = float(scores[idx])
                if sc > 2.0:
                    chunk = m[idx]
                    t_id = chunk.get("toc_id")
                    if not t_id:
                        continue
                    sec = chunk.get("section", "")
                    sec_lower = sec.lower()
                    if not is_admin_query and any(term in sec_lower for term in [
                        "administrative guidelines", "glossary", "billing and reimbursement",
                        "codes (", "codes", "references", "guideline page"
                    ]):
                        continue
                    parts = t_id.split(".")
                    primary_t_id = ".".join(parts[:2]) if len(parts) >= 2 else t_id
                    primary_t_id = canonical_parent.get(primary_t_id, primary_t_id)
                    title = flat_nodes.get(primary_t_id, flat_nodes.get(t_id, sec.split(">")[-1].strip()))
                    c_key = (k, primary_t_id)
                    if c_key not in candidates_by_key:
                        candidates_by_key[c_key] = {
                            "doc_key": k,
                            "doc_name": doc_name,
                            "toc_id": primary_t_id,
                            "title": title,
                            "score": sc
                        }
                    else:
                        candidates_by_key[c_key]["score"] += sc * 0.5

            # 3. Direct Title lexical matching against flat_nodes
            for tid, title in flat_nodes.items():
                title_lower = title.lower()
                if not is_admin_query and any(term in title_lower for term in [
                    "administrative guidelines", "glossary", "billing and reimbursement",
                    "codes (", "references"
                ]):
                    continue
                t_tokens = set(re.findall(r"[a-z0-9]+", title_lower)) - META_QUERY_STOPWORDS
                overlap = set(tokens) & t_tokens
                if overlap:
                    overlap_ratio = len(overlap) / (len(t_tokens) + 1e-5)
                    boost = len(overlap) * 3.0 + (5.0 if overlap_ratio > 0.4 else 0)
                    parts = tid.split(".")
                    primary_tid = ".".join(parts[:2]) if len(parts) >= 2 else tid
                    primary_tid = canonical_parent.get(primary_tid, primary_tid)
                    c_key = (k, primary_tid)
                    if c_key not in candidates_by_key:
                        candidates_by_key[c_key] = {
                            "doc_key": k,
                            "doc_name": doc_name,
                            "toc_id": primary_tid,
                            "title": flat_nodes.get(primary_tid, title),
                            "score": boost
                        }
                    else:
                        candidates_by_key[c_key]["score"] += boost

        except Exception:
            pass

    ranked = sorted(candidates_by_key.values(), key=lambda x: x["score"], reverse=True)
    final_cands = []
    for i, c in enumerate(ranked[:max_candidates], 1):
        c["candidate_index"] = i
        final_cands.append(c)

    return final_cands


def route_query_to_toc(query: str, prior_auth_status: str = None, cpt_desc: str = None, matched_cpts: list[str] = None) -> tuple[str, list[str]]:
    """
    Stage 2: Route user query against available policy Table of Contents using Constrained Candidate-Index Selection.
    Returns: (document_key, list_of_toc_ids)
    """
    if prior_auth_status:
        pa_lower = prior_auth_status.strip().lower()
        if pa_lower in ["no", "none", "not required", "not applicable", "false", "0"]:
            print(f"  ⚡ Bypassing Stage 2 TOC routing (Master Table indicates Prior Auth = '{prior_auth_status}')")
            return None, []

    explicit_codes = matched_cpts if matched_cpts else re.findall(r"\b[0-9]{4}[0-9A-Za-z]\b|\b[0-9]{5}\b", query)

    candidates = get_ranked_candidate_sections(query, matched_cpts=explicit_codes, cpt_desc=cpt_desc, max_candidates=6)
    if not candidates:
        return None, []

    cand_lines = []
    for c in candidates:
        cand_lines.append(f"[{c['candidate_index']}] Policy: {c['doc_key']} | Section: [{c['toc_id']}] {c['title']}")
    candidates_text = "\n".join(cand_lines)

    procedure_str = f"\nProcedure / Clinical Context: {cpt_desc}" if cpt_desc else ""

    prompt = f"""You are an expert clinical prior authorization policy router.
Given the clinical query and candidate policy sections below:
1. Select the single candidate number (1, 2, 3...) whose section contains the medical necessity criteria for this procedure or condition.
2. If NONE of the candidates cover this procedure, or if the question is about a routine non-precertified test (e.g. routine CBC, CMP, Lipid panel, HbA1c, TSH, Urinalysis, Vitamin D, routine office visits) that does not require prior authorization, return "selected_candidate": null.

### Candidate Policy Sections:
{candidates_text}

### Question:
{query}{procedure_str}

### Output Instructions:
Output strictly a JSON object:
{{"selected_candidate": <number 1-{len(candidates)} or null>, "reason": "<brief rationale>"}}
"""

    try:
        raw_resp = call_llm(prompt, json_mode=True)
        routing_data = extract_clean_json(raw_resp)
        sel = routing_data.get("selected_candidate")

        if sel is not None:
            try:
                sel_idx = int(sel)
                if 1 <= sel_idx <= len(candidates):
                    chosen = candidates[sel_idx - 1]
                    return chosen["doc_key"], [chosen["toc_id"]]
            except (ValueError, TypeError):
                pass

        # Fallback: check if the LLM returned document_key or toc_ids directly
        doc_key = routing_data.get("document_key")
        toc_ids = routing_data.get("toc_ids", [])
        if doc_key and doc_key in registry.documents:
            valid_tocs = set()
            tf = registry.documents[doc_key].get("toc_file")
            if tf and os.path.exists(tf):
                try:
                    with open(tf, "r", encoding="utf-8") as f:
                        valid_tocs = set(n.get("toc_id") for n in json.load(f).get("flat_toc", []))
                except Exception:
                    pass

            validated_ids = []
            for tid in toc_ids:
                s = str(tid).strip()
                if s in valid_tocs:
                    validated_ids.append(s)
                elif candidates and candidates[0]["doc_key"] == doc_key:
                    validated_ids.append(candidates[0]["toc_id"])
            if validated_ids:
                return doc_key, validated_ids
            elif candidates and candidates[0]["doc_key"] == doc_key:
                return doc_key, [candidates[0]["toc_id"]]

    except Exception as e:
        print(f"[Notice] TOC routing exception ({e})")
        if candidates and candidates[0]["score"] >= 15.0:
            return candidates[0]["doc_key"], [candidates[0]["toc_id"]]

    return None, []


# ============================================================
# STAGE 3: SCOPED HYBRID RETRIEVAL
# ============================================================

def retrieve_scoped_chunks(query: str, doc_key: str, candidate_toc_ids: list[str], top_k: int = 8) -> list[dict]:
    """
    Stage 3: Run hybrid search strictly scoped to the candidate toc_ids of the target document.
    """
    expanded_tocs = list(candidate_toc_ids)
    doc_info = registry.get_document(doc_key)
    if doc_info and doc_info.get("toc_file") and os.path.exists(doc_info["toc_file"]):
        try:
            with open(doc_info["toc_file"], "r", encoding="utf-8") as f:
                t_data = json.load(f)
            flat = {n["toc_id"]: n.get("title", "").strip().lower() for n in t_data.get("flat_toc", []) if n.get("toc_id")}
            for tid in candidate_toc_ids:
                parts = tid.split(".")
                for i in range(1, len(parts)):
                    anc = ".".join(parts[:i])
                    if anc in flat and flat[anc] == flat.get(tid, ""):
                        if anc not in expanded_tocs:
                            expanded_tocs.append(anc)
                        break
        except Exception:
            pass

    results = scoped_search(
        query=query,
        policy_hint=doc_key,
        candidate_toc_ids=expanded_tocs,
        top_k=top_k,
        alpha=0.5,
        mode="hybrid"
    )
    return results


def clean_section_breadcrumb(section_path: str) -> str:
    """Deduplicate repeated adjacent segments in breadcrumb hierarchies."""
    if not section_path:
        return ""
    parts = [p.strip() for p in section_path.split(">") if p.strip()]
    deduped = []
    for p in parts:
        if not deduped:
            deduped.append(p)
        else:
            prev = deduped[-1].lower()
            curr = p.lower()
            if curr == prev or curr.startswith(prev) or prev.startswith(curr):
                if len(p) > len(deduped[-1]):
                    deduped[-1] = p
            else:
                deduped.append(p)
    return " > ".join(deduped)


def build_context(results: list[dict]) -> str:
    # Prioritize clinical criteria chunks over pure bibliography/reference sections
    clinical_results = [
        r for r in results 
        if "references" not in r.get("section", "").lower()
    ]
    effective_results = clinical_results if clinical_results else results

    blocks = []
    for i, result in enumerate(effective_results):
        sec = clean_section_breadcrumb(result.get('section', ''))
        t_id = result.get('toc_id', '')
        header = f"[{i + 1}] Section: {sec}" + (f" (TOC: {t_id})" if t_id else "")
        blocks.append(f"{header}\n{result.get('text', '')}")
    return "\n\n---\n\n".join(blocks)


# ============================================================
# STAGE 4: STRUCTURED CLINICAL SYNTHESIS
# ============================================================

def build_synthesis_prompt(query: str, context: str, prior_auth_status: str, policy_name: str) -> str:
    return f"""You are an expert clinical medical policy analyst.
Analyze the user's clinical question and the provided policy context below.
Synthesize the requirements into a comprehensive, high-precision clinical policy report.

You must format your answer strictly as a valid JSON object matching this schema:

{{
  "Prior auth required": "{prior_auth_status}",
  "Policy Name": "{policy_name}",
  "Referred Sections": [
    "<Primary policy section ID/title>",
    "<Clinical condition / subsection 1>",
    "<Clinical condition / subsection 2>"
  ],
  "Medical necessity indications": [
    {{
      "Guideline Category": "<Clinical Condition / Category Name>",
      "Required findings": [
        "<Detailed bullet of symptom requirements, severity, and functional impairment>",
        "<Detailed bullet of objective physical examination findings required>",
        "<Detailed bullet of diagnostic imaging / laboratory findings required>",
        "<Detailed bullet of conservative management requirements and trial duration>",
        "<Detailed bullet of general criteria: qualifying rules and behavioral/risk health criteria>"
      ],
      "Source": "<Clean section citation without repeating titles, e.g. Section Title > Subsection (TOC: ID)>"
    }}
  ],
  "Non-Indications": [
    "<Clinical scenario where procedure is NOT medically necessary or is excluded based on policy rules (e.g. surgery prior to required elapsed interval, absence of concordant objective imaging or clinical deficits, failure to complete required trial of conservative therapy, unmanaged behavioral/risk health disorders)>"
    "<List clinical scenarios where the procedure is NOT medically necessary or is excluded based on the policy context. If none mentioned in context, output []>"
  ],
  "Important criteria & exceptions": [
    "<Important qualifying rules, verification methods, conservative care exceptions, or multi-level / concurrent procedure requirements>"
    "<List qualifying rules, verification methods, or exceptions stated in the policy context. If none, output []>"
  ],
  "Documentation required": [
    "<Specific clinical documents, diagnostic imaging reports, pathology/laboratory results, and provider notes required to verify criteria based strictly on the context>"
    "<List specific clinical documents, imaging reports, or provider records required to verify criteria based on the context. If none required or mentioned, output []>"
  ]
}}

### Medical Policy Context:
{context}

### User Question:
{query}

### CRITICAL OUTPUT INSTRUCTIONS:
1. Output ONLY a valid JSON object. Do not include markdown code blocks or conversational text.
2. NO PLACEHOLDERS OR GENERIC TEXT: Do NOT output placeholder text like "Conditions or scenarios considered not medically necessary" or "Specific clinical documentation, imaging reports, or test results required for submission".
3. "Documentation required": You MUST derive and list every concrete clinical document (imaging views, prior operative reports, therapy records, laboratory results) needed to prove the patient meets the criteria in the context.
4. "Non-Indications": You MUST extract or derive the specific clinical scenarios where the procedure is NOT medically necessary or is excluded based on the policy criteria.
5. "Source": Clean breadcrumbs only. Do not duplicate titles (e.g., write "Section Title > Subsection", NEVER "Section Title... > Section Title...").
6. Ground all answers strictly in the provided Medical Policy Context. Do NOT invent criteria or use generic placeholder text.
7. If "Documentation required" or "Non-Indications" are not specified or required in the context, return an empty array [] for that field.
8. CRITICAL: If the requested test or procedure is deemed Experimental, Investigational, Unproven, or NOT medically necessary with zero approved indications (e.g. DermTech melanoma test), you MUST still output "Prior auth required": "{prior_auth_status}" and "Medical necessity indications": [], detailing all investigational exclusions, non-covered reasons, and lack of evidence under "Non-Indications".
"""


def normalize_clinical_json(raw_dict: dict, prior_auth_status: str, policy_name: str) -> dict:
    """
    Universally normalize clinical synthesis JSON to guarantee all 7 canonical keys exist,
    regardless of casing (e.g. 'non-indications' vs 'Non-Indications') or whether the test is
    covered vs investigational/unproven.
    """
    if not isinstance(raw_dict, dict):
        raw_dict = {}

    key_alias_map = {
        "prior auth required": "Prior auth required",
        "prior_auth_required": "Prior auth required",
        "prior authorization required": "Prior auth required",
        "policy name": "Policy Name",
        "policy_name": "Policy Name",
        "referred sections": "Referred Sections",
        "referred_sections": "Referred Sections",
        "medical necessity indications": "Medical necessity indications",
        "medical_necessity_indications": "Medical necessity indications",
        "indications": "Medical necessity indications",
        "non-indications": "Non-Indications",
        "non_indications": "Non-Indications",
        "non indications": "Non-Indications",
        "important criteria & exceptions": "Important criteria & exceptions",
        "important_criteria_and_exceptions": "Important criteria & exceptions",
        "important_criteria_&_exceptions": "Important criteria & exceptions",
        "exceptions": "Important criteria & exceptions",
        "documentation required": "Documentation required",
        "documentation_required": "Documentation required",
    }

    normalized = {}
    for k, v in raw_dict.items():
        canon_key = key_alias_map.get(str(k).strip().lower(), k)
        normalized[canon_key] = v

    normalized["Prior auth required"] = prior_auth_status
    if not normalized.get("Policy Name"):
        normalized["Policy Name"] = policy_name

    # Handle Medical necessity indications
    if "Medical necessity indications" not in normalized or not normalized["Medical necessity indications"]:
        if "criteria" in normalized and isinstance(normalized["criteria"], list):
            indications = []
            for c in normalized["criteria"]:
                if isinstance(c, dict):
                    desc = c.get("description", "")
                    docs = c.get("documentation_required", [])
                    indications.append({
                        "Guideline Category": desc[:60] if desc else "Clinical Criteria",
                        "Required findings": [desc] + (docs if isinstance(docs, list) else []),
                        "Source": policy_name
                    })
            normalized["Medical necessity indications"] = indications
        elif not isinstance(normalized.get("Medical necessity indications"), list):
            normalized["Medical necessity indications"] = []

    if "Referred Sections" not in normalized or not isinstance(normalized["Referred Sections"], list):
        normalized["Referred Sections"] = [policy_name]

    if "Important criteria & exceptions" not in normalized or not isinstance(normalized["Important criteria & exceptions"], list):
        normalized["Important criteria & exceptions"] = []

    # Clean breadcrumbs
    for ind in normalized.get("Medical necessity indications", []):
        if "Source" in ind and isinstance(ind["Source"], str):
            ind["Source"] = clean_section_breadcrumb(ind["Source"])

    cleaned_refs = []
    for ref in normalized.get("Referred Sections", []):
        c = clean_section_breadcrumb(str(ref))
        if c and c not in cleaned_refs:
            cleaned_refs.append(c)
    normalized["Referred Sections"] = cleaned_refs

    PLACEHOLDER_SUBSTRINGS = [
        "conditions or scenarios considered not medically necessary",
        "specific clinical documentation, imaging reports",
        "clinical scenario where",
        "condition category name"
    ]
    if "Non-Indications" in normalized and isinstance(normalized["Non-Indications"], list):
        normalized["Non-Indications"] = [
            item for item in normalized["Non-Indications"]
            if not any(sub in str(item).lower() for sub in PLACEHOLDER_SUBSTRINGS)
        ]
    else:
        normalized["Non-Indications"] = []

    if "Documentation required" in normalized and isinstance(normalized["Documentation required"], list):
        normalized["Documentation required"] = [
            item for item in normalized["Documentation required"]
            if not any(sub in str(item).lower() for sub in PLACEHOLDER_SUBSTRINGS)
        ]
    else:
        normalized["Documentation required"] = []

    return normalized


def run_rag_pipeline(query: str, top_k: int = 8) -> dict:
    print("=" * 70)
    print(f"QUERY: {query}")
    print("=" * 70)

    # ---------------------------------------------------------
    # STAGE 1: Master Table Check
    # ---------------------------------------------------------
    print("\n[Stage 1: Master Table Check]")
    table_analysis = check_master_table_prior_auth(query)
    prior_auth_status = table_analysis.get("prior_auth_required", "Yes")
    matched_cpts = table_analysis.get("matched_cpts", [])
    cpt_desc = table_analysis.get("primary_description", "")
    print(f"  Prior Authorization Required: {prior_auth_status}")
    print(f"  Matched CPT Codes           : {matched_cpts}")
    if cpt_desc:
        print(f"  Procedure Description       : {cpt_desc[:80]}...")

    status_lower = prior_auth_status.strip().lower()

    # ---------------------------------------------------------
    # STAGE 2: TOC-Level Policy & Section Routing
    # ---------------------------------------------------------
    print("\n[Stage 2: TOC-Level Routing]")
    doc_key, routed_toc_ids = route_query_to_toc(
        query=query,
        prior_auth_status=prior_auth_status,
        cpt_desc=cpt_desc,
        matched_cpts=matched_cpts
    )
    if not doc_key or doc_key not in registry.documents:
        print("  [Notice] No matching policy document identified in registry.")
        notice_text = table_analysis.get("explanation", "")
        if not notice_text:
            if status_lower == "not applicable":
                notice_text = f"The query '{query}' refers to a medical diagnosis or condition rather than a billable procedure, surgery, or diagnostic service code. Commercial prior authorization applies strictly to procedures and test codes."
            elif status_lower == "no":
                notice_text = f"The requested procedure ({', '.join(matched_cpts) if matched_cpts else 'routine service'}) does not require commercial prior authorization under standard coverage terms."
            else:
                notice_text = f"No registered medical coverage policy was identified that covers the clinical question: '{query}'."

        structured_json = {
            "Prior auth required": prior_auth_status,
            "Policy Name": "None Identified",
            "Referred Sections": [],
            "Medical necessity indications": [],
            "Non-Indications": [],
            "Important criteria & exceptions": [],
            "Documentation required": [],
            "Notice": notice_text
        }
        os.makedirs(OUTPUT_DIR, exist_ok=True)
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        slug = "".join(c if c.isalnum() or c == " " else "" for c in query)
        slug = "_".join(slug.split())[:50]
        filename = f"{timestamp}_{slug}.json"
        filepath = os.path.join(OUTPUT_DIR, filename)
        with open(filepath, "w", encoding="utf-8") as f:
            json.dump(structured_json, f, indent=2, ensure_ascii=False)
        print(f"\nReport successfully saved to: {filepath}")
        print("\n" + "=" * 70)
        print("FINAL STRUCTURED JSON OUTPUT:")
        print("=" * 70)
        print(json.dumps(structured_json, indent=2))
        print("=" * 70)
        return structured_json

    if prior_auth_status in ["Not Found", "Pending Policy Review", "Not Applicable"]:
        prior_auth_status = "Yes"

    doc_info = registry.get_document(doc_key)
    policy_name = doc_info["display_name"] if doc_info else doc_key
    print(f"  Target Policy Document: {doc_key} ({policy_name})")
    print(f"  Routed Section IDs    : {routed_toc_ids}")

    # ---------------------------------------------------------
    # STAGE 3: Scoped Hybrid Retrieval
    # ---------------------------------------------------------
    print("\n[Stage 3: Scoped Hybrid Search (BM25 + Dense)]")
    results = retrieve_scoped_chunks(
        query=query,
        doc_key=doc_key,
        candidate_toc_ids=routed_toc_ids,
        top_k=top_k
    )

    if not results:
        # Self-healing: try candidate #2 from ranked candidates if available
        alt_cands = get_ranked_candidate_sections(query, matched_cpts=matched_cpts, cpt_desc=cpt_desc, max_candidates=4)
        for ac in alt_cands:
            if ac["doc_key"] == doc_key and ac["toc_id"] not in routed_toc_ids:
                print(f"  [Self-Healing] Initial section {routed_toc_ids} returned 0 chunks. Retrying with candidate: [{ac['toc_id']}] {ac['title']}...")
                alt_results = retrieve_scoped_chunks(
                    query=query,
                    doc_key=doc_key,
                    candidate_toc_ids=[ac["toc_id"]],
                    top_k=top_k
                )
                if alt_results:
                    results = alt_results
                    routed_toc_ids = [ac["toc_id"]]
                    break

    print(f"  Retrieved {len(results)} scoped chunks (with condition completion):")
    for i, r in enumerate(results[:5], 1):
        print(f"    {i}. [{r.get('toc_id', 'N/A')}] {r.get('section', '')[:65]}")

    if not results:
        print(f"  [Notice] No retrievable content found in routed sections {routed_toc_ids} of {doc_key}.")
        structured_json = {
            "Prior auth required": prior_auth_status,
            "Policy Name": policy_name,
            "Referred Sections": routed_toc_ids,
            "Medical necessity indications": [],
            "Non-Indications": [],
            "Important criteria & exceptions": [],
            "Documentation required": [],
            "Notice": f"The routed section(s) {routed_toc_ids} in policy '{policy_name}' do not contain clinical coverage criteria."
        }
        os.makedirs(OUTPUT_DIR, exist_ok=True)
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        slug = "".join(c if c.isalnum() or c == " " else "" for c in query)
        slug = "_".join(slug.split())[:50]
        filename = f"{timestamp}_{slug}.json"
        filepath = os.path.join(OUTPUT_DIR, filename)
        with open(filepath, "w", encoding="utf-8") as f:
            json.dump(structured_json, f, indent=2, ensure_ascii=False)
        print(f"\nReport successfully saved to: {filepath}")
        print("\n" + "=" * 70)
        print("FINAL STRUCTURED JSON OUTPUT:")
        print("=" * 70)
        print(json.dumps(structured_json, indent=2))
        print("=" * 70)
        return structured_json

    # ---------------------------------------------------------
    # STAGE 4: Structured Clinical JSON Synthesis
    # ---------------------------------------------------------
    print("\n[Stage 4: Structured Clinical JSON Synthesis]")
    context = build_context(results)
    prompt = build_synthesis_prompt(
        query=query,
        context=context,
        prior_auth_status=prior_auth_status,
        policy_name=policy_name
    )

    raw_response = call_llm(prompt, json_mode=True)
    raw_json = extract_clean_json(raw_response)
    structured_json = normalize_clinical_json(raw_json, prior_auth_status, policy_name)


    # Save output to data/results_new
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    slug = "".join(c if c.isalnum() or c == " " else "" for c in query)
    slug = "_".join(slug.split())[:50]
    filename = f"{timestamp}_{slug}.json"
    filepath = os.path.join(OUTPUT_DIR, filename)

    with open(filepath, "w", encoding="utf-8") as f:
        json.dump(structured_json, f, indent=2, ensure_ascii=False)

    print(f"\nReport successfully saved to: {filepath}")
    print("\n" + "=" * 70)
    print("FINAL STRUCTURED JSON OUTPUT:")
    print("=" * 70)
    print(json.dumps(structured_json, indent=2))
    print("=" * 70)

    return structured_json


# ============================================================
# MAIN
# ============================================================

if __name__ == "__main__":
    if len(sys.argv) > 1:
        user_query = " ".join(sys.argv[1:])
    else:
        user_query = input("Enter your query: ")

    run_rag_pipeline(user_query)