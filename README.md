# repo-template

A template for how a client repo is laid out and the guidelines it must
follow. A *client repo* is any repo created from this template or brought
into line with it. Use this repo as the GitHub template for a new client
repo, or as the checklist when bringing an existing repo into line.
`bin/check-layout.sh` reports where a client repo departs from it; "What
the check enforces" below lists exactly what it checks.

## The layout

Every client repo has this layout. In the listing, "the repo" means that
client repo.

```
README.md           what the repo is, how to use it, and a table of what is where
AGENTS.md           working rules for any agent (Claude Code, Codex, Gemini) and for people
CLAUDE.md           one line that imports AGENTS.md; nothing of its own
next-agents.md      handoff: the agent's state and next steps, rewritten at the end of each thread; /start creates it
next-operator.md    handoff: the operator's steps and open questions
LICENSE             MIT
LOCAL.md            git-ignored notes that stay on one machine (private names, local paths)
md/                 the repo's documents, in seven folders that always exist (md/README.md)
  governance/         the documents that govern the repo: ARCHITECTURE, POLICY, SCHEMA, PROCEDURE, DOCTRINE
  docs/             how to use and work on what the repo holds
  plans/            what will be done, in what order, and what it waits on
  analysis/         dated findings and recommendations
  issues/           dated findings against something: a bug, a doc that disagrees with the code
  audits/           dated readings of the repo against what it claims to be
  tested/           one report per run of something only a run can check
bin/                scripts, when the repo has any
evals/              evals of the code or of its subject matter, when the repo has any
```

Everything else at the root is code or data: source folders, a `dag/`, a
`tests/`, a build config.

## The guidelines

1. **`md/` has seven default folders.** They are `governance/`, `docs/`,
   `plans/`, `analysis/`, `issues/`, `audits/` and `tested/`. Every client
   repo has all seven, even when one is empty.
2. **Every folder in `md/` must contain a README.** It states what belongs
   there, what does not, and how files are named. A client repo may add
   folders to `md/` beyond the seven defaults (`glossary/` is in use
   elsewhere), as long as they follow the same rules.
3. **The root holds only the named files.** `README.md`, `AGENTS.md`,
   `CLAUDE.md`, `next-agents.md` and `next-operator.md` must exist;
   `LICENSE` and the git-ignored `LOCAL.md` sit beside them. No other document sits
   at the root: a governing document goes in `md/governance/`, anything
   else under `md/`.
4. **A governing document is present only when it has content.** The five
   files in this repo's `md/governance/` are stubs that say what each is
   for. A client repo deletes the ones it has no use for and lists the rest
   in its README.
5. **Documents carry a date and a status.** A plan opens with
   `> Status: proposed · YYYY-MM-DD`. An analysis opens with its date,
   question, sources read and method caveat. An issue and a thread carry
   the date in the file name.
6. **Open questions live in the handoff files.** An analysis holds findings
   and recommendations; a question that blocks the next step goes in
   `next-operator.md`, and any other in a plan linked from it. This is the
   global rule in `~/.dotfiles/agents/AGENTS.md`, "Docs".
7. **A public client repo names no private project.** Names, stacks and
   quoted material from private repos live in the git-ignored `LOCAL.md`.
8. **CLAUDE.md adds nothing.** Rules live in `AGENTS.md` so every agent and
   every person reads one file. `CLAUDE.md` imports it.
9. **The handoff files are rewritten, not appended.** `/start` reads them
   and `/end` rewrites them; finished steps are deleted, not kept as
   history.
10. **Threads live outside the client repo.** `/end` writes each thread's
    exchange to the private
    [thread-archive](https://github.com/markreveley/thread-archive) repo,
    under `threads/<repo>/`, unredacted. A client repo keeps what it
    learned from a thread in its handoff files and documents, not the
    thread itself.
11. **A decision is cited with the document that numbers it.** Plans and
    `ARCHITECTURE.md` both number decisions from `D1`, so a bare `D1` is
    used only inside its own document; elsewhere it is `ARCHITECTURE D1` or
    `<plan-slug> D1`. A plan's decision, once accepted and built as design,
    moves to `ARCHITECTURE.md` under that file's next number, and the plan
    links to it: architecture numbers stay unique and plan numbers stay
    local.

## Layers

This repo is the template for every client repo. A client repo that keeps
a DAG also follows [artifact-dag](https://github.com/markreveley/artifact-dag):
its schema (`md/governance/SCHEMA.md` there), its policy on claims, its
tools and its `dag` skill. An *artifact*, a client repo that represents
another repo in prose, figures, a command-line lab, a DAG and code anchors,
is made from artifact-template, which builds on both: this layout plus
what an artifact adds, and artifact-dag for the DAG. Nothing here says how
a DAG or an artifact is kept; nothing there says how a client repo is laid
out.

## Adopting the template

For a new client repo: create it from this template on GitHub, then
replace every `<placeholder>` in `README.md` and `AGENTS.md`, delete
`next-agents.md` and `next-operator.md` (they are this repo's own) and run
`/start`, which creates fresh ones, delete the governing documents the
client repo has no use for, pin the folder READMEs (below), and run
`bin/check-layout.sh`.

For an existing repo: run `bin/check-layout.sh` from its root. Move or
write what it names (the list is in "What the check enforces"), then
repoint links (`grep -rn "](old/path"`) and run it again.

## Pinned template text

A client repo keeps a copy of the template's text on what each `md/`
folder is for, pinned to the template commit it was copied from. The copy
freezes the purpose the client repo was built to; comparing it with the
template later shows where the guidelines moved and the client repo may
need to follow.

The copy goes at the bottom of the client repo's README for that folder,
after a `---`, never at the top: the top is the client repo's own content
(what is in the folder). The block is the template's file without its
title line:

```
---

<!-- pinned from repo-template md/plans/README.md @ <sha>; refresh from the template, do not edit by hand -->
## About this folder (repo-template `<sha>`)
<the template's md/plans/README.md, minus its first line>
```

`skills/template-sync/sync.sh` writes and compares the blocks, and the
`template-sync` skill (`skills/template-sync/SKILL.md`, linked into
`~/.claude/skills/` by the dotfiles installer) reads the changes against
the client repo:

```sh
skills/template-sync/sync.sh ~/dev/repos/<repo>               # report
skills/template-sync/sync.sh --pin md/plans/README.md <repo>  # add a block
skills/template-sync/sync.sh --apply <repo>                   # refresh stale blocks
```

To pin a README that holds only the template's text, cut it to its title
and the client repo's own line, then `--pin` it. Files a client repo fills
in rather than copies (`README.md`, `AGENTS.md`, `CLAUDE.md`, `.gitignore`,
the governance stubs) carry no block; the report shows the template's
changes to them since the client repo's oldest pin.

## Checking

```sh
bin/check-layout.sh            # this repo
bin/check-layout.sh ~/dev/repos/<repo>
```

Exit 0 prints `layout ok`; exit 1 means at least one finding, each on its
own line; exit 2 means the directory does not exist.

### What the check enforces

Each line is one check, with the guideline it enforces. The check reads
file and folder names, one line of `CLAUDE.md`, and the pinned blocks; it
reads nothing else in any document.

| Check | Guideline |
| --- | --- |
| `README.md`, `AGENTS.md`, `CLAUDE.md`, `next-agents.md` and `next-operator.md` exist at the root | 3 |
| No other `.md` file sits at the root, except `LOCAL.md`, `LICENSE.md` and `CHANGELOG.md` | 3 |
| `CLAUDE.md` has a line starting `@AGENTS.md` | 8 |
| `md/` exists, and so do its seven default folders | 1 |
| Every folder directly in `md/` has a `README.md`; folders nested deeper are not checked | 2 |
| No `.md` file sits directly in `md/` except `md/README.md` | 2 |
| `md/governance/` holds nothing but `README.md` and the five governing names | 4 |
| Every pinned block matches the template's current text (skipped when run on this repo itself) | Pinned template text |

### What it does not check

- That `LICENSE` exists, or that `LOCAL.md` is git-ignored (3).
- That `CLAUDE.md` adds nothing beyond the import (8).
- What a folder README says, or that files follow its naming (2).
- That a governing document has content, or that the README lists it (4).
- Guidelines 5, 6, 7, 9, 10 and 11: dates and statuses, where questions
  live, private names, how handoff files are kept, threads, decision
  citations.
