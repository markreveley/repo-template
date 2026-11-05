---
type: handoff
audience: agent
updated: 2026-11-04
---

# Next steps for the agent

Read with [`next-operator.md`](next-operator.md). Rewrite both at the end of each thread; delete finished steps.

## State
- This repo is the layout template and its rules; `README.md` is the contract, `md/analysis/2026-11-04-layout-survey/` the survey and decisions behind it.
- These two handoff files are this repo's own. A client repo deletes them and runs `/start`, which creates fresh ones (README, "Adopting the template").
- On `main`, pushed, clean. Changes go through PRs; #5 to #8 merged 4 Nov 2026.
- `bin/check-layout.sh` passes here.
- The README's rules are R1 to R27, one claim each; the check table and "What it does not check" map every check to a rule. Numbers are never reused.
- All five governing documents are required (R10); an unused one holds only its title and its pinned block (R12). `md/README.md`, the folder READMEs and the governing documents all carry pins (R13). Each governing document has a `**Changed by:**` line.
- Existing client repos are not yet synced to these changes: expect stale pins for `md/README.md`, `md/governance/README.md` and the five governing documents, unpinned governing documents, and a check-layout finding for any governing document a repo deleted.

## Conventions learned this thread
- "Client repo" means a repo created from this template or brought into line with it. Use it only in text that lives in repo-template alone (root `README.md`, the template-sync skill and `sync.sh`, `check-layout.sh`). Text copied verbatim into a client repo (`md/` READMEs, governing documents, `AGENTS.md`) says "the repo", meaning that client repo.
- Any change to a pinned file makes every client repo's pin of it stale; don't make whitespace-only edits to those files.
- Separate claims go in bullets, not prose (operator preference).

## Environment facts
- No dependencies. `shellcheck` both scripts before a change lands.
- `~/.claude/skills/template-sync` links to this repo's `skills/template-sync/`, so edits here are live.
- The `/start` skill runs `bin/check-layout.sh` on every repo it opens.
- `gh pr view <n> --json mergeable` reads `UNKNOWN` right after a push; wait a few seconds before merging.

## Next, in order
1. Port the scripts to Python: [python-port](md/plans/2026-11-04-python-port/python-port.md), step 1 (tests against the Bash scripts). D6 there reshapes the template's pinned files.
2. Run `/template-sync` in each client repo to take up R10 to R14 and the governance changes.
3. Align the repo that keeps its working material at the root (`in-progress/`), in a session there: `md/` with its seven default folders and their READMEs.

## Pending operator decisions
- None here. The private repo's `artifact-template` plan (amended to the three-layer ruling on 4 Nov 2026) has owner decisions D1 to D6, for a thread in that repo.
