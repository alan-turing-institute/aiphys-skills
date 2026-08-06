# Detailed Mode Guide

Use this pattern for a whole-paper, maths-forward note. Adapt the headings to the
paper and repository rather than reproducing them mechanically.

## Document Architecture

1. **Title and sources:** identify the paper version and link the paper, PDF,
   official code, and other primary artifacts used.
2. **Summary:** explain the problem, central mechanism, two to four
   main components, and headline evidence without requiring the appendices.
3. **Minimal mathematical setup:** define the target object, conditioning
   variables, assumptions, shapes, time coordinates, and a compact symbol
   ledger.
4. **Named method components:** give each component its purpose, defining
   equations, operational steps, and main trade-off.
5. **Model and experimental setup:** record architecture, data, preprocessing,
   training, inference, parameter count, resolution, splits, and ensemble or
   sampling construction when relevant.
6. **Results and their justification:** organize claims around the paper's
   experiments. State the metric, dataset, baseline or ablation, comparison, and
   caveat. Use compact tables for exact values when they sharpen the argument.
7. **Interpretation and limitations:** separate what the paper establishes from
   plausible mechanisms, implementation implications, and unresolved questions.
8. **Takeaway:** end the main note with a compact decomposition of the method and
   why it matters.
9. **Appendices:** move derivations, proofs, baseline mathematics, architecture
   details, tensor flow, numerical issues, and evaluation caveats here.

## Claim And Source Audit

For every central claim, determine whether it is:

- stated or empirically supported by the paper,
- a direct mathematical consequence of the formulation,
- established by official code or configuration,
- an interpretation supported by evidence, or
- speculation that must be labelled as such.

Read appendices and supplementary material before concluding that a detail is
missing. Inspect official code when describing released architecture, tensor
layout, training, inference, or configuration. If the paper and code disagree,
state both and identify which one the note uses.

## Notation And Accuracy Audit

After drafting, make a separate pass that:

- matches symbols to the paper or explicitly declares translations,
- distinguishes physical time, model time, and solver or diffusion time,
- distinguishes a trained model, initialization seed, sampling seed, latent
  process, and evolving state,
- verifies units, normalization, tensor axes, conditioning, and averaging,
- checks that marginal claims are not silently promoted to joint claims,
- tests verbal interpretations against the equations, including edge cases and
  limiting behaviour, and
- replaces ambiguous shorthand with operational wording.

## Appendix Selection

Add an appendix only when it supports the main note. Useful appendices include:

- a derivation needed to justify an interpretation,
- what an objective constrains and what it leaves unidentified,
- architecture and data-flow details with tensor shapes,
- mathematical descriptions of important baselines,
- training, scaling, parallelism, or inference procedures, and
- evaluation design, uncertainty decomposition, or reproducibility caveats.

Keep implementation plans separate when they would turn the article into a
repository design document.

## Final Review

- Confirm that the summary and main sections cover the whole paper,
  not only its most mathematically interesting component.
- Remove duplication between the main note and appendices.
- Run repository hooks and the normal site or document build.
- When delivering a PDF, render every page and inspect equations, tables,
  margins, references, link wrapping, whitespace, and page breaks.
