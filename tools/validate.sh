#!/usr/bin/env sh
set -eu

root="$(cd "$(dirname "$0")/.." && pwd -P)"
cd "$root"

req_dirs="capd rpc schemas tools docs scripts"
for d in $req_dirs; do
  [ -d "$d" ] || { echo "ERR: missing required dir: $d" >&2; exit 2; }
done

if find . -name ".DS_Store" -print -quit | grep -q .; then
  echo "ERR: found .DS_Store; delete and ensure .gitignore covers it" >&2
  exit 2
fi

if find . -maxdepth 2 -name "Makefile.bak.*" -print -quit | grep -q .; then
  echo "ERR: found Makefile.bak.*; delete and ignore" >&2
  exit 2
fi

echo "OK: validate passed ($(basename "$root"))"
