#!/usr/bin/env python3
"""Make the review copies a panel reads, from the documents listed in a run config.

    build_pack.py <run_config.md> <out_dir>

For each document in DOCUMENTS:
- pdf: copied as it is, with a plain-text version (pdftotext) for searching. Command-line reviewers get the file named
  by its `text:` option if there is one (a cleaner text with equations and charts written out), else the pdftotext.
- markdown: cut to start at the heading given by `start:` (everything before it is internal), every `{...}`
  placeholder turned into `[PENDING: ...]`, or into `[DRAFT VALUE: ...]` when it holds only a number or a range,
  then rendered to PDF with pandoc. The Markdown itself is the text version.

Writes <out_dir>/pack/, a manifest.json the assembler reads, and placeholders_found.md listing every placeholder,
so the pending-items list given to the panel cannot silently miss one.
"""

from __future__ import annotations

import json
import re
import shutil
import subprocess
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import panel_config  # noqa: E402
from panel_config import DocKind  # noqa: E402

PLACEHOLDER = re.compile(r"\{([^{}]*)\}")
VALUE_ONLY = re.compile(r"[\d.,%£$€\s]+(?:\s*(?:to|-|–)\s*[\d.,%£$€\s]+)?")
PANDOC_HEADER = r"""\usepackage{tgheros}
\renewcommand{\familydefault}{\sfdefault}
\usepackage{newunicodechar}
\newunicodechar{−}{-}
"""


def slug(label: str) -> str:
    return re.sub(r"[^a-z0-9]+", "_", label.lower()).strip("_")


def pages(pdf: Path) -> int:
    out = subprocess.run(["pdfinfo", str(pdf)], capture_output=True, text=True, check=True).stdout
    return int(re.search(r"^Pages:\s+(\d+)", out, re.M).group(1))


def convert_placeholders(text: str, label: str, found: list[dict[str, str]]) -> str:
    def repl(m: re.Match) -> str:
        inner = m.group(1).strip()
        kind = "DRAFT VALUE" if VALUE_ONLY.fullmatch(inner) else "PENDING"
        found.append({"document": label, "kind": kind, "text": inner})
        return f"[{kind}: {inner}]"

    return PLACEHOLDER.sub(repl, text)


def main(config_path: str, out_dir: str) -> None:
    fields = panel_config.load(config_path)
    pack = Path(out_dir) / "pack"
    pack.mkdir(parents=True, exist_ok=True)
    manifest, found = [], []
    for doc in panel_config.documents(fields):
        src, name = Path(doc["path"]), slug(doc["label"])
        if doc["kind"] == DocKind.PDF:
            pdf, txt = pack / f"{name}.pdf", pack / f"{name}.txt"
            shutil.copyfile(src, pdf)
            subprocess.run(["pdftotext", str(pdf), str(txt)], check=True)
            cli_text = Path(doc["text"]) if doc.get("text") else txt
        else:
            body = src.read_text()
            if doc.get("start"):
                body = body[body.index(doc["start"]):]
            body = convert_placeholders(body, doc["label"], found)
            md = pack / f"{name}.md"
            md.write_text(f"# {doc['label']}\n\n{body}")
            header = pack / "pandoc_header.tex"
            header.write_text(PANDOC_HEADER)
            pdf = pack / f"{name}.pdf"
            subprocess.run(["pandoc", str(md), "-o", str(pdf), "--pdf-engine=pdflatex", "-V", "geometry:margin=2cm",
                            "-V", "fontsize=11pt", "-H", str(header)], check=True)
            txt = cli_text = md
        manifest.append({"label": doc["label"], "pdf": str(pdf), "pages": pages(pdf), "txt": str(txt),
                         "cli_text": str(cli_text)})
    (pack / "manifest.json").write_text(json.dumps(manifest, indent=2))
    lines = ["# Placeholders found in the review copies", ""]
    lines += [f"- {f['document']}: [{f['kind']}: {f['text']}]" for f in found] or ["none"]
    (pack / "placeholders_found.md").write_text("\n".join(lines) + "\n")
    for m in manifest:
        print(f"{m['label']}: {m['pdf']} ({m['pages']} pages)")
    print(f"{len(found)} placeholders converted; list in {pack / 'placeholders_found.md'}")


if __name__ == "__main__":
    main(*sys.argv[1:3])
