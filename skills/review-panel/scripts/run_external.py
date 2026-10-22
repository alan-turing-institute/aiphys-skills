#!/usr/bin/env python3
"""Run the panel's command-line reviewers (runner "cli" in plan.json) in parallel through Antigravity's `agy`.

    run_external.py <out_dir> [--timeout-min 40]

Each reviewer runs in its own empty working directory, so it sees no project files, instructions or memory. If an
`agy-run` wrapper is on the PATH it is used instead of plain `agy --print`: the review is then its printed reply, minus
its report of what it did, which goes to reviews/<ID>.agy_log.txt, and it exits 77 when a tool permission was denied
and 78 on unproven silence. Any non-zero exit, or a review without a score and a ledger, is reported and the review is
kept for inspection, never treated as a success.
"""

from __future__ import annotations

import json
import shutil
import subprocess
import sys
from pathlib import Path

TRAILER = "--- what agy actually did"


def command(prompt: str, model: str) -> list[str]:
    if shutil.which("agy-run"):
        return ["agy-run", prompt, "--model", model]
    return ["agy", "--print", prompt, "--model", model]


def main(out_dir: str, timeout_min: float = 40) -> int:
    out = Path(out_dir).resolve()
    plan = [p for p in json.loads((out / "plan.json").read_text()) if p["runner"] == "cli"]
    procs = []
    for p in plan:
        work = out / "cli_work" / p["id"]
        work.mkdir(parents=True, exist_ok=True)
        prompt = Path(p["prompt"]).read_text()
        raw = (out / "reviews" / f"{p['id']}.raw.txt").open("w")
        cmd = command(prompt, p["model"])
        procs.append((p, raw, subprocess.Popen(cmd, cwd=work, stdout=raw, stderr=subprocess.STDOUT)))
        print(f"started {p['id']} on {p['model']}")
    failed = 0
    for p, raw, proc in procs:
        try:
            code = proc.wait(timeout=timeout_min * 60)
        except subprocess.TimeoutExpired:
            proc.kill()
            code = "timeout"
        raw.close()
        text = Path(raw.name).read_text()
        review, _, log = text.partition(TRAILER)
        Path(p["output"]).write_text(review.strip() + "\n")
        if log:
            (out / "reviews" / f"{p['id']}.agy_log.txt").write_text(TRAILER + log)
        ok = code == 0 and "## Score" in review and "# Ledger" in review
        failed += not ok
        print(f"{p['id']}: exit {code}, {len(review.split())} words, {'ok' if ok else 'CHECK: missing score or ledger'}")
    return 1 if failed else 0


if __name__ == "__main__":
    args = sys.argv[1:]
    timeout = float(args[args.index("--timeout-min") + 1]) if "--timeout-min" in args else 40
    sys.exit(main(args[0], timeout))
