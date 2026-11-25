#!/usr/bin/env python3
"""client_sync.py: keep a client repo in step with repo-template (README, R31).

  client_sync.py [repo]             report what changed in repo-template since the repo's last sync
  client_sync.py --names [repo]     the same, file names only
  client_sync.py --mark [repo]      record repo-template's current commit as synced
  client_sync.py --init [repo]      start a repo: copy template/ in without overwriting, write the sync record
  client_sync.py --migrate [repo]   --init, plus strip pre-2026-11-24 pinned blocks and drop title-only governing documents

Exit codes: 0 nothing to take up (or the action succeeded), 1 changes to take up, 2 error.
Standard library only; Python 3.9 or later.
"""
import os
import re
import shutil
import subprocess
import sys

HERE = os.path.dirname(os.path.dirname(os.path.realpath(__file__)))  # repo-template
TEMPLATE = os.path.join(HERE, "template")
SYNC_FILE = os.path.join("md", "docs", "repo-template-sync.md")
DEFAULT_FOLDERS = ["governance", "docs", "plans", "analysis", "issues", "audits", "tested"]
GOVERNING = ["ARCHITECTURE", "POLICY", "SCHEMA", "PROCEDURE", "DOCTRINE"]
WATCHED = ["template", "README.md"]  # what a client repo takes up from repo-template
RULES_URL = "https://github.com/markreveley/repo-template/blob/main/template/md/{}README.md"
PIN_MARKER = re.compile(r"\n*(?:^---\n+)?^<!-- pinned from repo-template .*", re.S | re.M)
SHA = re.compile(r"^synced:\s*([0-9a-f]{7,40})\s*$", re.M)


def git(*args):
    r = subprocess.run(["git", "-C", HERE] + list(args), capture_output=True, text=True)
    if r.returncode != 0:
        raise RuntimeError(r.stderr.strip() or "git " + " ".join(args) + " failed")
    return r.stdout


def head():
    return git("rev-parse", "HEAD").strip()


def synced_commit(root):
    """The commit in the repo's sync record, or None."""
    p = os.path.join(root, SYNC_FILE)
    if not os.path.isfile(p):
        return None
    with open(p) as f:
        m = SHA.search(f.read())
    return m.group(1) if m else None


def changed_since(commit):
    """Files under WATCHED that changed in repo-template between commit and HEAD."""
    out = git("diff", "--name-only", commit, "HEAD", "--", *WATCHED)
    return [l for l in out.splitlines() if l]


def folder_readme(folder):
    """A client repo's starting README for an md/ folder: says what it holds here, links to the rules."""
    rel = folder + "/" if folder else ""
    name = (folder or "md") + "/"
    return (
        f"# {name}\n\n"
        f"<What this folder holds in this repo.>\n\n"
        f"Rules for this folder (what belongs here, naming, form): "
        f"[repo-template]({RULES_URL.format(rel)}).\n"
    )


def write_sync_record(root, commit):
    p = os.path.join(root, SYNC_FILE)
    os.makedirs(os.path.dirname(p), exist_ok=True)
    if os.path.isfile(p):
        with open(p) as f:
            text = f.read()
        text = SHA.sub("synced: " + commit, text) if SHA.search(text) else text.rstrip() + "\n\nsynced: " + commit + "\n"
    else:
        with open(os.path.join(TEMPLATE, SYNC_FILE)) as f:
            text = f.read().replace("synced: <repo-template commit>", "synced: " + commit)
    with open(p, "w") as f:
        f.write(text)


def init(root, say):
    """Copy template/ into root without overwriting; folder READMEs are written as client stubs."""
    for dirpath, _, files in os.walk(TEMPLATE):
        rel_dir = os.path.relpath(dirpath, TEMPLATE)
        for name in files:
            rel = os.path.normpath(os.path.join(rel_dir, name))
            if rel == SYNC_FILE:
                continue
            parts = rel.split(os.sep)
            # md/ READMEs and governing documents stay in repo-template as rules; the repo gets stubs or nothing.
            if parts[0] == "md":
                continue
            if parts[0] == "_scheduled":
                continue  # optional folder; its rules stay in repo-template (R28)
            dest = os.path.join(root, rel)
            if not os.path.exists(dest):
                os.makedirs(os.path.dirname(dest), exist_ok=True)
                shutil.copyfile(os.path.join(dirpath, name), dest)
                say("added " + rel)
    for folder in [""] + DEFAULT_FOLDERS:
        dest = os.path.join(root, "md", folder, "README.md")
        if not os.path.exists(dest):
            os.makedirs(os.path.dirname(dest), exist_ok=True)
            with open(dest, "w") as f:
                f.write(folder_readme(folder))
            say("added " + os.path.relpath(dest, root))
    if not synced_commit(root):
        write_sync_record(root, head())
        say("added " + SYNC_FILE)


def migrate(root, say):
    """Strip pinned blocks, link folder READMEs to their rules, drop governing documents left with only a title."""
    for folder in [""] + DEFAULT_FOLDERS:
        p = os.path.join(root, "md", folder, "README.md")
        if not os.path.isfile(p):
            continue
        with open(p) as f:
            text = f.read()
        new = PIN_MARKER.sub("\n", text).rstrip() + "\n"
        rel = folder + "/" if folder else ""
        if "template/md/" + rel + "README.md" not in new:
            new += f"\nRules for this folder (what belongs here, naming, form): [repo-template]({RULES_URL.format(rel)}).\n"
        if new != text:
            with open(p, "w") as f:
                f.write(new)
            say("updated " + os.path.relpath(p, root))
    gov = os.path.join(root, "md", "governance")
    for g in GOVERNING:
        p = os.path.join(gov, g + ".md")
        if not os.path.isfile(p):
            continue
        with open(p) as f:
            text = f.read()
        new = PIN_MARKER.sub("\n", text).strip()
        if len([l for l in new.splitlines() if l.strip()]) <= 1:
            os.remove(p)
            say("removed " + os.path.relpath(p, root) + " (held only its title; governing documents are optional, R10)")
        elif new + "\n" != text:
            with open(p, "w") as f:
                f.write(new + "\n")
            say("updated " + os.path.relpath(p, root))


def main(argv):
    action = "report"
    args = []
    for a in argv:
        if a in ("--names", "--mark", "--init", "--migrate"):
            action = a[2:]
        elif a in ("-h", "--help"):
            print(__doc__)
            return 0
        else:
            args.append(a)
    root = args[0] if args else "."
    if not os.path.isdir(root):
        print("no such directory: " + root, file=sys.stderr)
        return 2
    try:
        if action in ("init", "migrate"):
            init(root, print)
            if action == "migrate":
                migrate(root, print)
            return 0
        if action == "mark":
            write_sync_record(root, head())
            print("synced: " + head())
            return 0
        commit = synced_commit(root)
        if not commit:
            print("no sync record: " + SYNC_FILE + " (run with --init or --migrate)")
            return 1
        try:
            files = changed_since(commit)
        except RuntimeError as e:
            print(f"repo-template has no commit {commit} (fetch its full history): {e}", file=sys.stderr)
            return 2
        if not files:
            print("in step with repo-template " + head()[:7])
            return 0
        print(f"repo-template changed since {commit[:7]} (now {head()[:7]}):")
        for f in files:
            print("  changed " + f)
        if action == "report":
            print()
            print(git("diff", commit, "HEAD", "--", *WATCHED))
        print("Take up what applies to this repo, then run with --mark.")
        return 1
    except RuntimeError as e:
        print(str(e), file=sys.stderr)
        return 2


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
