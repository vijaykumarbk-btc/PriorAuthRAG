#!/usr/bin/env python3
"""
ingest_policy.py
----------------
Unified CLI ingestion tool for adding new medical coverage policies.
Automates Steps 1 through 7 of the ingestion workflow:
  1. PDF Ingestion & Tiered Parsing (fallback.pipeline)
  2. TOC Extraction (hierarchical-processing/toc_v2.py)
  3. Semantic Markdown Chunking (hierarchical-processing/chunking_heirarchical.py)
  4. TOC-to-Chunk Mapping (hierarchical-processing/chunk_toc_mapper.py)
  5. Dense Embedding Generation (hierarchical-processing/embedding_with_section.py)
  6. BM25 Lexical Index Building (hierarchical-processing/build_bm25.py)
  7. Manifest Registration (hierarchical-processing/policies_manifest.json)

Usage:
  python ingest_policy.py <path_to_pdf> --name "<display_name>" [--doc-key <key>]
  python ingest_policy.py extra_pdfs/Cigna_Knee.pdf --name "Cigna Knee Surgery"
  python ingest_policy.py extra_pdfs/Cigna_Knee.pdf --dry-run
"""

import os
import sys
import re
import json
import shutil
import argparse
import subprocess
from pathlib import Path
from typing import Dict, Any, Optional

PROJECT_ROOT = Path(__file__).resolve().parent
HIERARCHICAL_DIR = PROJECT_ROOT / "hierarchical-processing"
MANIFEST_PATH = HIERARCHICAL_DIR / "policies_manifest.json"

TOC_SCRIPT = HIERARCHICAL_DIR / "toc_v2.py"
CHUNKING_SCRIPT = HIERARCHICAL_DIR / "chunking_heirarchical.py"
MAPPER_SCRIPT = HIERARCHICAL_DIR / "chunk_toc_mapper.py"
EMBEDDING_SCRIPT = HIERARCHICAL_DIR / "embedding_with_section.py"
BM25_SCRIPT = HIERARCHICAL_DIR / "build_bm25.py"


def clean_slug(name: str) -> str:
    """Sanitize string into a safe document slug/key."""
    s = re.sub(r"[^\w\s-]", "", name).strip()
    s = re.sub(r"[-\s]+", "_", s)
    return s


def print_banner(stage_num: int, title: str):
    print("\n" + "=" * 70)
    print(f" STAGE {stage_num}: {title.upper()}")
    print("=" * 70)


def execute_cmd(cmd: list, env: Optional[dict] = None, cwd: Optional[Path] = None):
    """Execute a CLI command with live stdout/stderr streaming."""
    cwd = cwd or PROJECT_ROOT
    cmd_str = " ".join(str(c) for c in cmd)
    print(f"\n[EXEC] cwd={cwd}")
    print(f"[EXEC] {cmd_str}\n")
    proc = subprocess.Popen(
        cmd,
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        text=True,
        bufsize=1,
        env=env or os.environ.copy(),
        cwd=cwd
    )
    for line in iter(proc.stdout.readline, ""):
        print(line, end="", flush=True)
    proc.stdout.close()
    returncode = proc.wait()
    if returncode != 0:
        raise RuntimeError(f"Command failed with exit code {returncode}:\n  {cmd_str}")


def stage_1_parse_pdf(pdf_path: Path, output_dir: Path, page_threshold: int):
    """Run fallback.pipeline to parse PDF into hierarchical JSON & Markdown."""
    print(f"Parsing PDF: {pdf_path}")
    print(f"Destination output directory: {output_dir}")
    print(f"Page threshold: {page_threshold}")

    runner_code = f"""
import sys
from pathlib import Path
from fallback.pipeline import process_pdf
from fallback.config import PipelineConfig

pdf = Path(r'{pdf_path.resolve()}')
out_dir = Path(r'{output_dir.resolve()}')
cfg = PipelineConfig(page_count_threshold={page_threshold})
res = process_pdf(pdf, out_dir, cfg)
print(f"PIPELINE_COMPLETE: used={{res.pipeline_used}}, pages={{res.page_count}}, blocks={{res.total_blocks}}")
"""
    execute_cmd([sys.executable, "-c", runner_code], cwd=PROJECT_ROOT)


def normalize_hierarchical_json(json_file: Path, pdf_path: Path, output_dir: Path):
    """Ensure hierarchical.json matches the standard dict format expected by toc_v2.py."""
    if not json_file.exists():
        return
    with open(json_file, "r", encoding="utf-8") as f:
        data = json.load(f)

    if isinstance(data, list):
        print(f"[INGEST] Normalizing {json_file.name} to standard {{document, blocks}} schema...")
        total_pages = None
        qa_file = output_dir / f"{pdf_path.stem}.qa_report.json"
        if qa_file.exists():
            try:
                with open(qa_file, "r", encoding="utf-8") as qf:
                    qa = json.load(qf)
                    total_pages = qa.get("page_count")
            except Exception:
                pass

        wrapped = {
            "document": {
                "source": pdf_path.name,
                "source_path": str(pdf_path.resolve()),
                "total_pages": total_pages,
            },
            "blocks": data
        }
        with open(json_file, "w", encoding="utf-8") as f:
            json.dump(wrapped, f, indent=2, ensure_ascii=False)
        print(f"[INGEST] Successfully normalized {json_file.name}.")


def stage_2_extract_toc(json_file: Path, toc_json_file: Path, toc_tree_file: Path, pdf_path: Path, output_dir: Path):
    """Extract Table of Contents tree using toc_v2.py."""
    normalize_hierarchical_json(json_file, pdf_path, output_dir)
    toc_json_file.parent.mkdir(parents=True, exist_ok=True)
    cmd = [
        sys.executable,
        str(TOC_SCRIPT),
        str(json_file.resolve()),
        str(toc_json_file.resolve()),
        str(toc_tree_file.resolve())
    ]
    execute_cmd(cmd, cwd=PROJECT_ROOT)


def stage_3_chunk_markdown(md_dir: Path, chunks_dir: Path, stem: str) -> Path:
    """Split markdown into criteria-aware semantic chunks."""
    chunks_dir.mkdir(parents=True, exist_ok=True)
    env = os.environ.copy()
    env["CHUNKING_INPUT_DIR"] = str(md_dir.resolve())
    env["CHUNKING_OUTPUT_DIR"] = str(chunks_dir.resolve())

    cmd = [sys.executable, str(CHUNKING_SCRIPT)]
    execute_cmd(cmd, env=env, cwd=HIERARCHICAL_DIR)

    # Locate generated chunks file
    expected_primary = chunks_dir / f"{stem}.hierarchical_chunks.json"
    expected_fallback = chunks_dir / f"{stem}_chunks.json"

    if expected_primary.exists():
        return expected_primary
    elif expected_fallback.exists():
        return expected_fallback
    else:
        # Check any json generated in chunks_dir
        found = list(chunks_dir.glob("*.json"))
        if found:
            return found[0]
        raise FileNotFoundError(f"No chunk file generated in {chunks_dir}")


def stage_4_map_toc_chunks(chunks_file: Path, toc_json_file: Path, enriched_chunks_file: Path):
    """Stamp chunks with exact TOC IDs and heading breadcrumbs."""
    enriched_chunks_file.parent.mkdir(parents=True, exist_ok=True)
    cmd = [
        sys.executable,
        str(MAPPER_SCRIPT),
        str(chunks_file.resolve()),
        str(toc_json_file.resolve()),
        str(enriched_chunks_file.resolve())
    ]
    execute_cmd(cmd, cwd=PROJECT_ROOT)


def stage_5_generate_embeddings(enriched_chunks_file: Path, embeddings_file: Path, metadata_file: Path):
    """Generate dense embeddings with section hierarchy breadcrumbs."""
    embeddings_file.parent.mkdir(parents=True, exist_ok=True)
    metadata_file.parent.mkdir(parents=True, exist_ok=True)
    cmd = [
        sys.executable,
        str(EMBEDDING_SCRIPT),
        str(enriched_chunks_file.resolve()),
        str(embeddings_file.resolve()),
        str(metadata_file.resolve())
    ]
    execute_cmd(cmd, cwd=PROJECT_ROOT)


def stage_6_build_bm25(metadata_file: Path, bm25_file: Path):
    """Build section-aware Rank-BM25 lexical index."""
    bm25_file.parent.mkdir(parents=True, exist_ok=True)
    cmd = [
        sys.executable,
        str(BM25_SCRIPT),
        str(metadata_file.resolve()),
        str(bm25_file.resolve())
    ]
    execute_cmd(cmd, cwd=PROJECT_ROOT)


def stage_7_register_manifest(
    doc_key: str,
    display_name: str,
    toc_file: Path,
    metadata_file: Path,
    embeddings_file: Path,
    bm25_file: Path
):
    """Safely register policy in policies_manifest.json with backup."""
    if not MANIFEST_PATH.exists():
        manifest_data = {"policies": []}
    else:
        # Create backup
        backup_path = MANIFEST_PATH.with_suffix(".json.bak")
        shutil.copyfile(MANIFEST_PATH, backup_path)
        print(f"Created backup of policies manifest: {backup_path}")
        with open(MANIFEST_PATH, "r", encoding="utf-8") as f:
            manifest_data = json.load(f)

    # Compute paths relative to hierarchical-processing/
    manifest_dir = MANIFEST_PATH.parent
    toc_rel = os.path.relpath(toc_file, manifest_dir)
    meta_rel = os.path.relpath(metadata_file, manifest_dir)
    emb_rel = os.path.relpath(embeddings_file, manifest_dir)
    bm25_rel = os.path.relpath(bm25_file, manifest_dir)

    new_entry = {
        "doc_key": doc_key,
        "display_name": display_name,
        "toc_file": toc_rel,
        "metadata_file": meta_rel,
        "embeddings_file": emb_rel,
        "bm25_file": bm25_rel
    }

    policies = manifest_data.setdefault("policies", [])
    updated = False
    for i, p in enumerate(policies):
        if p.get("doc_key") == doc_key:
            policies[i] = new_entry
            updated = True
            print(f"Updated existing registration for doc_key '{doc_key}' in manifest.")
            break

    if not updated:
        policies.append(new_entry)
        print(f"Appended new registration for doc_key '{doc_key}' to manifest.")

    with open(MANIFEST_PATH, "w", encoding="utf-8") as f:
        json.dump(manifest_data, f, indent=2, ensure_ascii=False)
        f.write("\n")

    print(f"Successfully saved manifest: {MANIFEST_PATH}")


def main():
    parser = argparse.ArgumentParser(
        description="Unified Ingestion Pipeline for Medical Coverage Policies (Steps 1-7)."
    )
    parser.add_argument("pdf_path", type=str, help="Path to input policy PDF")
    parser.add_argument("--name", "--display-name", dest="display_name", type=str, help="Human-friendly display name")
    parser.add_argument("--doc-key", dest="doc_key", type=str, help="Policy identifier slug (e.g., Cigna_Knee)")
    parser.add_argument("--output-dir", dest="output_dir", type=str, help="Root folder for policy artifacts (default: data/policies/<doc_key>)")
    parser.add_argument("--page-threshold", dest="page_threshold", type=int, default=300, help="Page threshold for tiered fallback vs Docling (default: 300)")
    parser.add_argument("--skip-to", dest="skip_to", type=int, choices=range(1, 8), default=1, help="Resume pipeline starting from stage N (1-7)")
    parser.add_argument("--dry-run", dest="dry_run", action="store_true", help="Print plan and paths without executing")

    args = parser.parse_args()

    pdf_path = Path(args.pdf_path).resolve()
    if not pdf_path.exists() or not pdf_path.is_file():
        print(f"Error: PDF file not found: {pdf_path}", file=sys.stderr)
        sys.exit(1)

    stem = pdf_path.stem.replace(".cleaned", "")
    doc_key = args.doc_key or clean_slug(stem)
    display_name = args.display_name or doc_key.replace("_", " ")

    # Directory Structure
    base_out = Path(args.output_dir).resolve() if args.output_dir else (PROJECT_ROOT / "data" / "policies" / doc_key)
    raw_dir = base_out / "raw"
    output_dir = base_out / "output"
    toc_dir = base_out / "toc"
    chunks_dir = base_out / "chunks"
    embeddings_dir = base_out / "embeddings"
    bm25_dir = base_out / "bm25"

    # Artifact file paths
    hierarchical_json = output_dir / f"{pdf_path.stem}.hierarchical.json"
    hierarchical_md = output_dir / f"{pdf_path.stem}.hierarchical.md"
    toc_json = toc_dir / f"{doc_key}_toc_output.json"
    toc_tree = toc_dir / f"{doc_key}_toc_tree.txt"
    chunks_file = chunks_dir / f"{pdf_path.stem}.hierarchical_chunks.json"
    enriched_chunks = chunks_dir / f"{doc_key}_enriched_chunks.json"
    embeddings_file = embeddings_dir / f"{doc_key}_embeddings.npy"
    metadata_file = embeddings_dir / f"{doc_key}_metadata.json"
    bm25_file = bm25_dir / f"{doc_key}_bm25.pkl"

    print("=" * 70)
    print(" UNIFIED POLICY INGESTION PIPELINE")
    print("=" * 70)
    print(f"Source PDF       : {pdf_path}")
    print(f"Doc Key          : {doc_key}")
    print(f"Display Name     : {display_name}")
    print(f"Base Output Dir  : {base_out}")
    print(f"Page Threshold   : {args.page_threshold}")
    print(f"Starting Stage   : {args.skip_to}")
    print(f"Dry Run          : {args.dry_run}")
    print("-" * 70)

    if args.dry_run:
        print("\n[DRY RUN PLAN]")
        print(f"  Stage 1: Parse PDF -> {hierarchical_md} & {hierarchical_json}")
        print(f"  Stage 2: Extract TOC -> {toc_json} & {toc_tree}")
        print(f"  Stage 3: Semantic Chunking -> {chunks_file}")
        print(f"  Stage 4: TOC-Chunk Mapping -> {enriched_chunks}")
        print(f"  Stage 5: Generate Dense Embeddings -> {embeddings_file} & {metadata_file}")
        print(f"  Stage 6: Build BM25 Index -> {bm25_file}")
        print(f"  Stage 7: Register policy in {MANIFEST_PATH}")
        print("\nDry run completed successfully. No files modified.")
        return

    # Create directories
    for d in [base_out, raw_dir, output_dir, toc_dir, chunks_dir, embeddings_dir, bm25_dir]:
        d.mkdir(parents=True, exist_ok=True)

    # Optional: copy or symlink raw PDF
    raw_pdf_dest = raw_dir / pdf_path.name
    if not raw_pdf_dest.exists():
        try:
            shutil.copyfile(pdf_path, raw_pdf_dest)
            print(f"Saved raw PDF copy to: {raw_pdf_dest}")
        except Exception as e:
            print(f"Warning: Could not copy raw PDF to {raw_pdf_dest}: {e}")

    try:
        # Stage 1: Parse PDF
        if args.skip_to <= 1:
            print_banner(1, "Parse PDF via Tiered Router")
            stage_1_parse_pdf(pdf_path, output_dir, args.page_threshold)
            if not hierarchical_json.exists():
                raise FileNotFoundError(f"Stage 1 failed to produce {hierarchical_json}")

        # Stage 2: Extract TOC
        if args.skip_to <= 2:
            print_banner(2, "Extract Table of Contents (TOC)")
            stage_2_extract_toc(hierarchical_json, toc_json, toc_tree, pdf_path, output_dir)
            if not toc_json.exists():
                raise FileNotFoundError(f"Stage 2 failed to produce {toc_json}")

        # Stage 3: Semantic Chunking
        actual_chunks_file = chunks_file
        if args.skip_to <= 3:
            print_banner(3, "Criteria-Aware Semantic Chunking")
            actual_chunks_file = stage_3_chunk_markdown(output_dir, chunks_dir, pdf_path.stem)
        elif not actual_chunks_file.exists():
            actual_chunks_file = chunks_dir / f"{pdf_path.stem}_chunks.json"

        # Stage 4: Map TOC to Chunks
        if args.skip_to <= 4:
            print_banner(4, "Map TOC to Chunks & Enrich Context")
            stage_4_map_toc_chunks(actual_chunks_file, toc_json, enriched_chunks)
            if not enriched_chunks.exists():
                raise FileNotFoundError(f"Stage 4 failed to produce {enriched_chunks}")

        # Stage 5: Dense Embeddings
        if args.skip_to <= 5:
            print_banner(5, "Generate Dense Embeddings & Chunk Metadata")
            stage_5_generate_embeddings(enriched_chunks, embeddings_file, metadata_file)
            if not embeddings_file.exists() or not metadata_file.exists():
                raise FileNotFoundError(f"Stage 5 failed to produce {embeddings_file} or {metadata_file}")

        # Stage 6: Build BM25 Index
        if args.skip_to <= 6:
            print_banner(6, "Build BM25 Lexical Index")
            stage_6_build_bm25(metadata_file, bm25_file)
            if not bm25_file.exists():
                raise FileNotFoundError(f"Stage 6 failed to produce {bm25_file}")

        # Stage 7: Register in Manifest
        if args.skip_to <= 7:
            print_banner(7, "Register Policy in Manifest")
            stage_7_register_manifest(
                doc_key=doc_key,
                display_name=display_name,
                toc_file=toc_json,
                metadata_file=metadata_file,
                embeddings_file=embeddings_file,
                bm25_file=bm25_file
            )

        print("\n" + "=" * 70)
        print(" 🎉 INGESTION COMPLETE! Policy is ready for instant querying.")
        print(f" Doc Key     : {doc_key}")
        print(f" Display Name: {display_name}")
        print(f" Manifest    : {MANIFEST_PATH}")
        print(f"\n Try querying it with:")
        print(f"   ./venv/bin/python retrieval-hierarchical.py \"<your query>\"")
        print("=" * 70 + "\n")

    except Exception as e:
        print(f"\n❌ INGESTION FAILED at Stage: {e}", file=sys.stderr)
        print("You can inspect the error above and resume ingestion after fixing using:")
        print(f"  ./venv/bin/python ingest_policy.py {pdf_path} --skip-to <stage_number>", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
