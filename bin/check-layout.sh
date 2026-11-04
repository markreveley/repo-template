#!/usr/bin/env bash
# check-layout.sh [repo-root]: report where a repo departs from repo-template's layout.
# Reads the layout only, never the documents. Exit 1 if there is any finding.
set -u
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

# 3. md/ and its folders' READMEs.
if [ -d md ]; then
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

# 4. Markdown-only folders outside md/. Content folders a tool reads (dag/, posts/) are
#    exempt when .layoutignore at the root lists them, one path prefix per line, no leading ./ .
#    The README's table is where a repo says what those folders are.
ignored=()
if [ -f .layoutignore ]; then
  while IFS= read -r line; do
    case "$line" in ''|'#'*) ;; *) ignored+=("./${line%/}") ;; esac
  done < .layoutignore
fi
is_ignored() {
  local d="$1" i
  for i in "${ignored[@]+"${ignored[@]}"}"; do
    case "$d" in "$i"|"$i"/*) return 0 ;; esac
  done
  return 1
}
while IFS= read -r d; do
  is_ignored "$d" && continue
  n=$(find "$d" -mindepth 1 -maxdepth 1 ! -name '.*' | wc -l | tr -d ' ')
  m=$(find "$d" -mindepth 1 -maxdepth 1 -name '*.md' | wc -l | tr -d ' ')
  if [ "$n" -gt 0 ] && [ "$n" -eq "$m" ]; then
    say "markdown-only folder outside md/: $d (content a tool reads? list it in .layoutignore)"
  fi
done < <(find . -type d \
  ! -path './.git' ! -path './.git/*' \
  ! -path './md' ! -path './md/*' \
  ! -path '*/node_modules*' ! -path '*/.venv*' ! -path '*/.cache*' \
  ! -path './.claude*' ! -path './.agents*' ! -path './.github*' \
  ! -path '.' | sort)

if [ "$findings" -eq 0 ]; then
  echo "layout ok"
  exit 0
fi
echo "$findings finding(s)"
exit 1
