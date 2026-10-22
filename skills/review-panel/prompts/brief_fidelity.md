# Brief-fidelity prompt (template)

For ONE agent that, unlike the panel, sees the author's own brief and rulings. It answers two questions no panel
reviewer is asked: does the draft do what its author asked for, and does it agree with itself? Run on the strongest
model available (measured lesson: a review against the funder's criteria alone passed a draft whose framing the author
then rejected, because nobody checked it against the author's brief).

| Field | Comes from | What it holds |
|---|---|---|
| `{FUNDER_CALL}` | profile | The funder and call |
| `{DOCUMENTS_BLOCK}` | assembly script | The same review copies the panel reads |
| `{RULINGS_FILE}` | run config | Absolute path to the author's brief and rulings, recorded close to verbatim |
| `{THESIS}` | run config | The author's organising thesis, quoted from the rulings file, with where it is recorded |
| `{RULINGS_CHECKLIST}` | run config | The rulings to check, each with where it is recorded in the rulings file |
| `{SECTION_LIST}` | run config | The sections of the application, in order |
| `{PENDING_ITEMS}` | run config | The unfinished items, as given to the panel |
| `{FUNDER_TEXT}` | profile | The funder's criteria, word for word (used only to spot tension with a ruling) |
| `{OUTPUT_PATH}` | assembly script | Where to write the findings |

Everything below the line is sent to the agent.

---

You are checking a draft funding application for {FUNDER_CALL} against its author's own brief. A separate panel is
reviewing the same draft against the funder's criteria; that is not your job. Your job has three parts: whether the
author's thesis organises the draft, whether each of the author's rulings is obeyed, and whether the draft agrees with
itself.

## What you have

- The draft: {DOCUMENTS_BLOCK}
- The author's brief and rulings, recorded close to verbatim, newest at the bottom: `{RULINGS_FILE}`. Where two
  rulings conflict, the later one stands. Read the whole file, not only the parts the checklist points to.
- The funder's criteria, word for word, at the end of this prompt.

Do not use any other source.

## Unfinished items

These are being completed by other people and are not findings. They appear in the text as `[PENDING: ...]` or
`[DRAFT VALUE: ...]`:

{PENDING_ITEMS}

## Part A. Does the author's thesis organise the draft?

The author's thesis:

{THESIS}

For each section below, decide whether the thesis ORGANISES it (the section's argument is built on it), is only
MENTIONED (it appears but does not shape the argument), or is ABSENT. Quote the draft each time. A thesis that is
stated once and then left behind is a failure, even if every sentence is correct.

{SECTION_LIST}

## Part B. Is each ruling obeyed?

For each ruling in the checklist:

1. Find it in the rulings file and quote the author's exact words, with where they are recorded.
2. Search the whole draft for text the ruling governs. Quote the passage that obeys it or breaks it, with where it is.
3. Mark it HOLDS, BREAKS, or TENSION (the ruling and the funder's criteria pull against each other: quote both and say
   how).

The checklist is a starting point, not the rule. Read the rulings file yourself, and add any ruling the checklist
missed, marked "added".

{RULINGS_CHECKLIST}

## Part C. Does the draft agree with itself?

List every place where two parts of the draft disagree: numbers, names, dates or months, who leads what, outputs,
references and their numbering, and terms (one name for one thing, used the same way everywhere). Quote both sides,
with where they are. Do not list pending items.

## Output

Write your findings to this file (create it; overwrite if it exists): `{OUTPUT_PATH}`

Use this structure:

```
# Brief fidelity

## A. Thesis
| Section | Organises / Mentioned / Absent | Quote and where |

## B. Rulings
### BREAKS
R<n>. <ruling, in the author's words, and where recorded>
- Draft: "<quote>" (<where>)
- Why it breaks: <one or two sentences>
- Smallest fix that obeys the ruling: <one sentence>

### TENSIONS
(same fields, with the funder's text quoted as well)

### HOLDS
R<n>. <ruling> | "<draft quote>" (<where>)

## C. Inconsistencies
I<n>. "<quote 1>" (<where>) vs "<quote 2>" (<where>): <what disagrees>

(Write "none" under any heading with no entries.)
```

Then reply with exactly one line and nothing else: `written, <B> breaks, <T> tensions, <I> inconsistencies`. Do not
return the findings as your message (long messages are cut off), and do not use SendMessage.

## The funder's criteria (word for word)

{FUNDER_TEXT}
