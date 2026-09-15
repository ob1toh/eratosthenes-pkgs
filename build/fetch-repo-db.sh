#!/bin/bash
# Download a complete pair of existing databases before an incremental update.
set -euo pipefail
out=${1:?Usage: fetch-repo-db.sh OUTPUT_DIRECTORY}
mirror=${MIRROR:-edge}
arch=${ARCH:-x86_64}
base=${REPO_BASE_URL:-https://pkgs.trevorndlovu.com}
mkdir -p "$out"
tmp=$(mktemp -d)
trap 'rm -rf "$tmp"' EXIT
# The legacy database supplies existing package entries during the first rename.
for name in eratosthenes hyprdots; do
  status=$(curl -sS -L -o "$tmp/db" -w '%{http_code}' "$base/$mirror/$arch/$name.db")
  if [[ $status == 404 ]]; then
    continue
  fi
  [[ $status == 200 ]] || { echo "Database download failed: HTTP $status" >&2; exit 1; }
  curl -fsSL "$base/$mirror/$arch/$name.files" -o "$tmp/files"
  tar -tf "$tmp/db" >/dev/null
  tar -tf "$tmp/files" >/dev/null
  cp "$tmp/db" "$out/eratosthenes.db.tar.zst"
  cp "$tmp/files" "$out/eratosthenes.files.tar.zst"
  echo "Loaded existing $name database for $mirror/$arch"
  exit 0
done
echo "No existing database found. Seed this channel explicitly before publishing." >&2
exit 1
