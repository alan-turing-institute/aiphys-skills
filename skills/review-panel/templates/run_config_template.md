# Review-panel run config: <application name>

Copy into the application's own folder (e.g. `<bid>/review/run_config.md`) and fill every section. A section whose
whole value is `file: <absolute path>` is replaced by that file. Sections left out come from the profile.

## PROFILE

<profile name in the skill's profiles/ folder, e.g. ukri_dpr>

## FUNDER_CALL

<funder and call or scheme, one line>

## FUNDER_TEXT

file: <absolute path to the funder's criteria and reviewer rules, copied word for word>

## AREAS

<numbered list: each assessment area with the exact question reviewers use as its subheading>

## SECTION_MAP

<bullets: where in the application each area is answered; which parts are read but not scored>

## FIT_CHECKS

<what the call says it will and will not support, phrased as questions>

## PENDING_ITEMS

file: <absolute path to a table of unfinished items and who completes each; or write "none">

## DOCUMENTS

- <label> | pdf | <absolute path> | text: <optional cleaner text version for command-line reviewers>
- <label> | markdown | <absolute path> | start: <optional heading where the reviewed text begins>

## COMPLIANCE

- pdf | <absolute path> | max_pages: <n> | text_pages: <a-b> | font_pt: <size> | margin_cm: <cm> | max_mb: <MB>
- markdown | <absolute path> | limits: <Section name>=<words>; <Section name>=<words>

## ROSTER

| ID | Runs on | Effort | Field | Background given to the reviewer |
|---|---|---|---|---|
| R1 | Claude, agent `general-purpose` | high | <field> | <two sentences: what this reviewer works on, what they know and do not know> |
| R2 | Gemini 3.8 Flash (High), through `agy` | High (set by the model name) | <field> | <...> |

## BRIEF_FIDELITY_AGENT

<agent type on your strongest model, e.g. general-purpose>

## MODERATOR_AGENT

<agent type on your strongest model, e.g. general-purpose>

## RULINGS_FILE

<absolute path to the author's brief and rulings, recorded close to verbatim>

## THESIS

<the author's organising thesis, quoted from the rulings file, with where it is recorded>

## RULINGS_CHECKLIST

<numbered rulings to check, each with where it is recorded>

## SECTION_LIST

<the sections of the application, in order>
