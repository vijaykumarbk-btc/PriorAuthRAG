# State file: `.doc-agent/last-commit.txt`

A single line containing the full SHA of the last commit whose changes were
**approved and merged** into the real docs (CHANGELOG.md, docs/features/,
RELEASE_NOTES.md).

Rules:
- This file only advances in Step 4 of the skill, after human approval —
  never write to it in Step 1–3.
- If it doesn't exist, treat this as the first run. Ask the user (or infer
  from tags) where documentation history should start, rather than trying
  to document the entire lifetime of the repo by default.
- Add `.doc-agent/draft-*.md` files to version control or `.gitignore` —
  either is fine, but be consistent: if the team wants pending drafts
  visible in PRs for review, commit them; if they're purely a local
  reminder, gitignore them. Ask the user which they'd prefer the first time
  this comes up, and note the answer in `.doc-agent/README.md` (create it)
  so future runs don't have to ask again.
