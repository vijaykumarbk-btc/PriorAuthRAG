# Using this skill in Google Antigravity

Good news: Antigravity uses the same `SKILL.md` format (YAML frontmatter +
Markdown body, optional `scripts/`, `references/`, `assets/`) as Claude
Code, so this skill folder works without modification. What differs is
*where you put it* and *how it gets triggered automatically*.

## Installing

Antigravity looks for skills in two scopes:

- **Workspace scope**: `<workspace-root>/.agent/skills/auto-doc-commits/`
- **User scope**: your Antigravity user config directory (check
  Antigravity's own docs/settings for the exact path on your OS — this can
  change between versions, so this file intentionally doesn't guess it).

For a per-repo doc workflow, workspace scope is almost certainly what you
want: copy this whole folder to
`<your-repo>/.agent/skills/auto-doc-commits/`.

## How triggering differs from Claude Code

Antigravity skills are **agent-triggered by semantic matching** against the
skill's `description` — the agent decides to consult a skill when a
request seems to match, the same way Claude Code does. There is currently
no confirmed simple shell command like Claude Code's `claude -p "..." --skill
X` for kicking off a specific skill headlessly from a git hook.

That's why `scripts/post-commit-hook.sh` doesn't try to invoke Antigravity
directly for you. Instead it drops `.doc-agent/pending-commit.flag`, and
this skill's Step 0 tells the agent to look for that flag. Practically,
that means:

1. You commit as normal; the git hook drops the flag.
2. Next time you're in Antigravity working in this repo (or you explicitly
   open the agent and say something like "check for pending docs"), the
   agent notices the flag, and per this skill's pushy description, treats
   it as a standing instruction to run the draft workflow.
3. You still get the same draft → approve → apply flow as in Claude Code.

## If Antigravity's own trigger/hook system fits better

The Antigravity Python SDK exposes a `triggers.py` pattern for "running
background checks and periodic tasks," and a `hooks.py` pattern for
`pre_turn`/`post_turn` events, plus a `human_in_the_loop.py` pattern for
pausing for confirmation. If your Antigravity setup uses the SDK directly
(rather than the IDE's built-in skill-triggering), those are the more
"native" places to wire in "run on every commit, then wait for human
confirmation before applying" — which maps directly onto Steps 3–4 of this
skill. This document doesn't include exact code for that because the
SDK's API surface may have moved since this was written — check
Antigravity's current SDK docs/examples (`hooks.py`, `triggers.py`,
`human_in_the_loop.py`) before wiring it that way.

Either approach (flag-file + semantic trigger, or native SDK
triggers/hooks) is compatible with the rest of this skill unchanged —
they only affect *when* the agent starts Step 0, not what it does once
it's running.
