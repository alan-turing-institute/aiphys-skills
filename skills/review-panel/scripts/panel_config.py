"""Read a review-panel run config and its funder profile.

Both are Markdown files made of `## FIELD` sections. A section whose whole value is `file: <absolute path>` is replaced
by that file's contents. Fields in the run config override fields of the same name in the profile named by `PROFILE`.
"""

from __future__ import annotations

import re
from enum import StrEnum
from pathlib import Path

SKILL_DIR = Path(__file__).resolve().parent.parent
DOC_REQUIRED_PARTS = 3  # label | kind | path
ROSTER_COLUMNS = 5  # ID | Runs on | Effort | Field | Background
CLI_MARKER = ", through"  # "Runs on" for a command-line model: "<model>, through agy"


class DocKind(StrEnum):
    PDF = "pdf"
    MARKDOWN = "markdown"


class Runner(StrEnum):
    AGENT = "agent"  # a Claude Code agent, launched by the session with the Agent tool
    CLI = "cli"  # a model run by run_external.py through the Antigravity command-line tool


def read_sections(path: Path) -> dict[str, str]:
    sections: dict[str, str] = {}
    name = None
    lines: list[str] = []
    for line in path.read_text().splitlines():
        m = re.fullmatch(r"## ([A-Z][A-Z0-9_]*)\s*", line)
        if m:
            if name:
                sections[name] = "\n".join(lines).strip()
            name, lines = m.group(1), []
        elif name:
            lines.append(line)
    if name:
        sections[name] = "\n".join(lines).strip()
    for key, value in sections.items():
        m = re.fullmatch(r"file:\s*(\S+)", value)
        if m:
            sections[key] = Path(m.group(1)).read_text().strip()
    return sections


def load(config_path: str | Path) -> dict[str, str]:
    config_path = Path(config_path)
    run = read_sections(config_path)
    profile_name = run.get("PROFILE", "").strip()
    fields: dict[str, str] = {}
    if profile_name:
        profile = SKILL_DIR / "profiles" / f"{profile_name}.md"
        if not profile.exists():
            msg = f"profile not found: {profile}"
            raise FileNotFoundError(msg)
        fields.update(read_sections(profile))
    fields.update(run)
    fields["_CONFIG_PATH"] = str(config_path)
    return fields


def documents(fields: dict[str, str]) -> list[dict[str, str]]:
    """DOCUMENTS lines: `- <label> | <pdf|markdown> | <path> | key: value | ...`."""
    docs = []
    for line in fields.get("DOCUMENTS", "").splitlines():
        line = line.strip()
        if not line.startswith("- "):
            continue
        parts = [p.strip() for p in line[2:].split(" | ")]
        if len(parts) < DOC_REQUIRED_PARTS:
            msg = f"DOCUMENTS line needs '<label> | <kind> | <path>': {line}"
            raise ValueError(msg)
        doc = {"label": parts[0], "kind": DocKind(parts[1]), "path": parts[2]}
        for opt in parts[3:]:
            key, _, value = opt.partition(":")
            doc[key.strip()] = value.strip()
        docs.append(doc)
    return docs


def roster(fields: dict[str, str]) -> list[dict[str, str]]:
    """ROSTER table: | ID | Runs on | Effort | Field | Background given to the reviewer |."""
    rows = []
    for line in fields.get("ROSTER", "").splitlines():
        cells = [c.strip() for c in line.strip().strip("|").split("|")]
        if len(cells) != ROSTER_COLUMNS or cells[0] in ("ID", "") or set(cells[0]) <= set("-: "):
            continue
        rid, runs_on, effort, field, background = cells
        entry = {"id": rid, "runs_on": runs_on, "effort": effort, "field": field, "background": background}
        if CLI_MARKER in runs_on:
            entry["runner"] = Runner.CLI
            entry["model"] = runs_on.split(CLI_MARKER)[0].strip()
        else:
            m = re.search(r"`([a-z0-9-]+)`", runs_on)
            if not m:
                msg = f"roster entry {rid}: name the agent type in backticks, e.g. `general-purpose`"
                raise ValueError(msg)
            entry["runner"] = Runner.AGENT
            entry["agent"] = m.group(1)
        rows.append(entry)
    return rows
