---
type: handoff
updated: 2026-11-24
---

# State

> What is true now, and nothing else: no history (git has it) and no next steps (`next.md`). `/end` rewrites this file (R30).

## Now

- The rules are R1 to R31; R12, R13, R14 and R22 are retired. The README's check table is the output of `bin/check_layout.py --list-checks`.
- Starting files and folder rules live in `template/`; repo-template's own `README.md`, `AGENTS.md`, `state.md`, `next.md` and `md/` are at the root.
- `bin/check_layout.py` and `bin/client_sync.py` are the tools (Python, standard library only). The tests pass, and `bin/check_layout.py` passes on this repo.
- The skills that run them, `/check-layout` and `/client-sync`, are in the agent-files plugin; `/start` there runs `/check-layout` on every repo it opens.
- No client repo has been migrated yet. Each still has pinned blocks, all five governing documents, State in `AGENTS.md` or `next.md` (or the old `next-agents.md` and `next-operator.md`), and no sync record; `/check-layout` reports all of these.

## Environment facts

- Python 3.9 or later, standard library only. `client_sync.py` needs repo-template's full git history to diff from a client repo's synced commit; a shallow clone fails with "has no commit".
- repo-template is public, so a cloud session can always read it, and the folder READMEs in client repos can link to it.
- The private repo's `artifact-template` plan (amended to the three-layer ruling on 4 Nov 2026) has owner decisions D1 to D6, for a thread in that repo.
