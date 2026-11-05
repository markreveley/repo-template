---
name: template-sync
description: Compare a repo laid out from repo-template with the template's current version - the pinned "About this folder" text at the bottom of its md/ READMEs, and the template's changes to the files the repo fills in - then report where the repo's own text or layout now disagrees, and refresh the pins once the user approves. Use when the user says "template sync", "sync with repo-template", "is this repo up to date with the template", or when check-layout reports pinned template text out of date.
---

# template-sync

The script does the comparing; you do the reading. The pinned-block format
and why it exists are in repo-template's `README.md`, "Pinned template text".

## Steps

1. **Find the template.** `~/dev/repos/repo-template`. If it is not there,
   say so and stop. Run `git -C ~/dev/repos/repo-template pull --ff-only`
   only if the user asks for the latest; otherwise compare against what is
   checked out and name its commit.
2. **Run the report** from the repo's root:
   `~/dev/repos/repo-template/skills/template-sync/sync.sh`. Read-only.
   Lines are `ok`, `stale` (the template changed since the pin), `edited`
   (the pin was changed here by hand), `gone` (the template no longer has
   that file), `unpinned`, `missing` (a template folder this repo lacks),
   and the template's diff since the oldest pin to the files a repo fills
   in (`README.md` guidelines, `AGENTS.md`, `CLAUDE.md`, `.gitignore`,
   governance stubs).
3. **Read each change against the repo.** For every stale pin and every
   change to a filled-in file, check whether the repo's own text now
   disagrees: the top of the same README, the files in that folder (names,
   status lines, form), `AGENTS.md`, the root README's table. This is the
   point of the skill; the diff alone is not the report.
4. **Report** in one list, most consequential first: each template change
   in a line, and under it what in the repo it contradicts, or "nothing in
   the repo depends on it". Then the `edited`, `gone`, `unpinned` and
   `missing` lines with a recommendation for each. Do not change anything
   yet.
5. **On approval**, in a branch if the repo works through PRs:
   - `sync.sh --apply` rewrites the stale and edited pins at the
     template's commit. It never touches the text above the `---`.
   - `sync.sh --pin <file>` adds a pin to an unpinned README. If the top of
     that file restates the template's text, say so first: the restatement
     goes, and the repo's own content stays on top.
   - Fix the repo text that step 3 found contradicting, as approved.
   - A `gone` pin, a `missing` folder and changes to filled-in files are
     edited by hand; the script does not do them.
6. Run `~/dev/repos/repo-template/bin/check-layout.sh`; it should report
   `layout ok`.
