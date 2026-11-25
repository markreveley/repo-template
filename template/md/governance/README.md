# governance/

The documents that govern the repo. Each of the five is optional: a repo
creates one the first time it has something to put in it, starting from
the form in repo-template's copy of that file (repo-template README, R10).

- [`ARCHITECTURE.md`](ARCHITECTURE.md)
- [`POLICY.md`](POLICY.md)
- [`SCHEMA.md`](SCHEMA.md)
- [`PROCEDURE.md`](PROCEDURE.md)
- [`DOCTRINE.md`](DOCTRINE.md)

How they relate:

- Doctrine says why; policy says what is required; procedure says how it
  is done; schema says what the data looks like; architecture says how the
  parts fit.
- A rule nobody checks and nothing enforces is doctrine, not policy.
- A policy cites the doctrine it serves.
- A procedure cites the policies it satisfies.
- An architecture decision cites both.

**Does not belong here:** a guide or a document about one piece of the
repo (`docs/`), a plan (`plans/`), an analysis (`analysis/`).
