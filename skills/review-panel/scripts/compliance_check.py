#!/usr/bin/env python3
"""Check a draft against the funder's format limits, from the run config's COMPLIANCE section.

    compliance_check.py <run_config.md> [--final]

COMPLIANCE lines:
    - pdf | <path> | max_pages: 4 | text_pages: 1-3 | font_pt: 11 | margin_cm: 2 | max_mb: 8
    - markdown | <path> | limits: Summary=550; Risk and reward=1000

PDF: page count, file size, the font size of the body text on each text page (the most common size; smaller sizes such
as superscripts are listed, not failed), and the margin on each side of every page. Markdown: words per section (a
`## ` heading starting with the limit's name, placeholders excluded) and leftover `{...}` placeholders, which fail only
with --final. Exit 1 if anything fails.
"""

from __future__ import annotations

import re
import subprocess
import sys
from collections import Counter
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from panel_config import DocKind, read_sections  # noqa: E402

PT_PER_CM = 72 / 2.54
# pdftotext word boxes include the font's descent (about 3 pt at 11 pt type), so a line whose baseline sits exactly on
# the margin, as LaTeX places the last line of a full page, measures about 0.10 cm inside it. Measured 2026-10-06.
MARGIN_TOLERANCE_CM = 0.15
SIZE_TOLERANCE_PT = 0.06
PLACEHOLDER = re.compile(r"\{[^{}]*\}")
failures: list[str] = []


def report(ok: bool, text: str) -> None:
    print(("ok    " if ok else "FAIL  ") + text)
    if not ok:
        failures.append(text)


def page_range(spec: str, n: int) -> list[int]:
    if not spec:
        return list(range(1, n + 1))
    a, _, b = spec.partition("-")
    return list(range(int(a), int(b or a) + 1))


def check_pdf(path: Path, opts: dict[str, str]) -> None:
    info = subprocess.run(["pdfinfo", str(path)], capture_output=True, text=True, check=True).stdout
    n = int(re.search(r"^Pages:\s+(\d+)", info, re.M).group(1))
    if "max_pages" in opts:
        report(n <= int(opts["max_pages"]), f"{path.name}: {n} pages (limit {opts['max_pages']})")
    if "max_mb" in opts:
        mb = path.stat().st_size / 1e6
        report(mb <= float(opts["max_mb"]), f"{path.name}: {mb:.2f} MB (limit {opts['max_mb']} MB)")
    if "font_pt" in opts:
        target = float(opts["font_pt"])
        for p in page_range(opts.get("text_pages", ""), n):
            xml = subprocess.run(["mutool", "draw", "-F", "stext", "-o", "-", str(path), str(p)],
                                 capture_output=True, text=True, check=True).stdout
            sizes = Counter()
            for m in re.finditer(r'<font name="[^"]*" size="([\d.]+)">(.*?)</font>', xml, re.S):
                sizes[round(float(m.group(1)), 2)] += len(re.findall(r"<char ", m.group(2)))
            body = sizes.most_common(1)[0][0] if sizes else 0
            other = ", ".join(f"{s} pt x{c}" for s, c in sorted(sizes.items()) if abs(s - body) > SIZE_TOLERANCE_PT)
            report(abs(body - target) <= SIZE_TOLERANCE_PT,
                   f"{path.name} p{p}: body text {body} pt (required {target}){'; also ' + other if other else ''}")
    if "margin_cm" in opts:
        need = float(opts["margin_cm"])
        bbox = subprocess.run(["pdftotext", "-bbox", str(path), "-"], capture_output=True, text=True, check=True).stdout
        for p, page in enumerate(re.findall(r"<page (.*?)</page>", bbox, re.S), 1):
            w, h = (float(x) for x in re.search(r'width="([\d.]+)" height="([\d.]+)"', page).groups())
            boxes = [tuple(map(float, b)) for b in
                     re.findall(r'xMin="([\d.]+)" yMin="([\d.]+)" xMax="([\d.]+)" yMax="([\d.]+)"', page)]
            if not boxes:
                continue
            left, top = min(b[0] for b in boxes), min(b[1] for b in boxes)
            right, bottom = w - max(b[2] for b in boxes), h - max(b[3] for b in boxes)
            worst = min(left, top, right, bottom) / PT_PER_CM
            report(worst >= need - MARGIN_TOLERANCE_CM,
                   f"{path.name} p{p}: smallest margin {worst:.2f} cm (left {left / PT_PER_CM:.2f}, right "
                   f"{right / PT_PER_CM:.2f}, top {top / PT_PER_CM:.2f}, bottom {bottom / PT_PER_CM:.2f}; need {need})")


def check_markdown(path: Path, opts: dict[str, str], final: bool) -> None:
    text = path.read_text()
    chunks = re.split(r"^## ", text, flags=re.M)
    for item in filter(None, (x.strip() for x in opts.get("limits", "").split(";"))):
        name, _, limit = item.rpartition("=")
        body = next((c.split("\n", 1)[1] for c in chunks if c.startswith(name.strip())), None)
        if body is None:
            report(False, f"{path.name}: no section starting '{name.strip()}'")
            continue
        words = len(PLACEHOLDER.sub("", body.split("\n---")[0]).split())
        report(words <= int(limit), f"{path.name} '{name.strip()}': {words} words (limit {limit})")
    left = PLACEHOLDER.findall(text.split("## ", 1)[-1])
    msg = f"{path.name}: {len(left)} placeholders left"
    if final:
        report(not left, msg)
    else:
        print(f"info  {msg} (allowed in a draft; fails with --final)")


def main(config_path: str, final: bool) -> int:
    for line in read_sections(Path(config_path)).get("COMPLIANCE", "").splitlines():
        if not line.strip().startswith("- "):
            continue
        parts = [x.strip() for x in line.strip()[2:].split(" | ")]
        kind, path = DocKind(parts[0]), Path(parts[1])
        opts = {k.strip(): v.strip() for k, _, v in (p.partition(":") for p in parts[2:])}
        if kind == DocKind.PDF:
            check_pdf(path, opts)
        else:
            check_markdown(path, opts, final)
    print(f"\n{len(failures)} failure(s)")
    return 1 if failures else 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1], "--final" in sys.argv))
