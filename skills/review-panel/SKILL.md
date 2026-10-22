---
name: review-panel
description: >-
  Run a simulated review panel on the team's OWN draft funding application (or another document a funder or journal
  will review) before submission: several independent reviewer agents on more than one model, a check against the
  author's own brief, and a moderator that verifies every criticism. Use when asked for an independent review, a mock
  or simulated review, a review panel, a committee review, a peer-review simulation, or "how would reviewers score
  this" for a grant application or proposal. Configurable per funder (number and fields of reviewers, models, score
  scale, rules). Never for reviewing other people's applications.
allowed-tools:
  - Read
  - Write
  - Edit
  - Bash
  - Agent
  - TodoWrite
---

# Review panel

A pre-submission review of our own draft, built to imitate how the funder's reviewers will read it and to report only
criticisms that survive a check against the text.

## Essential principles

1. **Our own drafts only.** Funders forbid putting other applicants' work into AI tools (UKRI's reviewer rules say no
   part of an application may be entered into one). Refuse to run this on anything we are reviewing for a funder.
2. **The author reviews first.** Run the panel only after the author has read and commented on the draft. It is a
   defect finder for a draft the author already stands behind, not a substitute for the author's judgement.
3. **Every criticism quotes the text, and the moderator checks it.** Reviewing models misquote and claim things are
   missing when they are not. Nothing reaches the author unverified.
4. **Ordinary reviewers, section by section, no debate.** No critical or lenient personas (they bias scores), no
   rebuttal round (performance fell after one), and reviews go area by area (this beat a persona council on real
   EPSRC proposals). At most two panel rounds per draft.
5. **Scores are indicative.** Agreement between simulated and human reviewers is weak in every published study. The
   value is the verified fix list.

## When to use

- A draft application is ready and the author has reviewed it.
- After substantial revisions, as a second and final round.
- To check a draft against the author's own rulings (the brief-fidelity step can run on its own).

## When not to use

- Reviewing another team's application: forbidden; refuse.
- A clarity read of a technical note: use the `research-report` skill's cold reader.
- Code review: use `code-review` or `tiered-review`.
- Checking facts, quotes or citations: use `deep-research-tiered` or a targeted fetch; the panel only reads the draft.

## Inputs

| Input | Where | What |
|---|---|---|
| Funder profile | `profiles/<name>.md` in this skill | Reviewer role, writing rules, score scale and severity grades, moderation rules, panel defaults. `ukri_dpr` covers UKRI calls using distributed peer review. Write a new profile for another funder. |
| Run config | the application's own folder, e.g. `<bid>/review/run_config.md` | `## FIELD` sections: PROFILE, FUNDER_CALL, FUNDER_TEXT, AREAS, SECTION_MAP, FIT_CHECKS, PENDING_ITEMS, DOCUMENTS, COMPLIANCE, ROSTER, BRIEF_FIDELITY_AGENT, MODERATOR_AGENT, RULINGS_FILE, THESIS, RULINGS_CHECKLIST, SECTION_LIST. Start from `templates/run_config_template.md`. |
| Pending items | marked `{...}` in the draft, plus an optional table of who completes what | Converted to `[PENDING: ...]` or `[DRAFT VALUE: ...]`; never counted as weaknesses. |

The roster sets how many reviewers there are, each one's field and background, and where each runs: a Claude Code
agent type in backticks (any type your setup defines; `general-purpose` is built in) or a model run through Google's
Antigravity command-line tool (for example `Gemini 3.8 Flash (High), through agy`). Use at least two model families
where you can: a Claude-only panel still runs, but its blind spots are all shared.

## Requirements

- Python 3.11 or later, and Claude Code (agent reviewers, the brief-fidelity check and the moderator run as agents).
- Poppler's `pdfinfo` and `pdftotext`, for review copies and compliance checks.
- MuPDF's `mutool`, only for the compliance check's font-size test.
- `pandoc` with `pdflatex` and the TeX Gyre fonts, only for documents listed as Markdown.
- Optional: Antigravity's `agy` command, for reviewers on a second model family. If an `agy-run` wrapper is on the
  `PATH` it is used instead (same arguments, with explicit exit codes when a tool is denied).

All paths in a run config are absolute paths on your own machine; nothing in the skill assumes a particular user or
folder layout.

## Phases

Scripts are in this skill's `scripts/` folder. `<cfg>` is the run config, `<out>` the run's output folder.

### Phase 1. Compliance

- Entry: the draft builds; the run config exists.
- Action: `python3 scripts/compliance_check.py <cfg>` (add `--final` before submission).
- Exit: no failures, or each failure reported to the author and fixed or accepted by them.

### Phase 2. Review copies

- Entry: Phase 1 passed. Any `text:` versions are rebuilt from the current draft.
- Action: `python3 scripts/build_pack.py <cfg> <out>`.
- Exit: `<out>/pack/manifest.json` exists, and `placeholders_found.md` lists every placeholder. Read the list against
  the pending-items table: an item in one and not the other is a gap to fix before going on.

### Phase 3. Prompts

- Entry: Phase 2 done.
- Action: `python3 scripts/assemble.py <cfg> <out>`.
- Exit: one prompt per reviewer plus `brief_fidelity.md` and `moderator.md` in `<out>/prompts/`, and `<out>/plan.json`.
  Open one reviewer prompt and check that the documents, pending items and funder text are filled in.

### Phase 4. Panel

- Entry: Phase 3 done; the author has agreed the roster and its cost.
- Actions, in parallel:
  1. Command-line reviewers: `python3 scripts/run_external.py <out>` in the background.
  2. Each agent reviewer: launch the agent type from `plan.json` with a short brief that points it at its prompt file
     ("Your complete instructions are in <prompt>; read it in full, then follow it exactly"). Keep within the
     session's limit on agents running at once.
- Exit: every review file in `<out>/reviews/` has a `## Score` and a `# Ledger`. A failed or empty review is rerun once;
  if it fails again, the moderator is told it is missing.

### Phase 5. Brief fidelity

- Entry: the author's rulings file exists. It can run alongside Phase 4.
- Action: launch the brief-fidelity agent from `plan.json` the same way.
- Exit: `<out>/brief_fidelity.md` exists.

### Phase 6. Moderation

- Entry: Phases 4 and 5 finished.
- Action: launch the moderator agent from `plan.json`.
- Exit: `<out>/panel_report.md` exists, with every section filled or marked "none".

### Phase 7. Report to the author

1. Read the panel report in full yourself before summarising it.
2. Tell the author the top fixes in plain words, the score spread, and the path of the report.
3. Fixes are made only with the author's agreement. A second round, if any, is the last.

## Success criteria

- [ ] Compliance checked; review copies hold no internal notes; every placeholder converted and listed.
- [ ] Every reviewer worked from the same review copies and saw nothing else.
- [ ] Every issue in the report quotes the draft and was verified by the moderator; dropped criticisms are listed.
- [ ] Every proposed fix was checked against the author's rulings.
- [ ] No outcome or ranking predicted from the panel's scores.

## Reference index

- `prompts/reviewer.md`, `prompts/brief_fidelity.md`, `prompts/moderator.md`: the templates, each with a table of its
  fields.
- `profiles/ukri_dpr.md`: the UKRI distributed peer review profile.
- `templates/run_config_template.md`: a blank run config to copy for a new application.
- `references/evidence_and_prior_work.md`: the studies and the existing tools this design rests on.

## Keeping the copies in step

This skill is published in two places, kept identical: the `review-panel` plugin of
`github.com/farhanferoz/claude-skills` and `skills/review-panel` in `github.com/alan-turing-institute/aiphys-skills`.
A change goes to both in the same sitting; compare the two folders (`diff -r`) before committing either.
