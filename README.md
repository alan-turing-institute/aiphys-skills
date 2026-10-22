# AI for Physical Systems Skills

Reusable Agent Skills for research and engineering workflows in AI for
physical systems.

## Available skills

### `summarize-paper`

Create source-audited, mathematics-aware summaries and detailed article notes
for research papers and technical reports.

### `review-panel`

Run a simulated review panel on your own draft funding application before
submission: a check of the funder's format limits, independent reviewers on
more than one model family who review section by section, a check of the draft
against the authors' own brief, and a moderator that verifies every quoted
criticism before it reaches the authors. Funders are described by profile
files; a UKRI distributed peer review profile is included. For your own drafts
only: funders forbid putting other applicants' work into AI tools.

Requires Claude Code, Python 3.11 or later and Poppler (`pdfinfo`,
`pdftotext`); some steps also use MuPDF's `mutool` and `pandoc` with
`pdflatex`. Reviewers on a second model family need Google's Antigravity CLI
(`agy`). The same skill is published in
[farhanferoz/claude-skills](https://github.com/farhanferoz/claude-skills), and
the two copies are kept identical.

## Installation

Install skills interactively with the `skills` CLI:

```bash
npx skills@latest add alan-turing-institute/aiphys-skills
```

For example, install `summarize-paper` globally for Codex and Claude Code
without prompts:

```bash
npx skills@latest add alan-turing-institute/aiphys-skills \
  --skill summarize-paper \
  --global \
  --agent codex \
  --agent claude-code \
  --yes
```
