# repo-template

How a client repo is laid out and the rules it follows. A *client repo* is any repo laid out from this one, including this one. `template/` holds the files a new client repo starts from and the rules for each `md/` folder; `bin/check_layout.py` reports where a client repo departs from the rules, and `bin/client_sync.py` shows what changed here since a client repo last synced.

In an agent session, use the agent-files skills: `/check-layout` runs the check, `/client-sync` runs the sync. Both use a local clone of this repo at `~/dev/repos/repo-template` when there is one, and clone it otherwise.

## The layout

Every client repo has this layout. In the listing, "the repo" means that client repo.

```
README.md           what the repo is, how to use it, and a table of what is where
AGENTS.md           working rules for any agent (Claude Code, Codex, Gemini) and for people
CLAUDE.md           imports AGENTS.md; nothing of its own
state.md            what is true now; /end rewrites it
next.md             the ordered list of what's next, each step saying whose; nothing else
LICENSE             MIT
LOCAL.md            git-ignored notes that stay on one machine (private names, local paths)
md/                 the repo's documents, in seven folders that always exist (md/README.md)
  governance/       the documents that govern the repo, when it has any: ARCHITECTURE, POLICY, SCHEMA, PROCEDURE, DOCTRINE
  docs/             how to use and work on what the repo holds; repo-template-sync.md records the last sync
  plans/            what will be done, in what order, and what it waits on
  analysis/         dated findings and recommendations
  issues/           dated findings against something: a bug, a doc that disagrees with the code
  audits/           dated readings of the repo against what it claims to be
  tested/           one report per run of something only a run can check
bin/                scripts, when the repo has any
_scheduled/         definitions of the repo's scheduled tasks, one file each, when the repo has any
evals/              evals of the code or of its subject matter, when the repo has any
```

Everything else at the root is code or data: source folders, a `dag/`, a `tests/`, a build config.

## The rules

Each rule is one claim. Rules are numbered so the check and other documents cite them (`R6`). A number is never reused: a retired rule keeps its number as `R7. Retired YYYY-MM-DD: <why>.`

### Root

- **R1.** `README.md`, `AGENTS.md`, `CLAUDE.md`, `state.md` and `next.md` exist at the root.
- **R2.** `LICENSE` (or `LICENSE.md`), `CHANGELOG.md` and `LOCAL.md` may also sit at the root. `LOCAL.md` is git-ignored.
- **R3.** No other document sits at the root. A governing document goes in `md/governance/`; any other document goes under `md/`.
- **R4.** `CLAUDE.md` imports `AGENTS.md` and adds nothing. Rules live in `AGENTS.md`, so every agent and every person reads one file.

### md/

- **R5.** `md/` has seven default folders: `governance/`, `docs/`, `plans/`, `analysis/`, `issues/`, `audits/` and `tested/`. All seven exist, even when empty, so a new document has an obvious place.
- **R6.** Every folder directly in `md/` contains a `README.md`.
- **R7.** `md/README.md` and each default folder's README say what that folder holds in this repo, and link to repo-template's rules for it (`template/md/<folder>/README.md`), which say what belongs there, what does not, how files are named, and their form.
- **R8.** A client repo may add folders to `md/` (`glossary/` is in use elsewhere). An added folder has a README that says what belongs there and how files are named, and a row in `md/README.md`'s table.
- **R9.** No document sits directly in `md/` except `md/README.md`.

### Governing documents

- **R10.** A governing document is one of `ARCHITECTURE.md`, `POLICY.md`, `SCHEMA.md`, `PROCEDURE.md` and `DOCTRINE.md`, in `md/governance/`. Each is optional: the repo creates one the first time it has something to put in it, in the form of repo-template's `template/md/governance/<NAME>.md`.
- **R11.** `md/governance/` holds nothing else except its `README.md`.
- **R12.** Retired 2026-11-24: governing documents are optional (R10), so an unused one is not kept.

### Template text

- **R13.** Retired 2026-11-24: client repos no longer keep a pinned copy of the template's text; folder READMEs link to it (R7).
- **R14.** Retired 2026-11-24: as R13.
- **R31.** `md/docs/repo-template-sync.md` records the repo-template commit the repo last synced to, on a line `synced: <commit>`. `/client-sync` shows what changed here since that commit; once the changes are taken up, it moves the line to the new commit.

### Dates and status

- **R15.** Every document in `plans/`, `analysis/`, `issues/`, `audits/` and `tested/` has its date in its name. The folder's rules give the pattern. Documents in `docs/` and `governance/` do not.
- **R16.** A plan, and a governing document, open with a status line, `> Status: <word> · YYYY-MM-DD`, updated whenever the document changes.
- **R17.** The rest of a document's header is set by its folder's rules.

### Handoff and threads

- **R18.** An analysis holds findings and recommendations, never open questions.
- **R19.** An open question that blocks the next step is an `(operator)` step in `next.md`. Any other open question goes in a plan linked from it.
- **R20.** The handoff is `state.md` and `next.md`. `/start` reads them; `/end` rewrites them, with what the thread changed and learned. Finished steps and past events are deleted, not kept as history: git has them.
- **R21.** Threads are not kept in the client repo. `/archive-thread` writes each one to the private [direction](https://github.com/markreveley/direction) repo, in an output folder in the day it started; `/end` calls it and marks the thread as a dev thread.
- **R22.** Retired 2026-11-24: merged into R20.
- **R30.** `next.md` holds only the ordered list of next steps, each saying whose it is: `(operator)`, `(agent)` or `(agent, blocked on operator)`. `state.md` holds only what is true now and the environment facts a fresh agent needs. Both start from, and keep the form of, `template/next.md` and `template/state.md`. `next.md` is changed through `/update-next`, which also sets the repo's Next cell in direction's `repo-manifest.md` to its first open step.

### Private names

- **R23.** A public client repo names no private project.
- **R24.** Names, stacks and quoted material from private repos go in the git-ignored `LOCAL.md`.

### Decisions

- **R25.** Plans and `ARCHITECTURE.md` number their decisions from `D1`.
- **R26.** A bare decision number (`D1`) is used only inside its own document. Elsewhere it is `ARCHITECTURE D1` or `<plan-slug> D1`.
- **R27.** A plan's decision, once accepted and built as design, moves to `ARCHITECTURE.md` under that file's next number, and the plan links to it.

### Scheduled tasks

- **R28.** A client repo with scheduled tasks keeps one definition file per task in `_scheduled/`, in the structure `template/_scheduled/README.md` sets. The file is the source of truth; the scheduler's prompt only points at it.

### Pushing

- **R29.** The agent commits and pushes straight to `main`, without asking and with no PR, unless the repo's `AGENTS.md` says otherwise.

## Starting or aligning a client repo

A new repo:

1. Create the repo, clone it, and run `/client-sync` with `--init` (or `bin/client_sync.py --init <repo>`). It copies `template/` into the repo without overwriting anything, writes a README in each `md/` folder that links to its rules here, and writes `md/docs/repo-template-sync.md`.
2. Replace every `<placeholder>` in `README.md`, `AGENTS.md`, `state.md` and `next.md`.
3. Run `/check-layout`.

An existing repo: run `/client-sync` with `--migrate`, which also strips pinned blocks left from before 2026-11-24 and deletes governing documents left holding only a title. Then run `/check-layout`, move or write what it names, and repoint links (`grep -rn "](old/path"`).

## Checking

```sh
bin/check_layout.py                      # this repo
bin/check_layout.py ~/dev/repos/<repo>
bin/check_layout.py --list-checks        # the table below
```

Exit 0 prints `layout ok`; exit 1 means at least one finding, each on its own line; exit 2 means the directory does not exist.

### What the check enforces

Each line is one check, with the rule it enforces. The table is `bin/check_layout.py --list-checks`; `tests/test_tools.py` fails if the two differ.

<!-- checks:start -->
| Check | Rule |
| --- | --- |
| `README.md`, `AGENTS.md` and `CLAUDE.md` exist at the root | R1 |
| `state.md` exists at the root; a repo still keeping State in `AGENTS.md` or `next.md` is told to move it | R1, R30 |
| `next.md` exists at the root; `next-agents.md` and `next-operator.md` are reported for merging | R1, R30 |
| No other `.md` file sits at the root, except `LOCAL.md`, `LICENSE.md` and `CHANGELOG.md` | R3 |
| `CLAUDE.md` has a line starting `@AGENTS.md` | R4 |
| `md/` exists, and so do its seven default folders | R5 |
| Every folder directly in `md/` has a `README.md` | R6 |
| `md/README.md` and each default folder's README link to repo-template's rules for that folder | R7 |
| No `.md` file sits directly in `md/` except `md/README.md` | R9 |
| `md/governance/` holds only `README.md` and the five governing documents | R11 |
| No pinned template block from before 2026-11-24 is left in `md/` | R7 |
| `md/docs/repo-template-sync.md` has a `synced:` commit | R31 |
| No change to `template/` or `README.md` here since that commit (skipped for repo-template itself) | R31 |
<!-- checks:end -->

### What it does not check

- R2: that `LOCAL.md` is git-ignored.
- R4: that `CLAUDE.md` adds nothing beyond the import.
- R8: what an added folder's README says, and its row in `md/README.md`.
- R10, R15 to R30: governing documents' form, names, status lines, headers, open questions, what the handoff files hold, threads, private names, decisions, scheduled tasks, pushing.

## Layers

A client repo that keeps a DAG also follows [artifact-dag](https://github.com/markreveley/artifact-dag): its schema, its policy on claims, its tools and its `dag` skill. An *artifact*, a client repo that represents another repo in prose, figures, a command-line lab, a DAG and code anchors, is made from artifact-template, which builds on both. Nothing here says how a DAG or an artifact is kept; nothing there says how a client repo is laid out.
