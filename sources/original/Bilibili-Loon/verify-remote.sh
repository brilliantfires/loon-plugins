#!/bin/zsh
set -euo pipefail

root="$(cd "$(dirname "$0")" && pwd)"
tmpdir="$(mktemp -d "${TMPDIR:-/tmp}/bilibili-loon-verify.XXXXXX")"
trap 'rm -rf "$tmpdir"' EXIT

current="https://raw.githubusercontent.com/kokoryh/Sparkle/caf42c487706787431109cc105e93fcec8fc61cd"
snapshot="https://raw.githubusercontent.com/kokoryh/Sparkle/1bc5b545a544d7d59b1cf821785daddc3868e4a5"

fetch_and_compare() {
  local url="$1"
  local local_file="$2"
  local remote_file="$tmpdir/$(basename "$local_file")"
  curl -L --compressed -fsS --max-time 60 "$url" -o "$remote_file"
  cmp "$remote_file" "$root/$local_file"
}

fetch_and_compare "$current/release/loon/plugin/bilibili.lpx" "upstream/kokoryh-bilibili-2026-11-01.lpx"
fetch_and_compare "$current/dist/bilibili.protobuf.response.js" "scripts/upstream-response-2026-11-01.js"
fetch_and_compare "$current/dist/bilibili.protobuf.request.js" "scripts/upstream-request-2026-11-01.js"
fetch_and_compare "$current/dist/bilibili.json.js" "scripts/upstream-json-2026-11-01.js"
fetch_and_compare "$current/dist/webpage.bilibili.js" "scripts/upstream-webpage-2026-11-01.js"
fetch_and_compare "$current/jq/bilibili.tab.jq" "upstream/bilibili.tab.jq"
fetch_and_compare "$current/jq/bilibili.mine.jq" "upstream/bilibili.mine.jq"

fetch_and_compare "$snapshot/release/loon/plugin/bilibili.lpx" "upstream/kokoryh-bilibili-2026-09-15-snapshot.lpx"
fetch_and_compare "$snapshot/dist/bilibili.protobuf.response.js" "scripts/snapshot-response-2026-09-15.js"
fetch_and_compare "$snapshot/dist/bilibili.protobuf.request.js" "scripts/snapshot-request-2026-09-15.js"

echo "OK: all pinned upstream plugin/script/jq files match the archived local copies"
