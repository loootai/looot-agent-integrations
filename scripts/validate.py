#!/usr/bin/env python3
"""Validate every config in this repo: JSON, TOML, YAML (via ruby), skill frontmatter, no secrets."""
import json, pathlib, re, subprocess, sys, tomllib

root = pathlib.Path(__file__).resolve().parent.parent
errors = []
URL = "https://api.looot.ai/mcp"

def strip_jsonc(t):
    return re.sub(r"^\s*//.*$", "", t, flags=re.M)

for p in sorted((root / "configs").iterdir()):
    t = p.read_text()
    try:
        if p.suffix in (".json", ".jsonc"):
            json.loads(strip_jsonc(t))
        elif p.suffix == ".toml":
            tomllib.loads(t)
        elif p.suffix == ".yaml":
            r = subprocess.run(["ruby", "-ryaml", "-e", "YAML.load(STDIN.read)"], input=t, text=True, capture_output=True)
            if r.returncode:
                errors.append(f"{p.name}: yaml {r.stderr.strip()}")
    except Exception as e:
        errors.append(f"{p.name}: {e}")
    if URL not in t:
        errors.append(f"{p.name}: missing {URL}")

# platform-specific shape checks
oc = json.loads((root / "configs/opencode.json").read_text())
assert oc["mcp"]["looot"]["type"] == "remote", "opencode type"
assert json.loads((root / "configs/zed.settings.json").read_text())["context_servers"]["looot"]["url"] == URL
assert "mcp_servers" in tomllib.loads((root / "configs/codex.config.toml").read_text())

# skills
for s in (root / "skills").glob("*/SKILL.md"):
    t = s.read_text()
    m = re.match(r"---\n(.*?)\n---\n", t, re.S)
    if not m:
        errors.append(f"{s}: no frontmatter"); continue
    fm = m.group(1)
    name = re.search(r"^name: (.+)$", fm, re.M)
    if not name or name.group(1) != s.parent.name:
        errors.append(f"{s}: name must equal folder")
    if "description:" not in fm:
        errors.append(f"{s}: no description")

# kilo marketplace entry required fields
k = (root / "kilo-marketplace/mcps/looot/MCP.yaml").read_text()
for f in ("id", "name", "description", "author", "url", "category", "content"):
    if not re.search(rf"^{f}:", k, re.M):
        errors.append(f"MCP.yaml: missing {f}")

# secret scan
pat = re.compile(r"cs_ms_[A-Za-z0-9_-]{8,}|sk-[A-Za-z0-9_-]{20,}|ghp_[A-Za-z0-9]{20,}|onrender\.com|127\.0\.0\.1|8787")
for p in root.rglob("*"):
    if p.is_file() and ".git/" not in str(p) and p.name != "validate.py":
        if pat.search(p.read_text(errors="ignore")):
            errors.append(f"{p.relative_to(root)}: leak pattern")

if errors:
    print("\n".join(errors)); sys.exit(1)
print("ok: all configs, skills and Kilo entry valid")
