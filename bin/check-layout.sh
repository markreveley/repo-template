#!/usr/bin/env bash
# check-layout.sh [repo-root]: report where a client repo departs from repo-template's layout (README, "What the check enforces").
# Reads the layout, and pinned template text (via skills/template-sync/sync.sh); not the rest of the documents. Exit 1 if there is any finding.
set -u
here=$(cd -P "$(dirname "$0")" && pwd)
root="${1:-.}"
cd "$root" || { echo "no such directory: $root" >&2; exit 2; }
findings=0
say() { findings=$((findings + 1)); printf '%s\n' "$*"; }

# 1. The named root files.
for f in README.md AGENTS.md CLAUDE.md next-agents.md next-operator.md; do
  [ -f "$f" ] || say "missing at root: $f"
done
if [ -f CLAUDE.md ] && ! grep -q '^@AGENTS.md' CLAUDE.md; then
  say "CLAUDE.md does not import AGENTS.md (expected a line '@AGENTS.md')"
fi

# 2. Loose documents at the root: any .md other than the named files and LICENSE-like names.
for f in *.md; do
  [ -e "$f" ] || continue
  case "$f" in
    README.md|AGENTS.md|CLAUDE.md|next-agents.md|next-operator.md|LOCAL.md|LICENSE.md|CHANGELOG.md) ;;
    *) say "loose document at root: $f (a governing document goes in md/governance/, anything else under md/)" ;;
  esac
done

# 3. md/: the seven default folders (guideline 1), a README in every folder directly in md/ (guideline 2).
if [ -d md ]; then
  for d in governance docs plans analysis issues audits tested; do
    [ -d "md/$d" ] || say "missing default folder: md/$d/"
  done
  for d in md/*/; do
    [ -d "$d" ] || continue
    [ -f "${d}README.md" ] || say "no README in ${d}"
  done
  for f in md/*.md; do
    [ -e "$f" ] || continue
    [ "$f" = md/README.md ] || say "loose document in md/: $f (it belongs in one of md/'s folders)"
  done
  if [ -d md/governance ]; then
    for f in md/governance/*; do
      case "$(basename "$f")" in
        README.md|ARCHITECTURE.md|POLICY.md|SCHEMA.md|PROCEDURE.md|DOCTRINE.md) ;;
        *) say "unexpected file in md/governance/: $f" ;;
      esac
    done
  fi
else
  say "no md/ folder"
fi

# 4. Pinned template text that no longer matches the template (skills/template-sync/sync.sh says how).
sync="$(dirname "$here")/skills/template-sync/sync.sh"
if [ -x "$sync" ] && [ "$(pwd -P)" != "$(dirname "$here")" ]; then
  while IFS= read -r line; do
    say "pinned template text is out of date: ${line#stale } (run $sync for the diff)"
  done < <("$sync" --stale-only .)
fi

if [ "$findings" -eq 0 ]; then
  echo "layout ok"
  exit 0
fi
echo "$findings finding(s)"
exit 1
