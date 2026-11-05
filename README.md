# repo-template

The layout every one of these repos follows, and the guidelines they adhere
to. Use it as the GitHub template for a new repo, or as the checklist when
bringing an existing one into line. `bin/check-layout.sh` reports where a
repo departs from it.

## The layout

```
README.md           what the repo is, how to use it, and a table of what is where
AGENTS.md           working rules for any agent (Claude Code, Codex, Gemini) and for people
CLAUDE.md           one line that imports AGENTS.md; nothing of its own
next-agents.md      handoff: the agent's state and next steps, rewritten at the end of each thread; /start creates it
next-operator.md    handoff: the operator's steps and open questions
LICENSE             MIT
LOCAL.md            git-ignored notes that stay on one machine (private names, local paths)
md/                 every Markdown document about the repo or its work (md/README.md)
  governance/         the documents that govern the repo: ARCHITECTURE, POLICY, SCHEMA, PROCEDURE, DOCTRINE
  docs/             how to use and work on what the repo holds
  plans/            what will be done, in what order, and what it waits on
  analysis/         dated findings and recommendations
  issues/           dated findings against something: a bug, a doc that disagrees with the code
  audits/           dated readings of the repo against what it claims to be
  tested/           one report per run of something only a run can check
bin/                scripts, when the repo has any
```

Everything else at the root is code or data: source folders, a `dag/`, a
`tests/`, a build config.

## The guidelines

1. **The md rule.** A folder that holds Markdown files and only Markdown
   files lives under `md/`. A folder of Markdown that a tool reads as data
   (a DAG's node files, a static site's posts, a tutorial's source) is the
   repo's content, not a document about it, and stays where its tool
   expects it; the README's table says so.
2. **Every folder under `md/` has a README.** It says what belongs there,
   what does not, and how files are named. A repo may add folders under
   `md/` beyond the seven defaults (`glossary/` is in use elsewhere) on the
   same terms.
3. **The root holds the five named files and README.** No other loose
   documents at the root: a document is a governing document, or it goes under `md/`.
4. **A governing document is present only when it has content.** The five files there
   are stubs that say what each is for. A repo deletes the ones it has no
   use for and lists the rest in its README.
5. **Documents carry a date and a status.** A plan opens with
   `> Status: proposed · YYYY-MM-DD`. An analysis opens with its date,
   question, sources read and method caveat. An issue and a thread carry
   the date in the file name.
6. **Open questions live in the handoff files.** An analysis holds findings
   and recommendations; a question that blocks the next step goes in
   `next-operator.md`, and any other in a plan linked from it. This is the
   global rule in `~/.dotfiles/agents/AGENTS.md`, "Docs".
7. **A public repo names no private project.** Names, stacks and quoted
   material from private repos live in the git-ignored `LOCAL.md`.
8. **CLAUDE.md adds nothing.** Rules live in `AGENTS.md` so every agent and
   every person reads one file. `CLAUDE.md` imports it.
9. **The handoff files are rewritten, not appended.** `/start` reads them
   and `/end` rewrites them; finished steps are deleted, not kept as history.
10. **Threads live outside the repo.** `/end` writes each thread's exchange
    to the private [thread-archive](https://github.com/markreveley/thread-archive)
    repo, under `threads/<repo>/`, unredacted. A repo keeps what it learned
    from a thread in its handoff files and documents, not the thread itself.

## Layers

This repo is the template for every repo. A repo that keeps a DAG also
follows [artifact-dag](https://github.com/markreveley/artifact-dag): its
schema (`md/governance/SCHEMA.md` there), its policy on claims, its tools
and its `dag` skill. An *artifact*, a repo that represents another repo in
prose, figures, a command-line lab, a DAG and code anchors, is made from
artifact-template, which builds on both: this layout plus what an artifact
adds, and artifact-dag for the DAG. Nothing here says how a DAG or an
artifact is kept; nothing there says how a repo is laid out.

## Adopting the template

For a new repo: create it from this template on GitHub, then replace every
`<placeholder>` in `README.md` and `AGENTS.md`, delete `next-agents.md` and
`next-operator.md` (they are this repo's own) and run `/start`, which creates
fresh ones, delete the governing documents the repo has no use for, pin
the folder READMEs (below), and run `bin/check-layout.sh`.

For an existing repo: run `bin/check-layout.sh` from its root. It lists
Markdown-only folders outside `md/`, folders under `md/` with no README,
loose documents at the root, and the named files that are missing. Move or
write what it names, then repoint links (`grep -rn "](old/path"`) and run it
again.

## Pinned template text

A repo keeps a copy of the template's text on what each `md/` folder is
for, pinned to the template commit it was copied from. The copy freezes
the purpose the repo was built to; comparing it with the template later
shows where the guidelines moved and the repo may need to follow.

The copy goes at the bottom of the repo's README for that folder, after a
`---`, never at the top: the top is the repo's own content (what is in the
folder). The block is the template's file without its title line:

```
---

<!-- pinned from repo-template md/plans/README.md @ <sha>; refresh from the template, do not edit by hand -->
## About this folder (repo-template `<sha>`)
<the template's md/plans/README.md, minus its first line>
```

`skills/template-sync/sync.sh` writes and compares the blocks, and the
`template-sync` skill (`skills/template-sync/SKILL.md`, linked into
`~/.claude/skills/` by the dotfiles installer) reads the changes against
the repo:

```sh
skills/template-sync/sync.sh ~/dev/repos/<repo>               # report
skills/template-sync/sync.sh --pin md/plans/README.md <repo>  # add a block
skills/template-sync/sync.sh --apply <repo>                   # refresh stale blocks
```

To pin a README that holds only the template's text, cut it to its title
and the repo's own line, then `--pin` it. Files a repo fills in rather
than copies (`README.md`, `AGENTS.md`, `CLAUDE.md`, `.gitignore`, the
governance stubs) carry no block; the report shows the template's changes
to them since the repo's oldest pin.

## Checking

```sh
bin/check-layout.sh            # this repo
bin/check-layout.sh ~/dev/repos/<repo>
```

Exit 1 means at least one finding. The check reads the layout, and the
pinned blocks only to compare them with the template; it does not read the
rest of the documents. A folder of Markdown that a tool reads as data
(guideline 1) is listed in `.layoutignore` at the root, one path prefix per
line, and the README's table says what it is.
