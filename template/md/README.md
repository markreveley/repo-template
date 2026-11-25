# md/

The repo's documents about itself and its work. The seven folders below
exist in every repo, each with its README, whether or not anything is in it
yet (repo-template README, R5 and R6).

| folder | holds | file name |
|---|---|---|
| [`governance/`](governance/README.md) | the documents that govern the repo | the five fixed names |
| [`docs/`](docs/README.md) | how to use and work on what the repo holds | `<topic>.md` |
| [`plans/`](plans/README.md) | what will be done, in order, and what it waits on | `YYYY-MM-DD-<slug>/<slug>.md` |
| [`analysis/`](analysis/README.md) | dated findings and recommendations | `YYYY-MM-DD-<slug>/<slug>.md` |
| [`issues/`](issues/README.md) | dated findings against something | `YYYY-MM-DD-<slug>.md` |
| [`audits/`](audits/README.md) | a dated reading of the repo against what it claims to be | `YYYY-MM-DD-<slug>.md` |
| [`tested/`](tested/README.md) | one report per run of something only a run can check | `YYYY-MM-DD-HHMM-<kind>.md` |

These files in repo-template's `template/md/` say what belongs in each
folder and what does not. In a repo, each folder's README says what is in it
there and links to the matching file here (R7). A repo may add a folder
(`glossary/` exists elsewhere) if it gives it a README that says what belongs
there and how files are named, and a row in its `md/README.md` table (R8).

Where a document goes when it could go in two places:

- It says what to do next: a plan. It says what was found: an analysis. A
  document that does both is an analysis whose recommendations become a
  plan's steps, linked both ways.
- It records a problem in something: an issue. Something was learned from
  fixing it: `docs/`.
- It is a rule, a format, a method, a design or a principle that the repo
  lives by: governance. One that applies to one piece of the repo only:
  `docs/`.
- No document here holds an open question. A question that blocks the next
  step is an `(operator)` step in `next.md`; any other goes in a plan linked from it.
