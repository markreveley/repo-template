# repo-template: working rules

Rules for any agent and for people working on repo-template itself. repo-template is also a client repo of its own rules (README, "The rules"). `CLAUDE.md` imports this file and adds nothing.

## Read first

1. `README.md`: the layout, the rules (R1 to R32) and the check. It is the contract every client repo follows.
2. `state.md` (what is true now) and `next.md` (what to do next, in order). Change `next.md` with `/update-next` (R30).
3. `template/`: the files a new client repo starts from (`README.md`, `AGENTS.md`, `CLAUDE.md`, `state.md`, `next.md`, `.gitignore`), the rules for each `md/` folder (`template/md/<folder>/README.md`), the forms of the five governing documents, and the rules for `_scheduled/`. These are what client repos read and copy; repo-template's own files are at the root and in `md/`.

## Where things are

- `bin/check_layout.py`: the check. Each check is an entry in `CHECKS`, with its rule and its line in the README's table.
- `bin/client_sync.py`: the sync record, `--init`, `--migrate`, and the report of what changed since a client repo's last sync.
- `tests/test_tools.py`: tests of both, in throwaway repos. `python3 -m unittest discover tests`.
- `md/`: repo-template's own documents (the layout survey, the Python-port plan).

## Working

- Commit and push straight to `main`, without asking (R29).
- Run the tests and `bin/check_layout.py` before pushing.
- A change to `template/` or the README's rules reaches every client repo through `/client-sync`, which shows it as a diff to take up. Keep those files free of anything that is about repo-template alone, and don't make whitespace-only edits to them.
- A new or changed check changes the README's table: paste `bin/check_layout.py --list-checks` between the `checks:start` and `checks:end` markers. The tests fail until the two match.
- "Client repo" means a repo laid out from this one. Use the term only in text that is about repo-template (the README, `bin/`). Text in `template/` that a client repo copies or reads says "the repo", meaning that client repo.
- Separate claims go in bullets, not prose (operator preference).
