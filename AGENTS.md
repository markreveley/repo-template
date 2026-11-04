# <repo>: working rules

Rules for any agent (Claude Code, Codex, Gemini) and for people. The global
rules in `~/.dotfiles/agents/AGENTS.md` apply first; this file adds the
repo's own. `CLAUDE.md` imports this file and adds nothing.

## Read first

1. `README.md`: what the repo is and the table of what is where.
2. `next-agents.md` and `next-operator.md`: where the last thread stopped.
   `/start` reads them; `/end` rewrites them. What to work on comes from
   `next-agents.md`, not from reading other documents.
3. The governing documents in `md/governance/` that exist: `ARCHITECTURE.md` before
   changing how the parts fit, `POLICY.md` before any change (its rules are
   numbered so you can cite them), `SCHEMA.md` before writing data the repo
   holds, `PROCEDURE.md` before running one of its methods.

## Where things are

- `<code or data folders>`: <one line each>.
- `md/`: every document about the repo. `md/README.md` lists the folders
  and the naming conventions; each folder's README says what belongs in it.
- `LOCAL.md` (git-ignored): names of private projects, local paths, and
  anything else that stays on this machine. This repo is <public|private>;
  <if public:> name no private project in any tracked file.

## Working

- Changes reach `main` through a PR, unless `next-agents.md` says the work
  is on `main`. `/end` commits where the work is and opens the PR.
- Before changing a contract (`SCHEMA.md`, a CLI, a file format), check who
  reads it: <downstream repos, CI>.
- Tests: `<command>`. Run them before a PR.
- Threads are archived at `/end` into `md/threads/`, redacted with
  `md/threads/redact.json` (git-ignored). `md/threads/README.md` says how.
- Worktrees go under `.claude/worktrees/` (git-ignored). Never touch
  another session's worktree.

## This repo's own rules

- <rule, with its reason>
