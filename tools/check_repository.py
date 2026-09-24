"""Check local links, Python syntax and input maps against the PCB netlists."""
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
for path in (ROOT / "docs/assets").glob("*.svg"):
    ET.parse(path)


def header_map(board, header):
    path = ROOT / ("hardware/netlists/arcade-%s_netlist_2026-09-24.tel" % board)
    text = path.read_text().split("$NETS")[1].split("$SCHEDULE")[0]
    mapping = {}
    for match in re.finditer(r"([^;\n]+) ; ([\s\S]*?)(?=\n[^ \n][^;\n]* ;|\Z)", text):
        net, refs = match.groups()
        for pin in re.findall(r"\b%s\.(\d+)\b" % header, refs):
            mapping[int(pin)] = net.strip().strip("'")
    return mapping


def numbers(values):
    return [re.sub(r"^(GPIO|IO|GP|D)", "", value.strip()) for value in values]


def py_array(path, name):
    for node in ast.parse((ROOT / path).read_text()).body:
        if isinstance(node, ast.Assign) and any(isinstance(t, ast.Name) and t.id == name for t in node.targets):
            return [str(x) for x in ast.literal_eval(node.value)]
    raise ValueError(name)


arduino = (ROOT / "examples/arduino/InputMonitor/InputMonitor.ino").read_text()
arrays = re.findall(r"INPUT_PINS\[\] = \{([^}]+)\}", arduino)
actual = {
    "nano": arrays[0].split(","),
    "esp32-s3": arrays[1].split(","),
    "pico": py_array("examples/pico/arcade.py", "INPUT_PINS"),
    "zero2w": py_array("examples/zero2w/input_monitor.py", "PINS"),
}
for board, values in actual.items():
    pins = header_map(board, "H3" if board in ("nano", "zero2w") else "H1")
    expected = [pins[i] for i in range(4, 18)]
    if numbers(values) != numbers(expected):
        errors.append("Input map differs from netlist: " + board)

for path in [*ROOT.rglob("*.md"), *python_files, *(ROOT / "examples").rglob("*.ino")]:
    if re.search(r"[\u4e00-\u9fff]", path.read_text()):
        errors.append("Non-English text in: " + str(path.relative_to(ROOT)))

if errors:
    raise SystemExit("\n".join(errors))
print("PASS: %d local links, %d Python files, SVG XML and four input maps." % (links, len(python_files)))
