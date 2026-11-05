#!/usr/bin/env bash
# sync.sh [--apply | --stale-only | --pin FILE] [repo-root]
# Compare a client repo's pinned repo-template text with the template's HEAD.
#
# A pinned block sits at the bottom of a file, after a `---` line:
#   <!-- pinned from repo-template <path> @ <sha>; refresh from the template, do not edit by hand -->
#   ## About this folder (repo-template `<sha>`)    (a README; a governing document says "About this file")
#   <the template file at <path>, minus its first line (the title)>
#
# Default: report every pin (ok / stale / gone), unpinned folder READMEs and governing documents,
#   template folders the client repo lacks, and the template's changes since the
#   oldest pin to the files a client repo fills in rather than pins.
# --stale-only: print only `stale <file>` lines (check-layout.sh uses this).
# --apply: rewrite stale pins with the template's HEAD text.
# --pin FILE: append a pinned block to FILE (a client repo path under md/). A FILE still identical
#   to the template's is cut to its title line first.
# Exit: 0 nothing to do, 1 something to do, 2 error.
set -u

mode=report pin_file=""
case "${1:-}" in
  --apply) mode=apply; shift ;;
  --stale-only) mode=stale; shift ;;
  --pin) mode=pin; pin_file="${2:-}"; shift 2 || { echo "--pin needs a file" >&2; exit 2; } ;;
esac
# The template is the checkout this script lives in (cd -P resolves a linked skill dir).
tdir="${REPO_TEMPLATE:-$(cd -P "$(dirname "$0")" && cd ../.. && pwd)}"
root="${1:-.}"
cd "$root" || { echo "no such directory: $root" >&2; exit 2; }
root=$(pwd)

git -C "$tdir" rev-parse --git-dir >/dev/null 2>&1 || { echo "not a git checkout: $tdir" >&2; exit 2; }
[ "$root" = "$(cd "$tdir" && pwd -P)" ] && { echo "this is repo-template itself; run it in a client repo" >&2; exit 2; }
head_sha=$(git -C "$tdir" rev-parse --short HEAD)

marker_re='<!-- pinned from repo-template ([^ ]+) @ ([0-9a-f]+);'
todo=0
note() { todo=$((todo + 1)); printf '%s\n' "$*"; }

body_now() { tail -n +2 "$tdir/$1"; }                  # template text, minus title
body_pinned() { awk -v m="$2" 'NR > m + 1' "$1"; }     # after the marker and heading

block() { # path sha -> the pinned block
  printf -- '---\n\n<!-- pinned from repo-template %s @ %s; refresh from the template, do not edit by hand -->\n' "$1" "$2"
  what="folder"; [ "$(basename "$1")" = README.md ] || what="file"
  # shellcheck disable=SC2016 # the backticks are Markdown
  printf '## About this %s (repo-template `%s`)\n' "$what" "$2"
  body_now "$1"
}

if [ "$mode" = pin ]; then
  [ -f "$pin_file" ] || { echo "no such file: $pin_file" >&2; exit 2; }
  [ -f "$tdir/$pin_file" ] || { echo "repo-template has no $pin_file" >&2; exit 2; }
  grep -q 'pinned from repo-template' "$pin_file" && { echo "already pinned: $pin_file" >&2; exit 2; }
  # An unmodified copy of the template's file: keep only its title, so the text is not there twice.
  if cmp -s "$pin_file" "$tdir/$pin_file"; then
    tmp=$(mktemp) && head -n 1 "$pin_file" > "$tmp" && mv "$tmp" "$pin_file"
  fi
  # shellcheck disable=SC2094 # block reads the template's file, not this one
  { printf '\n'; block "$pin_file" "$head_sha"; } >> "$pin_file"
  echo "pinned  $pin_file @ $head_sha"
  exit 0
fi

oldest="" oldest_age=-1
while IFS= read -r f; do
  f=${f#./}
  line=$(grep -nE "$marker_re" "$f" | head -1)
  n=${line%%:*}
  path=$(printf '%s' "$line" | sed -E "s/.*$marker_re.*/\1/")
  sha=$(printf '%s' "$line" | sed -E "s/.*$marker_re.*/\2/")
  if ! [ -f "$tdir/$path" ]; then
    [ "$mode" = stale ] || note "gone    $f: repo-template has no $path now (renamed or removed?)"
    continue
  fi
  # Why it differs: the template changed since the pin (stale), or the pin was edited here (edited).
  why=stale
  if git -C "$tdir" cat-file -e "$sha^{commit}" 2>/dev/null; then
    age=$(git -C "$tdir" rev-list --count "$sha..HEAD")
    [ "$age" -gt "$oldest_age" ] && { oldest=$sha; oldest_age=$age; }
    git -C "$tdir" diff --quiet "$sha" HEAD -- "$path" && why=edited
  fi
  if [ "$(body_pinned "$f" "$n")" = "$(body_now "$path")" ]; then
    [ "$mode" = report ] && printf 'ok      %s (pinned %s)\n' "$f" "$sha"
    continue
  fi
  case "$mode" in
    stale) printf 'stale %s\n' "$f" ;;
    report)
      if [ "$why" = edited ]; then
        note "edited  $f: the pinned text was changed here; --apply restores the template's:"
      else
        note "stale   $f (pinned $sha, template $head_sha); --apply makes it:"
      fi
      diff -u <(body_pinned "$f" "$n") <(body_now "$path") | tail -n +3 | sed 's/^/        /' ;;
    apply)
      sep=$(awk -v m="$n" 'NR < m && /^---$/ { s = NR } END { print s + 0 }' "$f")
      [ "$sep" -gt 0 ] || { echo "no --- before the marker in $f; fix by hand" >&2; exit 2; }
      tmp=$(mktemp)
      { head -n $((sep - 1)) "$f"; block "$path" "$head_sha"; } > "$tmp" && mv "$tmp" "$f"
      printf 'updated %s -> %s\n' "$f" "$head_sha" ;;
  esac
done < <(grep -rlE "$marker_re" --include='*.md' --exclude-dir=.git --exclude-dir=node_modules . | sort)

[ "$mode" = report ] || exit 0

# Folder READMEs and governing documents with no pin, and template folders the client repo lacks.
for f in md/README.md md/*/README.md md/governance/{ARCHITECTURE,POLICY,SCHEMA,PROCEDURE,DOCTRINE}.md; do
  [ -f "$f" ] && [ -f "$tdir/$f" ] || continue
  grep -qE "$marker_re" "$f" || note "unpinned $f (pin with: $0 --pin $f)"
done
for d in "$tdir"/md/*/; do
  [ -d "$d" ] || continue
  d=md/$(basename "$d")
  [ -d "$d" ] || note "missing $d/ (repo-template has it)"
done

# Files a client repo fills in rather than pins: show what changed in the template since the oldest pin.
if [ -n "$oldest" ]; then
  filled=(README.md AGENTS.md CLAUDE.md .gitignore)
  if ! git -C "$tdir" diff --quiet "$oldest" HEAD -- "${filled[@]}"; then
    note "template changes since $oldest to files this client repo fills in (README rules, AGENTS.md, CLAUDE.md, .gitignore):"
    git -C "$tdir" --no-pager diff "$oldest" HEAD -- "${filled[@]}" | sed 's/^/        /'
  fi
fi

[ "$todo" -eq 0 ] && echo "in sync with repo-template $head_sha"
[ "$todo" -eq 0 ]
