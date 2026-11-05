# repo-template

A template for how a client repo is laid out and the rules it must
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

## The rules

Each rule is one claim. Rules are numbered so the check and other
documents cite them (`R6`). A number is never reused: a retired rule keeps
its number as `R7. Retired YYYY-MM-DD: <why>.`

### Root

- **R1.** `README.md`, `AGENTS.md`, `CLAUDE.md`, `next-agents.md` and
  `next-operator.md` exist at the root.
- **R2.** `LICENSE` (or `LICENSE.md`), `CHANGELOG.md` and `LOCAL.md` may
  also sit at the root. `LOCAL.md` is git-ignored.
- **R3.** No other document sits at the root. A governing document goes in
  `md/governance/`; any other document goes under `md/`.
- **R4.** `CLAUDE.md` imports `AGENTS.md` and adds nothing. Rules live in
  `AGENTS.md`, so every agent and every person reads one file.

### md/

- **R5.** `md/` has seven default folders: `governance/`, `docs/`,
  `plans/`, `analysis/`, `issues/`, `audits/` and `tested/`. All seven
  exist, even when empty.
- **R6.** Every folder directly in `md/` contains a `README.md`.
- **R7.** A folder's README states what belongs there, what does not, how
  files are named, and their form.
- **R8.** A client repo may add folders to `md/` (`glossary/` is in use
  elsewhere). An added folder follows R6 and R7 and has a row in
  `md/README.md`'s table.
- **R9.** No document sits directly in `md/` except `md/README.md`.

### Governing documents

- **R10.** `md/governance/` holds all five governing documents:
  `ARCHITECTURE.md`, `POLICY.md`, `SCHEMA.md`, `PROCEDURE.md` and
  `DOCTRINE.md`.
- **R11.** `md/governance/` holds nothing else except its `README.md`.
- **R12.** A governing document the client repo has no use for holds only
  its title and its pinned block. It is never deleted.

### Pinned template text

- **R13.** `md/README.md`, every default folder's README and every
  governing document end with a pinned block: the template's text for that
  file ("Pinned template text", below).
- **R14.** A pinned block is never edited by hand. It is refreshed from the
  template.

### Dates and status

- **R15.** Every document in `plans/`, `analysis/`, `issues/`, `audits/`
  and `tested/` has its date in its name. The folder's README gives the
  pattern. Documents in `docs/` and `governance/` do not.
- **R16.** A plan, and a governing document in use, open with a status
  line, `> Status: <word> · YYYY-MM-DD`, updated whenever the document
  changes.
- **R17.** The rest of a document's header is set by its folder's README.

### Handoff and threads

- **R18.** An analysis holds findings and recommendations, never open
  questions (the global rule in `~/.dotfiles/agents/AGENTS.md`, "Docs").
- **R19.** An open question that blocks the next step goes in
  `next-operator.md`. Any other open question goes in a plan linked from
  it.
- **R20.** `/start` reads the handoff files and `/end` rewrites them.
  Finished steps are deleted, not kept as history.
- **R21.** Threads are not kept in the client repo. `/end` writes each
  thread's exchange, unredacted, to the private
  [thread-archive](https://github.com/markreveley/thread-archive) repo
  under `threads/<repo>/`.
- **R22.** What a client repo learned from a thread goes in its handoff
  files and documents.

### Private names

- **R23.** A public client repo names no private project.
- **R24.** Names, stacks and quoted material from private repos go in the
  git-ignored `LOCAL.md`.

### Decisions

- **R25.** Plans and `ARCHITECTURE.md` number their decisions from `D1`.
- **R26.** A bare decision number (`D1`) is used only inside its own
  document. Elsewhere it is `ARCHITECTURE D1` or `<plan-slug> D1`.
- **R27.** A plan's decision, once accepted and built as design, moves to
  `ARCHITECTURE.md` under that file's next number, and the plan links to
  it.

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

For a new client repo:

1. Create it from this template on GitHub.
2. Replace every `<placeholder>` in `README.md` and `AGENTS.md`.
3. Delete `next-agents.md` and `next-operator.md` (they are this repo's
   own) and run `/start`, which creates fresh ones.
4. Pin `md/README.md`, each folder README and each governing document:
   `skills/template-sync/sync.sh --pin <file>`. A file still identical to
   the template's is cut to its title before the block is added.
5. Write the client repo's own content above each pin: what is in each
   folder, and each governing document it uses (R12, R16).
6. Run `bin/check-layout.sh`.

For an existing repo: run `bin/check-layout.sh` from its root. Move or
write what it names (the list is in "What the check enforces"), then
repoint links (`grep -rn "](old/path"`) and run it again.

## Pinned template text

A client repo keeps a copy of the template's text on what each `md/`
folder and each governing document is for, pinned to the template commit
it was copied from. The copy freezes the purpose the client repo was built
to; comparing it with the template later shows where the rules moved and
the client repo may need to follow.

- **Which files:** `md/README.md`, each default folder's README, and the
  five governing documents (R13).
- **Where:** at the bottom of the file, after a `---`, never at the top.
  The top is the client repo's own content.
- **What:** the template's file without its title line, under a marker
  comment and a heading (`About this folder` for a README, `About this
  file` for a governing document):

```
---

<!-- pinned from repo-template md/governance/POLICY.md @ <sha>; refresh from the template, do not edit by hand -->
## About this file (repo-template `<sha>`)
<the template's md/governance/POLICY.md, minus its first line>
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

Files a client repo fills in rather than copies (`README.md`, `AGENTS.md`,
`CLAUDE.md`, `.gitignore`) carry no block. The report shows the template's
changes to them since the client repo's oldest pin.

## Checking

```sh
bin/check-layout.sh            # this repo
bin/check-layout.sh ~/dev/repos/<repo>
```

Exit 0 prints `layout ok`; exit 1 means at least one finding, each on its
own line; exit 2 means the directory does not exist.

### What the check enforces

Each line is one check, with the rule it enforces. The check reads file
and folder names, one line of `CLAUDE.md`, and the pinned blocks; it reads
nothing else in any document.

| Check | Rule |
| --- | --- |
| `README.md`, `AGENTS.md`, `CLAUDE.md`, `next-agents.md` and `next-operator.md` exist at the root | R1 |
| No other `.md` file sits at the root, except `LOCAL.md`, `LICENSE.md` and `CHANGELOG.md` | R3 |
| `CLAUDE.md` has a line starting `@AGENTS.md` | R4 |
| `md/` exists, and so do its seven default folders | R5 |
| Every folder directly in `md/` has a `README.md`; folders nested deeper are not checked | R6 |
| No `.md` file sits directly in `md/` except `md/README.md` | R9 |
| `md/governance/` holds all five governing documents | R10 |
| `md/governance/` holds nothing else except `README.md` | R11 |
| Every pinned block matches the template's current text (skipped when run on this repo itself) | R14 |

### What it does not check

- R2: that `LOCAL.md` is git-ignored.
- R4: that `CLAUDE.md` adds nothing beyond the import.
- R7, R8: what a folder README says, and an added folder's row in
  `md/README.md`.
- R12: that an unused governing document holds only its title and pin.
- R13: that the pins are there. The check compares the pins it finds;
  `sync.sh`'s report lists files with none.
- R15 to R27: names, status lines, headers, open questions, handoff files,
  threads, private names, decisions.
