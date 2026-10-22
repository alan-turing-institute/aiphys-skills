# Evidence and prior work behind the review panel

Recorded 2026-10-06.

- Section-by-section review beat both a single pass and a "council of personas" on six real EPSRC proposals (Thorne et
  al. 2026, arXiv:2603.08281), though all missed most planted flaws and most clarity problems.
- Extreme personas are biased; agreement with human reviewers is weak; performance fell after rebuttal rounds
  (ReviewerToo, arXiv:2510.08867).
- Splitting a document across agents cut generic comments from 60% to 29% (MARG, arXiv:2401.04259); an ensemble of
  reviews plus a meta-review step (The AI Scientist, arXiv:2408.06292); checking that weaknesses are valid and specific
  before ranking them (DIAGPaper, arXiv:2601.07611).
- Checks borrowed from the `review-grant` skill in github.com/claesbackman/AI-research-feedback (MIT licence): every
  output traced to a work package, overclaiming and underclaiming, unsecured dependencies, agents shown only their
  listed files.
- Mechanics from our own `research-report` cold reader: read the rendered PDF, write findings to a file, reply in one
  line.


## What is not known

- How many real flaws this panel finds in our drafts: not measured. A calibration run (known flaws planted in a
  copy of a draft) would measure it.
- Whether two model families find different problems: the moderator's "raised by one model only" section
  records it per run.
