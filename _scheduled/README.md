# _scheduled: scheduled tasks

*Added November 21, 2026.*

`_scheduled/` holds the definitions of the repo's scheduled tasks: work an agent runs on a timer, with no one watching. A client repo with no scheduled task does not need the folder.

## Policy

- **One file per task.** The file is named for what the task does, in kebab-case (`init-new-day.md`, `weekly-review-draft.md`).
- **The file is the source of truth.** The scheduler holds only a short prompt that names the repo and the file and says to carry it out. To change what a task does, edit its file. The schedule itself (the cron line and time zone) lives in the scheduler, and the file's second line records it, so the two are changed together.
- **Visible, not hidden.** The folder starts with an underscore, not a dot. A dot folder is tooling state (`.git`, `.github`); these files are documents that people and agents read and edit, and dot folders are skipped by many searches and globs. The underscore matches other non-content folders such as `_posts/`.
- **Outside the content structure.** Tools and tasks that enumerate the repo's dated or content folders skip `_scheduled/`. Say so in each task that scans folders.
- **A task is idempotent.** Run twice, it does the same as run once. It checks first whether its work is already done and, if so, stops without changing anything.
- **A task never overwrites.** It creates or appends; it does not edit earlier work, and it does not write anything the operator alone reports (a check, a decision, a journal entry).
- **A task states its own failure behavior.** For example: retry a failed push once, then report the error in the final message and force nothing.
- **A task is written to run cold.** Each run starts a fresh session with no memory of any thread. Everything the run needs is in the file or in the repo it clones.
- **The repo's own rules win.** If a task file disagrees with `AGENTS.md` or a governing document, those win; fix the task file.
- **Say which time zone.** A date in a task means the date in the time zone the file names, not UTC.

## Structure of a task file

```
# Scheduled task: <name>

*Runs <schedule in words> <time zone>. Created <date>.*

<One or two lines: the file is the source of truth; edit it to change the task.>

## Task

<What the task does, as numbered steps. The first step reads the repo's rules.
Early steps check whether the work is already done and stop if so.
The last step says where the result goes (commit message, branch, PR, report).>

## Rules

<What the task must not do. Failure behavior.>
```

## Adding a scheduled task

1. Write `_scheduled/<name>.md` in the structure above and merge it to the default branch. The scheduler's clone must be able to see it.
2. Create the scheduled task with a prompt of the form: "Clone `<owner>/<repo>`, read `_scheduled/<name>.md` and `AGENTS.md`, and carry out the task exactly as written there. <the date's time zone and the done-already check, in one sentence>. Say in the final message what was done."
3. Record the cron line and time zone in the file's second line.
4. Add a line to the repo's `AGENTS.md` under "Where things are" pointing to `_scheduled/`, so an agent knows tasks run unattended against the repo.

## Renaming or retiring

Renaming the folder or a file means updating the scheduler's prompt in the same change. A retired task's file is deleted in the same change that disables the scheduled task; git history keeps it.
