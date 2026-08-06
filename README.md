# AI for Physical Systems Skills

Reusable Agent Skills for research and engineering workflows in AI for
physical systems.

## Available skills

### `summarize-paper`

Create source-audited, mathematics-aware summaries and detailed article notes
for research papers and technical reports.

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
