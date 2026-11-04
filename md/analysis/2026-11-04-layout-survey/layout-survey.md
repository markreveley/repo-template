# The layout the repos share: a survey, and the decisions behind this template

**Date:** 2026-11-04

**Question.** What layout do the operator's repos follow today, what do they
disagree on, and what should the template fix? Asked when this repo was
created, empty, with the brief: an `md/` folder for every Markdown-only
folder, default subfolders, a set of governing documents, and the four named
files at the root.

**Sources read.** The root listing and `md/` listing of the eleven repos
with a commit in the week to 3 Nov 2026, their `AGENTS.md` and `CLAUDE.md`,
the README of each `md/` subfolder that had one, the `/start` and `/end`
skills in dotfiles, and the global `~/.dotfiles/agents/AGENTS.md`. One
repo's plan of 2 Nov for an `artifact-template` repo. Private repos are not
named here.

**Method caveat.** A one-day reading of layouts, not of the documents'
content. Counts are as of 3 Nov 2026.

---

## 1. The short answer

- **The root is already uniform.** Ten of eleven repos have `README.md`,
  `AGENTS.md`, `CLAUDE.md`, `next-agents.md` and `next-operator.md`;
  `CLAUDE.md` is one import line in every one of them. The exception is
  artifact-dag, which had no `AGENTS.md` or `CLAUDE.md` until this thread.
- **`md/` is half adopted.** Six repos have it. Folders seen: `analysis`,
  `audits`, `docs`, `glossary`, `issues`, `plans`, `tested`, `threads`.
  Two repos keep the same kinds of folder at the root instead; one keeps
  its working material in `in-progress/<topic>/`.
- **Governing documents sit at the root.** `ARCHITECTURE.md` in two repos,
  `SCHEMA.md` in one, `SETUP.md` and `SPEC.md` in one each. None had a
  `POLICY.md`; rules lived in `AGENTS.md` and in skills.
- **Naming disagrees in three places,** settled in §3.
- **Most Markdown-only folders outside `md/` are content, not documents:**
  DAG node folders, tutorial sources and audits, a site's posts, eval
  corpora, test fixtures. The md rule as first stated would have moved
  them.

## 2. What the repos do

| | repos | note |
|---|---|---|
| five named root files | 10 of 11 | the eleventh lacked `AGENTS.md` and `CLAUDE.md` |
| `md/` folder | 6 | `issues` and `plans` most common, then `docs`, `analysis`, `threads` |
| `ARCHITECTURE.md` at root | 2 | one opens with `> Status: draft vN · date` and a thesis section |
| `SCHEMA.md` at root | 1 | the node-format contract downstream repos cite by that name |
| plan as dated folder `YYYY-MM-DD-<slug>/` | 2 | one repo uses flat files with a `> Status:` line |
| analysis as dated folder | 1 | holds 33; header block of date, question, sources, caveat |
| issue files with the model's name in the file name | 2 | `…-claude-opus-5-5.md` |
| thread files at `/end`, redaction map git-ignored | 2 | the `/end` skill already prefers `md/threads/` |
| `md/tested/` per-run reports opened by a tool | 1 | `YYYY-MM-DD-HHMM-<kind>.md` |
| `md/audits/` | 1 | |
| a loose file directly in `md/` | 1 | an operator's own notes |

## 3. Decisions taken (operator, 4 Nov 2026)

1. **The md rule is for documents, not content.** Markdown a tool reads as
   data stays with its tool; `.layoutignore` lists those folders for the
   check, and the README's table says what they are.
2. **Governing documents live under `md/governance/`,** `SCHEMA.md`
   included, not at the root.
3. **`governance`, not `mandates`.** Doctrine says why, policy says what is
   required and is checked by something, procedure says how, schema says
   what the data looks like, architecture says how the parts fit. A rule
   nobody checks is doctrine.
4. **Dated folders for analysis and plans, dated files for issues and
   threads; the plan status line; no model name in issue file names.**
5. **`audits/` and `tested/` are defaults,** making eight folders. The
   repo that keeps working material at its root should adopt the layout;
   the repo built on another project's conventions is out of scope.
6. **`README.md` and an MIT `LICENSE` at the root,** with the five named
   files.
7. **Three layers.** repo-template is the template for every repo.
   artifact-dag is the source for any repo that keeps a DAG: its schema,
   its policy on claims, its tools and its `dag` skill. artifact-template,
   planned on 2 Nov in a private repo as a renaming and growth of the
   tutorial builder's repo, is the template for an *artifact*: a repo that
   represents another repo in prose, figures, a command-line lab, a DAG and
   code anchors. It builds on both: its layout contract is a pointer to
   repo-template plus what an artifact adds (`dag/`, `tutorials/`, the
   glossary and viewer configs, the wrappers and CI), and its DAG pieces
   come from artifact-dag. The plan is amended to say so (operator, 4 Nov).
8. **artifact-dag is aligned first,** as the repo this template was built
   beside.

## 4. Recommendations not yet decided

- **How existing repos run the check.** Turn on GitHub's template setting
  for new repos, and have the `/start` skill run `bin/check-layout.sh`
  whenever `~/dev/repos/repo-template` exists, so drift is reported in
  every session. The decision is in `next-operator.md`.
