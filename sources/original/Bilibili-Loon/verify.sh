#!/bin/zsh
set -euo pipefail

root="$(cd "$(dirname "$0")" && pwd)"
cd "$root"

for script in scripts/*.js; do
  node --check "$script"
done

python3 - <<'PY'
from pathlib import Path
import hashlib
import re
import sys

root = Path.cwd()
required = [
    root / "Bilibili-Ads-Conservative.lpx",
    root / "Bilibili-Ads-Full.lpx",
    root / "Bilibili-Ads-Minimal.lpx",
    root / "upstream/kokoryh-bilibili-2026-09-15-snapshot.lpx",
    root / "upstream/kokoryh-bilibili-2026-11-01.lpx",
    root / "scripts/upstream-response-2026-11-01.js",
]
for path in required:
    if not path.is_file() or path.stat().st_size == 0:
        raise SystemExit(f"missing or empty: {path}")

for name in ("Bilibili-Ads-Conservative.lpx", "Bilibili-Ads-Minimal.lpx"):
    text = (root / name).read_text(encoding="utf-8")
    for section in ("[Argument]", "[Rewrite]", "[MitM]"):
        if section not in text:
            raise SystemExit(f"{name}: missing {section}")
    forbidden = re.search(
        r"DmView|DmSegMobile|ViewProgress|PlayViewUnite|/PlayView(?:\b|$)|"
        r"ModeStatus|DOMAIN,api\.biliapi\.com,REJECT|DOMAIN,app\.biliapi\.com,REJECT",
        text,
    )
    if forbidden:
        raise SystemExit(f"{name}: forbidden endpoint/rule: {forbidden.group(0)}")

conservative = (root / "Bilibili-Ads-Conservative.lpx").read_text(encoding="utf-8")
if conservative.count("caf42c487706787431109cc105e93fcec8fc61cd") != 4:
    raise SystemExit("conservative plugin must pin all four script routes to the archived commit")

full = (root / "Bilibili-Ads-Full.lpx").read_text(encoding="utf-8")
for section in ("[Argument]", "[Rewrite]", "[Script]", "[MitM]"):
    if section not in full:
        raise SystemExit(f"full plugin: missing {section}")
if "||" in full:
    raise SystemExit("full plugin: unsupported || condition remains")
if "response.header.add(\"grpc-status\"" in full:
    raise SystemExit("full plugin: grpc-status must use set")
if full.count("caf42c487706787431109cc105e93fcec8fc61cd") != 12:
    raise SystemExit("full plugin must pin all twelve script/JQ routes to the archived commit")
for option in (
    "commentAds",
    "purifyComment",
    "dynamicAds",
    "videoPageAds",
    "interactiveDanmakuClean",
    "sponsorBlock",
    "playbackEnhance",
    "legacyDomainBlock",
    "webpageClean",
):
    pattern = rf"(?m)^{re.escape(option)}\s*=\s*switch,false,"
    if not re.search(pattern, full):
        raise SystemExit(f"full plugin: {option} must default to false")

script_rules = [
    line
    for line in full.splitlines()
    if line.startswith(("request if ", "response if ")) and "script(" in line
]
danger_guards = {
    "MainList": ("${commentAds} == true", "${optimizeRequest} == true"),
    "DynAll": ("${dynamicAds} == true",),
    "RelatesFeed": ("${videoPageAds} == true",),
    "DmView": ("${interactiveDanmakuClean} == true",),
    "DmSegMobile": ("${sponsorBlock} == true",),
    "ViewProgress": ("${sponsorBlock} == true",),
    "PlayViewUnite": ("${playbackEnhance} == true",),
    "PlayView": ("${playbackEnhance} == true",),
}
for marker, guards in danger_guards.items():
    matching = [line for line in script_rules if marker in line]
    if not matching:
        raise SystemExit(f"full plugin: expected script route missing for {marker}")
    for line in matching:
        if not any(guard in line for guard in guards):
            raise SystemExit(f"full plugin: unguarded script route for {marker}: {line}")

expected = "701d22911e3a3aa9ff87cd94f2f2bffad45e92c5fdcee5019dd97d6e925c55de"
actual = hashlib.sha256((root / "scripts/upstream-response-2026-11-01.js").read_bytes()).hexdigest()
if actual != expected:
    raise SystemExit(f"response script hash mismatch: {actual}")

print("OK: structure, full-version switch guards, pinned commits, and response-script hash")
PY
