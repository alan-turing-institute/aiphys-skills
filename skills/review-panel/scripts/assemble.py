#!/usr/bin/env python3
"""Fill the prompt templates for one panel run.

    assemble.py <run_config.md> <out_dir>

Needs <out_dir>/pack/manifest.json from build_pack.py. Writes <out_dir>/prompts/<ID>.md for every roster entry,
brief_fidelity.md and moderator.md, and <out_dir>/plan.json listing who runs what, on which model, writing where.
Refuses if any template field is left unfilled, or if a command-line prompt is too long to pass as one argument.
"""

from __future__ import annotations

import json
import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import panel_config  # noqa: E402
from panel_config import Runner  # noqa: E402

PROMPTS = panel_config.SKILL_DIR / "prompts"
FIELD = re.compile(r"\{([A-Z][A-Z0-9_]+)\}")
MAX_ARG_BYTES = 120_000  # Linux caps one argv string at 131,072 bytes; agy takes the prompt as one argument


def template(name: str) -> str:
    text = (PROMPTS / f"{name}.md").read_text()
    return text.split("\n---\n", 1)[1].lstrip("\n")  # everything below the line is what the model receives


def fill(text: str, values: dict[str, str]) -> str:
    out = FIELD.sub(lambda m: values.get(m.group(1), m.group(0)), text)
    left = sorted({m for m in FIELD.findall(out) if m in KNOWN_FIELDS})
    if left:
        msg = f"unfilled fields: {', '.join(left)}"
        raise ValueError(msg)
    return out


KNOWN_FIELDS = {m for t in ("reviewer", "brief_fidelity", "moderator")
                for m in FIELD.findall((PROMPTS / f"{t}.md").read_text())}


def docs_for_agent(manifest: list[dict], with_text: bool = False) -> str:
    lines = ["Read each file completely with the Read tool. For PDFs use the `pages` parameter, so that you see "
             "tables, equations and charts as they are typeset."]
    lines += [f"{i}. {m['label']} ({m['pages']} pages): `{m['pdf']}`" for i, m in enumerate(manifest, 1)]
    if with_text:
        lines.append("Plain-text versions, for searching quotes: "
                     + "; ".join(f"{m['label']}: `{m['txt']}`" for m in manifest))
    return "\n".join(lines)


def docs_inline(manifest: list[dict]) -> str:
    parts = ["The documents are reproduced below as text. Equations are written in LaTeX notation, and charts are "
             "given as tables. Text in `[PENDING: ...]` or `[DRAFT VALUE: ...]` is unfinished (see above)."]
    for m in manifest:
        parts.append(f"===== {m['label']} =====\n\n{Path(m['cli_text']).read_text().strip()}\n\n"
                     f"===== end of {m['label']} =====")
    return "\n\n".join(parts)


def output_for_agent(path: Path, reply: str) -> str:
    return (f"Write your output to this file (create it; overwrite if it exists): `{path}`\n\nThen reply with "
            f"exactly one line and nothing else: `{reply}`. Do not return the output as your message (long "
            "messages are cut off), and do not use SendMessage.")


OUTPUT_FOR_CLI = ("Reply with the review and the ledger only, as plain Markdown, and nothing else. You have no tools "
                  "and need none.")


def main(config_path: str, out_dir: str) -> None:
    fields = panel_config.load(config_path)
    out = Path(out_dir).resolve()
    manifest = json.loads((out / "pack" / "manifest.json").read_text())
    found = (out / "pack" / "placeholders_found.md").read_text()
    pending = f"{fields.get('PENDING_ITEMS', 'none listed').strip()}\n\n{found.strip()}"
    (out / "prompts").mkdir(exist_ok=True)
    (out / "reviews").mkdir(exist_ok=True)
    common = {**fields, "PENDING_ITEMS": pending}
    plan, review_lines = [], []
    for r in panel_config.roster(fields):
        review = out / "reviews" / f"{r['id']}.md"
        values = {**common, "REVIEWER_ID": r["id"], "FIELD_NAME": r["field"], "FIELD_DESCRIPTION": r["background"]}
        if r["runner"] == Runner.AGENT:
            values["DOCUMENTS_BLOCK"] = docs_for_agent(manifest)
            values["OUTPUT_BLOCK"] = output_for_agent(review, "written, score <score>, <n> weaknesses")
        else:
            values["DOCUMENTS_BLOCK"] = docs_inline(manifest)
            values["OUTPUT_BLOCK"] = OUTPUT_FOR_CLI
        prompt = fill(template("reviewer"), values)
        if r["runner"] == Runner.CLI and len(prompt.encode()) > MAX_ARG_BYTES:
            msg = f"{r['id']}: prompt is {len(prompt.encode())} bytes, over {MAX_ARG_BYTES}"
            raise ValueError(msg)
        path = out / "prompts" / f"{r['id']}.md"
        path.write_text(prompt)
        model = r.get("model") or f"agent {r['agent']}"
        plan.append({"id": r["id"], "runner": r["runner"].value, "agent": r.get("agent"), "model": r.get("model"),
                     "effort": r["effort"], "prompt": str(path), "output": str(review)})
        review_lines.append(f"- {r['id']} ({r['field']}; {model}, effort {r['effort']}): `{review}`")
    brief = out / "brief_fidelity.md"
    bf = fill(template("brief_fidelity"), {**common, "DOCUMENTS_BLOCK": docs_for_agent(manifest),
                                            "OUTPUT_PATH": str(brief)})
    (out / "prompts" / "brief_fidelity.md").write_text(bf)
    report = out / "panel_report.md"
    mod = fill(template("moderator"), {**common, "DOCUMENTS_BLOCK": docs_for_agent(manifest, with_text=True),
                                       "REVIEW_FILES": "\n" + "\n".join(review_lines), "BRIEF_FIDELITY_FILE": str(brief),
                                       "OUTPUT_PATH": str(report)})
    (out / "prompts" / "moderator.md").write_text(mod)
    for step, output in (("brief_fidelity", brief), ("moderator", report)):
        agent = (fields.get(f"{step.upper()}_AGENT", "").strip().splitlines() or ["general-purpose"])[0].strip()
        plan.append({"id": step, "runner": Runner.AGENT.value, "agent": agent,
                     "prompt": str(out / "prompts" / f"{step}.md"), "output": str(output)})
    (out / "plan.json").write_text(json.dumps(plan, indent=2))
    for p in plan:
        size = len(Path(p["prompt"]).read_text().encode())
        print(f"{p['id']}: {p['runner']} {p.get('agent') or p.get('model')}  prompt {size:,} bytes -> {p['output']}")


if __name__ == "__main__":
    main(*sys.argv[1:3])
