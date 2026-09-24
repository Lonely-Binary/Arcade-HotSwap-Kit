"""Check local links, Python syntax and English-only text.

The pin lists in the examples are checked against the PCB net lists by the
handbook's tests, which read this repository at its release tag.
"""
import ast
from pathlib import Path
import re
from urllib.parse import unquote
import xml.etree.ElementTree as ET

ROOT = Path(__file__).resolve().parents[1]
errors = []
links = 0
for path in ROOT.rglob("*.md"):
    for target in re.findall(r"\]\(([^)]+)\)", path.read_text()):
        target = unquote(target.split("#", 1)[0])
        if not target or re.match(r"[a-z]+:", target):
            continue
        links += 1
        if not (path.parent / target).exists():
            errors.append("Broken link: %s -> %s" % (path.relative_to(ROOT), target))

python_files = list((ROOT / "examples").rglob("*.py"))
for path in python_files:
    ast.parse(path.read_text(), filename=str(path))
for path in [*ROOT.rglob("*.md"), *python_files, *(ROOT / "examples").rglob("*.ino")]:
    if re.search(r"[\u4e00-\u9fff]", path.read_text()):
        errors.append("Non-English text in: " + str(path.relative_to(ROOT)))

if errors:
    raise SystemExit("\n".join(errors))
print("PASS: %d local links, %d Python files." % (links, len(python_files)))
