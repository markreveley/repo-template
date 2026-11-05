# Port the scripts to Python

> Status: accepted · 2026-11-04 · operator decision, 4 Nov 2026; D6 added the same day

Replace `bin/check-layout.sh` and `skills/template-sync/sync.sh` with
Python scripts that do the same job, with the same flags, output lines and
exit codes, so nothing that calls them has to change except the file name.

## Why

- The README's "What the check enforces" table is written by hand from the
  script. In Python each check can carry its description and rule
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
- **D5. Each check is data.** A list of entries, each with its rule
  number, a one-line description and a function. The README table is the
  output of `check-layout.py --list-checks`, pasted in; a test fails when
  the two differ.
- **D6. The template's files ship in pinned shape.** `md/README.md`,
  every default folder's README and the five governing documents are laid
  out in repo-template as a client repo's copy will be: the title, room
  for the repo's own content, `---`, a marker, the heading, then the
  template's text. A repo created from the template starts in the right
  shape, and nobody cuts a stub down by hand.
  - **Unstamped marker** in the template: `<!-- pinned from repo-template
    <path> @ unstamped; run sync.py --pin, do not edit by hand -->`. The
    heading has no commit: `## About this folder` or `## About this file`.
  - **The pinned text is everything after the heading**, in the template
    and in a client repo alike. It is no longer "the file minus its title
    line".
  - **`--pin` stamps instead of appending:** it writes the template's
    commit into the marker and the heading. A file with no marker (a repo
    brought into line, not created from the template) still gets the
    block appended, as now.
  - **Report:** an unstamped marker is reported as `unpinned`.
  - **Exception to D2:** `--pin`'s behaviour changes as above; its flag
    and output line stay the same.
  - **Pins made before D6** compare against the new text once, show as
    `stale`, and `--apply` rewrites them in the new form.

## Steps

1. Write `tests/` with fixture client repos that cover each check and each
   sync line, and run them against the current Bash scripts, so the
   tests record today's behaviour before the port.
2. Port `sync.sh` to `sync.py` (D1, D2), then make D6's changes to it.
   Tests pass.
3. Port `check-layout.sh` to `check-layout.py` (D4, D5). Tests pass.
4. Reshape the template's files (D6): add the `---`, the unstamped
   marker and the heading to `md/README.md`, the folder READMEs and the
   governing documents. Add fixture cases for unstamped, stamped and
   pre-D6 pins. Tests pass.
5. Add `--list-checks`; regenerate the README's "What the check enforces"
   table from it; add the test that compares them (D5).
6. Delete the `.sh` files and update every reference (D3): `README.md`
   ("Pinned template text", "Checking", "Adopting the template", whose
   pin step becomes a stamp step under D6), `skills/template-sync/SKILL.md`,
   `next-agents.md`. `grep -rn "check-layout.sh\|sync.sh"` finds none.
7. Run `check-layout.py` here and in one client repo; run `/template-sync`
   in that client repo. Record both in `md/tested/`.

## Waits on

Nothing.
