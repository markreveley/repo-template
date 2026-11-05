# Port the scripts to Python

> Status: accepted · 2026-11-04 · operator decision, 4 Nov 2026

Replace `bin/check-layout.sh` and `skills/template-sync/sync.sh` with
Python scripts that do the same job, with the same flags, output lines and
exit codes, so nothing that calls them has to change except the file name.

## Why

- The README's "What the check enforces" table is written by hand from the
  script. In Python each check can carry its description and guideline
  number, and the script can print the table (`--list-checks`), so the
  README and the script can't drift apart.
- `sync.sh` does the most text handling (finding pinned blocks, cutting a
  file's title line, comparing against `git show`). That is easier to
  read and to test in Python than in Bash.
- Tests become possible: build a small client repo in a temp folder and
  assert on the findings.

## Decisions

- **D1. Standard library only, Python 3.9 or later.** No `pip install`, no
  virtualenv: the scripts run with the `python3` that macOS ships.
- **D2. Same interface.** The flags (`--apply`, `--stale-only`, `--pin
  FILE`, an optional repo root), the output lines (`ok`, `stale`,
  `edited`, `gone`, `unpinned`, `missing`, the finding messages) and the
  exit codes (0, 1, 2) stay as they are. A client repo or skill that
  parses them sees no change.
- **D3. New names, no wrappers.** `bin/check-layout.py` and
  `skills/template-sync/sync.py`. The `.sh` files are deleted in the same
  PR; every reference is updated in that PR too.
- **D4. check-layout imports sync** instead of running it as a
  subprocess, for the stale-pin check.
- **D5. Each check is data.** A list of entries, each with its guideline
  number, a one-line description and a function. The README table is the
  output of `check-layout.py --list-checks`, pasted in; a test fails when
  the two differ.

## Steps

1. Write `tests/` with fixture client repos that cover each check and each
   sync line, and run them against the current Bash scripts, so the
   tests record today's behaviour before the port.
2. Port `sync.sh` to `sync.py` (D1, D2). Tests pass.
3. Port `check-layout.sh` to `check-layout.py` (D4, D5). Tests pass.
4. Add `--list-checks`; regenerate the README's "What the check enforces"
   table from it; add the test that compares them (D5).
5. Delete the `.sh` files and update every reference (D3): `README.md`
   ("Pinned template text", "Checking", "Adopting the template"),
   `skills/template-sync/SKILL.md`, `next-agents.md`. `grep -rn "check-layout.sh\|sync.sh"` finds none.
6. Run `check-layout.py` here and in one client repo; run `/template-sync`
   in that client repo. Record both in `md/tested/`.

## Waits on

Nothing.
