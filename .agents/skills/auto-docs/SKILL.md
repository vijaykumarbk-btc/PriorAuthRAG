---
name: auto-docs
description: >
  Comprehensive documentation suite for project structure, Git history from repo inception, and automated semantic changelog/feature drafting. Use this skill when asked to "document the project", "generate project docs", "document recent commits", "update changelog", "scan project structure", or when commits land and need to be documented. Combines deterministic structural/git-history generation with LLM-driven semantic feature documentation and changelog drafting into the documentation/ folder.
---

# Auto-Docs: Unified Project & Git Documentation Suite

This skill provides a **dual-engine documentation architecture** for the project, saving all output into the `documentation/` directory:

1. **Engine 1: Automated Snapshot & Git Metric Generator (Deterministic)**
   - Scans full project directory tree and package dependencies &rarr; `documentation/PROJECT_STRUCTURE.md`
   - Parses Git commits from initial root commit to `HEAD` &rarr; `documentation/GIT_HISTORY.md`
   - Zero LLM tokens required; executes via fast Node.js scripts or CLI commands.

2. **Engine 2: Semantic Feature & Changelog Drafter (AI-Driven)**
   - Analyzes code diffs and commit history since `.doc-agent/last-commit.txt`.
   - Generates human-readable, Keep-a-Changelog style entries &rarr; `documentation/CHANGELOG.md`.
   - Produces technical feature guides & code usage &rarr; `documentation/features/<feature>.md`.
   - Summarizes user-facing release highlights &rarr; `documentation/RELEASE_NOTES.md`.
   - **Safety First**: Drafts are staged in `.doc-agent/draft-<range>.md` and require human approval before applying to real files.

---

## Quick Command Reference

```bash
# Run deterministic documentation (Structure + Git History)
npm run update-docs

# Run only Git History from root commit to HEAD
npm run update-history

# Run only Project Structure tree
npm run update-structure
```

---

## Workflow: Semantic Commit & Feature Documentation

Whenever new commits have landed, or when the user asks to *"document the changes"*, *"update the changelog"*, or *"write docs for this commit"*, follow these steps:

### Step 0: Check Pending State
```bash
mkdir -p .doc-agent
cat .doc-agent/last-commit.txt 2>/dev/null || echo "(none yet — first run)"
if [ -f .doc-agent/pending-commit.flag ]; then
  echo "Commit(s) landed since last review:"; cat .doc-agent/pending-commit.flag
fi
```
If `.doc-agent/last-commit.txt` does not exist, use the initial commit (`git rev-list --max-parents=0 HEAD`) or ask the user where to start.

### Step 1: Analyze What Changed
```bash
LAST=$(cat .doc-agent/last-commit.txt 2>/dev/null || git rev-list --max-parents=0 HEAD)
git log "$LAST"..HEAD --oneline
git diff "$LAST"..HEAD --stat
git diff "$LAST"..HEAD
```
- Read full diffs for meaningful context.
- Classify changes into: **Added (new features)**, **Changed (modifications)**, **Fixed (bugfixes)**, or **Removed/Deprecated**.
- Skip pure internal chores/CI from user-facing logs.

### Step 2: Draft Output in Staging
Never write directly to final doc files without approval. Write a draft staging file:
```
.doc-agent/draft-<short-sha-range>.md
```
Using the templates in `references/output-formats.md`:
1. **Changelog additions** (`documentation/CHANGELOG.md`)
2. **Feature guides** (`documentation/features/<slug>.md`)
3. **Release notes** (`documentation/RELEASE_NOTES.md`)
4. **Notes / Uncertainty** (explicitly flag anything ambiguous)

### Step 3: Stop and Request Human Approval
Present the staged draft to the user and ask:
> *"I have drafted documentation for commits `<X>..<Y>`. Would you like me to apply these updates to `documentation/CHANGELOG.md`, `documentation/features/`, and `documentation/RELEASE_NOTES.md`?"*

Stop execution and wait for the user's response.

### Step 4: Apply and Advance State
Upon receiving confirmation:
1. Prepend entries into `documentation/CHANGELOG.md` under `## [Unreleased]`.
2. Write/update files in `documentation/features/`.
3. Append notes to `documentation/RELEASE_NOTES.md`.
4. Delete the staged `.doc-agent/draft-<range>.md` and `.doc-agent/pending-commit.flag`.
5. Update `.doc-agent/last-commit.txt` to the current `HEAD` SHA:
   ```bash
   git rev-parse HEAD > .doc-agent/last-commit.txt
   ```
6. Regenerate structural & history docs:
   ```bash
   npm run update-docs
   ```

---

## Git Post-Commit Hook Integration

To automatically flag new commits as they happen:
```bash
cp .agents/skills/auto-docs/scripts/post-commit-hook.sh .git/hooks/post-commit
chmod +x .git/hooks/post-commit
```
After each commit, the hook marks `.doc-agent/pending-commit.flag` so the assistant notices pending docs immediately on next launch.
