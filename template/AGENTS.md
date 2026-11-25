# <repo>: working rules

Rules for any agent (Claude Code, Codex, Gemini and others) and for people. The rules every repo shares are in [repo-template's README](https://github.com/markreveley/repo-template#the-rules); this file adds the repo's own. `CLAUDE.md` imports this file and adds nothing. It holds only the rules in force, with their reasons: no state, no next steps and no history (repo-template R32).

## Read first

1. `README.md`: what the repo is and the table of what is where.
2. `state.md` (what is true now) and `next.md` (what to do next, in order): where the last thread stopped. `/start` reads them; `/end` rewrites them. What to work on comes from `next.md`, not from reading other documents. Change `next.md` with `/update-next` (repo-template R30).
3. The governing documents in `md/governance/`, if the repo has any: `ARCHITECTURE.md` before changing how the parts fit, `POLICY.md` before any change (its rules are numbered so you can cite them), `SCHEMA.md` before writing data the repo holds, `PROCEDURE.md` before running one of its methods.

## Where things are

- `<code or data folders>`: <one line each>.
- `md/`: every document about the repo. `md/README.md` lists the folders; each folder's README says what is in it here and links to repo-template's rules for it.
- `LOCAL.md` (git-ignored): names of private projects, local paths, and anything else that stays on one machine. This repo is <public|private>; <if public:> name no private project in any tracked file.

## Working

- Commit and push straight to `main`, without asking (repo-template R29). <Or the repo's exception, with its reason.>
- Before changing a contract (`SCHEMA.md`, a CLI, a file format), check who reads it: <downstream repos, CI>.
- Tests: `<command>`. Run them before pushing.
- Threads are archived to direction with `/archive-thread`, not kept in this repo (repo-template R21).

## This repo's own rules

- <rule, with its reason>
