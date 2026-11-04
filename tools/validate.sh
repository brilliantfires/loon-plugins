#!/bin/zsh
set -euo pipefail

root="$(cd "$(dirname "$0")/.." && pwd)"
cd "$root"

expected=27
count="$(find plugins -maxdepth 1 -type f -name '*.lpx' | wc -l | tr -d ' ')"
if [[ "$count" -ne "$expected" ]]; then
  echo "Expected $expected plugins, found $count" >&2
  exit 1
fi

if rg -n '192\.168\.|127\.0\.0\.1|localhost|\[Mitm\]' plugins scripts; then
  echo "Found local or legacy dependency" >&2
  exit 1
fi

for file in plugins/*.lpx; do
  for key in name desc homepage tag system system_version loon_version author date; do
    if ! rg -q "^#!${key}=" "$file"; then
      echo "$file: missing #!${key}" >&2
      exit 1
    fi
  done

  name="$(awk -F= '/^#!name=/{print substr($0,8); exit}' "$file")"
  if [[ -z "$name" ]]; then
    echo "$file: empty name" >&2
    exit 1
  fi
  if [[ "$name" == *"去广告"* || "$name" == *"("* || "$name" == *"（"* ]]; then
    echo "$file: display name is not a concise application name: $name" >&2
    exit 1
  fi

  if ! rg -q '^\[(Rule|Rewrite|Script)\]$' "$file"; then
    echo "$file: no functional section" >&2
    exit 1
  fi
  if rg -q '^\[(Rewrite|Script)\]$' "$file" && ! awk '
    /^\[MitM\]/{inside=1; next}
    /^\[/{inside=0}
    inside && /^hostname *= *[^ ]/{found=1}
    END{exit(found ? 0 : 1)}
  ' "$file"; then
    echo "$file: rewrite/script without MitM hostname" >&2
    exit 1
  fi
done

for file in plugins/*.lpx; do
  awk '
    /^\[/{section=$0; next}
    section ~ /^\[(Rule|Rewrite|Script)\]$/ && /^(AND|DOMAIN|IP-CIDR|request|response) / {print section "\t" $0}
  ' "$file" | sort | uniq -d > /tmp/loon-plugin-duplicates.txt
  if [[ -s /tmp/loon-plugin-duplicates.txt ]]; then
    echo "$file: duplicate rules found" >&2
    cat /tmp/loon-plugin-duplicates.txt >&2
    exit 1
  fi
done

while IFS= read -r script_name; do
  if [[ ! -f "scripts/$script_name" ]]; then
    echo "Missing script dependency: scripts/$script_name" >&2
    exit 1
  fi
done < <(
  rg -o 'raw\.githubusercontent\.com/brilliantfires/loon-plugins/main/scripts/[^"]+' plugins/*.lpx \
    | sed 's#.*/scripts/##' \
    | sort -u
)

catalog_count="$(jq 'length' catalog.json)"
if [[ "$catalog_count" -ne "$expected" ]]; then
  echo "catalog.json has $catalog_count entries, expected $expected" >&2
  exit 1
fi

echo "Validated $count plugins"
