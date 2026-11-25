# <repo>: working rules

Rules for any agent (Claude Code, Codex, Gemini) and for people. The global
rules in `~/.dotfiles/agents/AGENTS.md` apply first; this file adds the
repo's own. `CLAUDE.md` imports this file and adds nothing.

## Read first

1. `README.md`: what the repo is and the table of what is where.
2. `next.md` (what to do next, in order) and **State** at the end of this
   file (what is true now): where the last thread stopped. `/start` reads
   them; `/end` rewrites them. What to work on comes from `next.md`, not
   from reading other documents. Change `next.md` with `update-next` (R30).
3. The governing documents in `md/governance/` that are not empty: `ARCHITECTURE.md` before
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

- Changes go straight to `main`, with no PR. Unless the operator has
  explicitly asked for the push, ask in the thread first and push once they
  say yes. `/end` commits where the work is and, with that go-ahead, pushes.
- Before changing a contract (`SCHEMA.md`, a CLI, a file format), check who
  reads it: <downstream repos, CI>.
- Tests: `<command>`. Run them before pushing.
- Threads are archived at `/end` into the private `thread-archive` repo,
  under `threads/<repo>/`, not into this repo.
- Worktrees go under `.claude/worktrees/` (git-ignored). Never touch
  another session's worktree.

## This repo's own rules

- <rule, with its reason>

## State

<!-- repo-template's own state. A client repo empties this section and Environment facts and runs /start (README, "Adopting the template", step 3). -->

- This repo is the layout template and its rules; `README.md` is the contract, `md/analysis/2026-11-04-layout-survey/` the survey and decisions behind it.
- `next.md` and this State are this repo's own. A client repo replaces them (README, "Adopting the template").
- On `main`, pushed, clean. Changes go straight to `main` (policy changed 2026-11-21, R29); #5 to #8 were PRs, merged 4 Nov 2026.
- `bin/check-layout.sh` passes here.
- The README's rules are R1 to R30, one claim each; the check table and "What it does not check" map every check to a rule. Numbers are never reused.
- All five governing documents are required (R10); an unused one holds only its title and its pinned block (R12). `md/README.md`, the folder READMEs and the governing documents all carry pins (R13). Each governing document has a `**Changed by:**` line.
- The handoff is a single `next.md` (the list only) plus this State (R1, R30), since 2026-11-24. It replaced `next-agents.md` and `next-operator.md`; the checker reports a repo that still has them.
- Existing client repos are not yet synced to these changes: expect stale pins for `md/README.md`, `md/governance/README.md`, `md/plans/README.md`, `md/analysis/README.md` and the five governing documents, unpinned governing documents, a check-layout finding for any governing document a repo deleted, and a finding for the old handoff files.
- No operator decisions are pending here. The private repo's `artifact-template` plan (amended to the three-layer ruling on 4 Nov 2026) has owner decisions D1 to D6, for a thread in that repo.
- Conventions learned:
  - "Client repo" means a repo created from this template or brought into line with it. Use it only in text that lives in repo-template alone (root `README.md`, the template-sync skill and `sync.sh`, `check-layout.sh`). Text copied verbatim into a client repo (`md/` READMEs, governing documents, `AGENTS.md`) says "the repo", meaning that client repo.
  - Any change to a pinned file makes every client repo's pin of it stale; don't make whitespace-only edits to those files.
  - Separate claims go in bullets, not prose (operator preference).

## Environment facts

- No dependencies. `shellcheck` both scripts before a change lands.
- `~/.claude/skills/template-sync` links to this repo's `skills/template-sync/`, so edits here are live.
- The `/start` skill runs `bin/check-layout.sh` on every repo it opens.
- `gh pr view <n> --json mergeable` reads `UNKNOWN` right after a push; wait a few seconds before merging.
