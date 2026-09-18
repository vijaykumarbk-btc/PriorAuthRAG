Here is the step-by-step roadmap to migrate your existing vector storage and retrieval pipeline from `.npy` + JSON metadata to **ChromaDB** without re-computing embeddings.

---

### Step 1: Environment & Dependency Setup
1. **Install ChromaDB** in your active virtual environment (`pip install chromadb`).
2. **Choose the Architecture Pattern**:
   * **Local Embedded Persistent Storage** *(Recommended for this setup)*: Uses `chromadb.PersistentClient(path="./chroma_db")` storing data directly on disk in SQLite + Parquet.
   * **Client/Server Mode**: For multi-process or containerized deployments (`chromadb.HttpClient(...)`).

---

### Step 2: Collection & Metadata Design
1. **Decide on Collection Strategy**:
   * **Option A (Per-Policy Collections)**: e.g., `policy_cigna_acdf`, `policy_cigna_lab_management`. Clean isolation, matches current folder structure.
   * **Option B (Unified Multi-Tenant Collection)**: A single `clinical_policies` collection with `doc_key` / `policy_id` as metadata filter. Enables cross-policy querying.
2. **Flatten & Sanitize Metadata**:
   * **Constraint**: ChromaDB only supports primitive types (`str`, `int`, `float`, `bool`) in `metadatas`.
   * Any lists or nested dictionaries in your `*_metadata.json` (such as `section_path` lists, CPT codes arrays, or tables) must be converted:
     * Lists $\rightarrow$ Delimited strings (e.g., `"Test Specific Guidelines > BRCA Analysis"`) or `json.dumps(...)`.
     * `toc_id`, `chunk_type` (`criteria`, `table`, `text`), `page_start`, `page_end` $\rightarrow$ Standard primitives.

---

### Step 3: Fast Ingestion / Migration Script (Zero Re-Embedding)
Since embeddings are already computed and saved in `.npy` files:
1. **Load Existing Assets**:
   * Read `*.npy` (vectors of shape `(N, 768)`).
   * Read `*_metadata.json` (metadata for $N$ chunks).
2. **Batch Upsert into ChromaDB**:
   * Insert in batches (e.g., 500–1000 items) using:
     ```python
     collection.upsert(
         ids=batch_chunk_ids,
         embeddings=batch_vectors.tolist(),
         documents=batch_text_chunks,
         metadatas=batch_sanitized_metadatas,
     )
     ```
   * *Benefit: Instant migration without spending GPU/CPU compute on Ollama embedding calls.*

---

### Step 4: Update the Ingestion Pipeline for New Policies
Update your embedding script (e.g., [`embedding_with_section.py`](file:///home/vijaykumar/Desktop/project2/embedding_with_section.py) / [`ingest_policy.py`](file:///home/vijaykumar/Desktop/project2/ingest_policy.py)):
1. After generating batch embeddings from Ollama, write directly to the Chroma collection instead of exporting separate `.npy` and `.metadata.json` files.
2. Maintain chunk-to-TOC relationship via the `toc_id` metadata attribute.

---

### Step 5: Update the Retrieval Pipeline (`retrieval-hierarchical.py`)
1. **Replace In-Memory Matrix Multiplication**:
   * Remove loading `.npy` arrays into RAM and manual dot-product / cosine similarity calculations (`np.dot(matrix, query_vec)`).
2. **Implement Native Filtered Vector Search**:
   * In Stage 3 (Scoped Hybrid Retrieval), pass the Ollama query vector directly to `collection.query`:
     ```python
     results = collection.query(
         query_embeddings=[query_vector],
         n_results=top_k,
         where={"toc_id": {"$in": scoped_toc_ids}},  # Hierarchical scope filtering
     )
     ```
3. **Preserve Hybrid Scoring (BM25 + Dense)**:
   * Keep the BM25 index as a separate lexical ranker, or run both concurrently and merge scores using **Reciprocal Rank Fusion (RRF)**.

---

### Step 6: Update Policy Manifest & Configuration
1. In [`hierarchical-processing/policies_manifest.json`](file:///home/vijaykumar/Desktop/project2/hierarchical-processing/policies_manifest.json), replace file paths:
   * Remove `embeddings_file` (`.npy`) and `metadata_file` (`.json`).
   * Add `chroma_collection_name` (or point to the common Chroma persist directory).

---

### Step 7: Parity Verification & Performance Check
1. **Parity Testing**: Run the baseline query (*"What are the criteria for BRCA1 and BRCA2 genetic testing?"*) and verify that top-ranked chunks match the previous `.npy` retrieval results.
2. **Benchmark Comparison**: Run [`eval_lab_management_benchmark.py`](file:///home/vijaykumar/Desktop/project2/eval_lab_management_benchmark.py) to confirm latency, memory usage, and precision stay equal to or better than the NumPy-based baseline.