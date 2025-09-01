#!/usr/bin/env python3
import sys, re
from pathlib import Path

# настройки
INCLUDE_EXT = {".md", ".txt", ".py", ".js", ".ts", ".ps1", ".json", ".yml", ".yaml"}
SKIP_DIRS = {".git", "node_modules", "dist", "build", "exports", "out", ".venv", "venv", "__pycache__"}

TRACKING_KEYS = [
    r"utm_[a-z0-9_]+", r"gclid", r"fbclid", r"mc_eid", r"igshid", r"yclid", r"dclid"
]

def is_text_file(p: Path) -> bool:
    return p.suffix.lower() in INCLUDE_EXT

def should_skip(p: Path) -> bool:
    parts = set(p.parts)
    return any(skip in parts for skip in SKIP_DIRS)

def check_file(p: Path) -> list[str]:
    issues = []
    try:
        content = p.read_text(encoding="utf-8")
    except Exception:
        return issues

    if "—" in content or "–" in content:
        issues.append("contains long dash, use hyphen '-' only")

    url_params = re.findall(r"[?&]([a-z0-9_]+)=", content, flags=re.I)
    if any(re.fullmatch(k, key, flags=re.I) for key in url_params for k in TRACKING_KEYS):
        issues.append("contains tracking params in URLs, remove utm and similar")

    if "\t" in content:
        issues.append("contains tab characters, use spaces")

    lines = content.splitlines()
    trailing = [i+1 for i, line in enumerate(lines) if len(line) and line.rstrip() != line]
    if trailing:
        issues.append(f"trailing spaces at lines {trailing[:10]}{'...' if len(trailing) > 10 else ''}")

    return [f"{p}: {msg}" for msg in issues]

def main() -> int:
    root = Path(".").resolve()
    problems = []
    for p in root.rglob("*"):
        if p.is_file() and is_text_file(p) and not should_skip(p):
            problems.extend(check_file(p))

    if problems:
        print("Text lint failed:")
        for msg in problems:
            print(" -", msg)
        return 1

    print("Text lint passed")
    return 0

if __name__ == "__main__":
    sys.exit(main())
