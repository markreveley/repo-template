---
type: handoff
audience: agent
updated: 2026-11-04
---

# Next steps for the agent

Read with [`next-operator.md`](next-operator.md). Rewrite both at the end of each thread; delete finished steps.

## State
- This repo is the layout template and its rules; `README.md` is the contract, `md/analysis/2026-11-04-layout-survey/` the survey and decisions behind it. Built 4 Nov 2026 beside artifact-dag, which was aligned to it the same day.
- These two handoff files are this repo's own. A client repo deletes them and runs `/start`, which creates fresh ones from its templates (README, "Adopting the template").
- Nothing is committed yet; the repo has a remote (`markreveley/repo-template`) and no commits.
- `bin/check-layout.sh` passes here.

## Environment facts
- No dependencies. `shellcheck` on the script before a change lands.
- The `/start` and `/end` skills live in `~/.claude/skills/` (linked from `~/.dotfiles`); `/end` writes threads to `~/dev/repos/thread-archive/threads/<repo>/`, not into the repo.

## Next, in order
1. First commit and push, when the operator says.
2. The GitHub template setting is the operator's (their file). The `/start` step that runs the check was added to the skill in dotfiles on 4 Nov 2026.
3. Port the scripts to Python: [python-port](md/plans/2026-11-04-python-port/python-port.md), step 1.
4. Align the repo that keeps its working material at the root (`in-progress/`), in a session there: `md/` with its seven default folders and their READMEs.

## Pending operator decisions
- None. The private repo's `artifact-template` plan was amended to the three-layer ruling on 4 Nov 2026 (uncommitted there); its owner decisions D1 to D6 are the next thread's, in that repo.
