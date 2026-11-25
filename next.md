---
type: handoff
updated: 2026-11-24
---

# Next

> This file's first open step is mirrored in direction's `repo-manifest.md`. Change it by asking an agent to run `update-next`. If you edit it by hand, run `update-next` afterwards. State lives in `AGENTS.md`, not here.

1. **(agent)** Port the scripts to Python: [python-port](md/plans/2026-11-04-python-port/python-port.md), step 1 (tests against the Bash scripts). D6 there reshapes the template's pinned files.
2. **(operator)** Turn on the template setting, if you want new repos made from this one: GitHub, repo Settings, General, tick "Template repository". New repos then get "Use this template". Still off as of 4 Nov 2026.
3. **(agent)** Run `/template-sync` in each client repo to take up R10 to R14, R30 and the governance changes. Moving each repo to `next.md` plus State in `AGENTS.md` is step 3 of agent-files' `next.md`, which lists the repos.
4. **(agent)** Align the repo that keeps its working material at the root (`in-progress/`), in a session there: `md/` with its seven default folders and their READMEs.
