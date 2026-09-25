# PriorAuthRAG Documentation Index

Comprehensive documentation suite generated for **PriorAuthRAG**, covering project structure, per-commit audit folders from inception, and technical architecture guides.

---

## 1. Project & Repository Maps
- **[`commits/`](./commits/README.md)**: **Modular Per-Commit Documentation Folders** (each of the 20 commits has a dedicated folder with metadata, diff statistics, and changed file lists).
- **[`GIT_HISTORY.md`](./GIT_HISTORY.md)**: Master chronological timeline audit log linking to all 20 individual commit folders.
- **[`PROJECT_STRUCTURE.md`](./PROJECT_STRUCTURE.md)**: Full interactive directory tree with clickable links, scripts, and runtime dependencies.

---

## 2. Release & Versioning Records
- **[`CHANGELOG.md`](./CHANGELOG.md)**: Keep-a-Changelog formatted records of all major milestones, additions, changes, and bug fixes across time.
- **[`RELEASE_NOTES.md`](./RELEASE_NOTES.md)**: High-level version milestones written for end-users and stakeholders.

---

## 3. Technical Feature Guides
- **[`features/hierarchical-rag-engine.md`](./features/hierarchical-rag-engine.md)**: Architectural guide for hierarchical chunking and multi-tier medical policy retrieval.
- **[`features/clinical-policy-pipelines.md`](./features/clinical-policy-pipelines.md)**: Guideline-specific ingestion pipelines (Lumbar, Lab Management, Radiation Oncology, Knee).
- **[`features/fallback-parser-engine.md`](./features/fallback-parser-engine.md)**: Non-OCR direct layout parser for complex multi-page tabular PDF policies.
- **[`features/hybrid-search-retrieval.md`](./features/hybrid-search-retrieval.md)**: Dual BM25 lexical + dense vector embedding retrieval mechanism.
- **[`features/evaluation-and-benchmarking.md`](./features/evaluation-and-benchmarking.md)**: 30-question evaluation report and clinical benchmark test runners.

---

## Maintenance Commands
```bash
# Update all documentation (Structure + Git History + Commit Folders)
npm run update-docs

# Update only Git history & commit folders from inception
npm run update-history

# Update only project structure tree
npm run update-structure
```
