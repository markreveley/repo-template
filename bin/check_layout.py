#!/usr/bin/env python3
"""check_layout.py [repo] | --list-checks: report where a client repo departs from repo-template (README, "What the check enforces").

Reads file and folder names, CLAUDE.md's import, the folder READMEs' links and the sync record; nothing else.
Exit 0 prints "layout ok"; exit 1 means at least one finding; exit 2 means the directory does not exist.
Standard library only; Python 3.9 or later.
"""
import os
import re
import sys

sys.path.insert(0, os.path.dirname(os.path.realpath(__file__)))
import client_sync  # noqa: E402

FOLDERS = client_sync.DEFAULT_FOLDERS
GOVERNING = client_sync.GOVERNING
ROOT_ALLOWED = {"README.md", "AGENTS.md", "CLAUDE.md", "state.md", "next.md", "LOCAL.md", "LICENSE.md", "CHANGELOG.md"}


def read(p):
    try:
        with open(p) as f:
            return f.read()
    except OSError:
        return ""


def root_files(r):
    return [f"missing at root: {f}" for f in ("README.md", "AGENTS.md", "CLAUDE.md") if not os.path.isfile(os.path.join(r, f))]


def state_file(r):
    if os.path.isfile(os.path.join(r, "state.md")):
        return []
    for f in ("AGENTS.md", "next.md"):
        if re.search(r"^## State\b", read(os.path.join(r, f)), re.M):
            return [f"missing at root: state.md (move the State and Environment facts in {f} into it, from template/state.md; R30)"]
    return ["missing at root: state.md (start it from template/state.md)"]


def next_file(r):
    old = [f for f in ("next-agents.md", "next-operator.md") if os.path.isfile(os.path.join(r, f))]
    if os.path.isfile(os.path.join(r, "next.md")):
        return [f"leftover handoff file: {f} (merge its steps into next.md and its state into state.md with /update-next, then delete it; R30)" for f in old]
    if old:
        return [f"old handoff files at root: {', '.join(old)}, and no next.md (merge them with /update-next; R1, R30)"]
    return ["missing at root: next.md"]


def loose_root(r):
    return [f"loose document at root: {f} (a governing document goes in md/governance/, anything else under md/)"
            for f in sorted(os.listdir(r)) if f.endswith(".md") and f not in ROOT_ALLOWED | {"next-agents.md", "next-operator.md"}
            and os.path.isfile(os.path.join(r, f))]


def claude_import(r):
    p = os.path.join(r, "CLAUDE.md")
    if os.path.isfile(p) and not re.search(r"^@AGENTS\.md", read(p), re.M):
        return ["CLAUDE.md does not import AGENTS.md (expected a line '@AGENTS.md')"]
    return []


def md_folders(r):
    if not os.path.isdir(os.path.join(r, "md")):
        return ["no md/ folder"]
    return [f"missing default folder: md/{d}/" for d in FOLDERS if not os.path.isdir(os.path.join(r, "md", d))]


def md_readmes(r):
    md = os.path.join(r, "md")
    if not os.path.isdir(md):
        return []
    return [f"no README in md/{d}/" for d in sorted(os.listdir(md))
            if os.path.isdir(os.path.join(md, d)) and not os.path.isfile(os.path.join(md, d, "README.md"))]


def readme_links(r):
    out = []
    for folder in [""] + FOLDERS:
        p = os.path.join(r, "md", folder, "README.md")
        rel = folder + "/" if folder else ""
        if os.path.isfile(p) and f"template/md/{rel}README.md" not in read(p):
            out.append(f"md/{rel}README.md does not link to its rules (template/md/{rel}README.md in repo-template; R7)")
    return out


def loose_md(r):
    md = os.path.join(r, "md")
    if not os.path.isdir(md):
        return []
    return [f"loose document in md/: md/{f} (it belongs in one of md/'s folders)"
            for f in sorted(os.listdir(md)) if f.endswith(".md") and f != "README.md" and os.path.isfile(os.path.join(md, f))]


def governance_only(r):
    g = os.path.join(r, "md", "governance")
    if not os.path.isdir(g):
        return []
    ok = {"README.md"} | {n + ".md" for n in GOVERNING}
    return [f"unexpected file in md/governance/: {f}" for f in sorted(os.listdir(g)) if f not in ok]


def leftover_pins(r):
    out = []
    for dirpath, _, files in os.walk(os.path.join(r, "md")):
        for f in files:
            p = os.path.join(dirpath, f)
            if f.endswith(".md") and re.search(r"^<!-- pinned from repo-template", read(p), re.M):
                out.append(f"pinned template block left in {os.path.relpath(p, r)} (run /client-sync --migrate; R7)")
    return out


def sync_record(r):
    if not client_sync.synced_commit(r):
        return [f"no sync record: {client_sync.SYNC_FILE} with a 'synced: <commit>' line (run /client-sync --init; R31)"]
    return []


def sync_current(r):
    if os.path.realpath(r) == client_sync.HERE:
        return []
    c = client_sync.synced_commit(r)
    if not c:
        return []
    try:
        files = client_sync.changed_since(c)
    except RuntimeError:
        return [f"repo-template has no commit {c[:7]}; fetch its full history, or the record is wrong (R31)"]
    return [f"repo-template changed since this repo's last sync ({len(files)} file(s)); run /client-sync (R31)"] if files else []


# (description for the README table, rule, function). The README's table is --list-checks; a test keeps them equal.
CHECKS = [
    ("`README.md`, `AGENTS.md` and `CLAUDE.md` exist at the root", "R1", root_files),
    ("`state.md` exists at the root; a repo still keeping State in `AGENTS.md` or `next.md` is told to move it", "R1, R30", state_file),
    ("`next.md` exists at the root; `next-agents.md` and `next-operator.md` are reported for merging", "R1, R30", next_file),
    ("No other `.md` file sits at the root, except `LOCAL.md`, `LICENSE.md` and `CHANGELOG.md`", "R3", loose_root),
    ("`CLAUDE.md` has a line starting `@AGENTS.md`", "R4", claude_import),
    ("`md/` exists, and so do its seven default folders", "R5", md_folders),
    ("Every folder directly in `md/` has a `README.md`", "R6", md_readmes),
    ("`md/README.md` and each default folder's README link to repo-template's rules for that folder", "R7", readme_links),
    ("No `.md` file sits directly in `md/` except `md/README.md`", "R9", loose_md),
    ("`md/governance/` holds only `README.md` and the five governing documents", "R11", governance_only),
    ("No pinned template block from before 2026-11-24 is left in `md/`", "R7", leftover_pins),
    ("`md/docs/repo-template-sync.md` has a `synced:` commit", "R31", sync_record),
    ("No change to `template/` or `README.md` here since that commit (skipped for repo-template itself)", "R31", sync_current),
]


def table():
    rows = ["| Check | Rule |", "| --- | --- |"] + [f"| {d} | {rule} |" for d, rule, _ in CHECKS]
    return "\n".join(rows)


def main(argv):
    if "--list-checks" in argv:
        print(table())
        return 0
    if argv and argv[0] in ("-h", "--help"):
        print(__doc__)
        return 0
    root = argv[0] if argv else "."
    if not os.path.isdir(root):
        print("no such directory: " + root, file=sys.stderr)
        return 2
    findings = [f for _, _, check in CHECKS for f in check(root)]
    for f in findings:
        print(f)
    if findings:
        print(f"{len(findings)} finding(s)")
        return 1
    print("layout ok")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
