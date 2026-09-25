# Output Templates for `documentation/`

All documentation artifacts are maintained under the `documentation/` directory.

## 1. CHANGELOG.md (`documentation/CHANGELOG.md`)

Append under the `## [Unreleased]` heading (create it at the top of the file, right after the title, if it doesn't exist):

```markdown
## [Unreleased]

### Added
- Short, user-facing description of the new capability. (#<short-sha>)

### Changed
- What changed in existing behavior and why it matters to a user. (#<short-sha>)

### Fixed
- What was broken and now isn't. (#<short-sha>)

### Removed
- What was removed or deprecated, and what to use instead. (#<short-sha>)
```

Omit any subsection with nothing in it. One line per commit (or per logical change, if one commit bundles several).

## 2. Feature Docs (`documentation/features/<feature-slug>.md`)

```markdown
# <Feature name>

<One or two sentence summary — what it does and why someone would use it.>

## Usage

<Concrete example — a code snippet, CLI invocation, or config, showing the
feature in use. Prefer a real example pulled from tests or the diff over an
invented one.>

## Notes

<Anything a user needs to know: limitations, migration steps if this
replaces old behavior, links to related features.>

---
*Documented from commit <sha> on <date>.*
```

If the feature already has a doc page, append a `## Changes in <date>` subsection instead of rewriting the whole page.

## 3. Release Notes Summary (`documentation/RELEASE_NOTES.md`)

```markdown
## <date or version placeholder>

<One short paragraph, written for end users, not developers. Lead with the
most user-visible change. Skip internal refactors entirely — release notes
are not a changelog.>
```

## 4. Draft File Wrapper (`.doc-agent/draft-<range>.md`)

When staging a draft before approval, wrap the sections above like this so the human reviewing it can inspect what's pending:

```markdown
# Draft Documentation for <short-sha-1>..<short-sha-2>
Generated: <date>
Status: PENDING APPROVAL

## 1. Changelog Additions
<template 1 content>

## 2. Feature Docs
<template 2 content, one block per feature>

## 3. Release Notes
<template 3 content>

## 4. Notes / Uncertainty
<anything you weren't sure about — call it out here rather than guessing
silently in the sections above.>
```
