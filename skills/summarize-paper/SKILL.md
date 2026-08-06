---
name: summarize-paper
description: Create source-audited, technically dense Markdown summaries and layered article notes for research papers, arXiv PDFs, articles, and technical reports. Use when summarizing a paper with mathematical detail, citations, notation and claim checks, tensor shapes, model or data-flow discussion, figures, results, potential applications, implementation notes, or rendered PDF output; supports both strict concise summaries and whole-paper detailed notes with appendices.
---

# Summarize Paper

## Overview

Produce source-faithful Markdown that is useful to someone reusing,
implementing, or critiquing the paper. Preserve the central claim, enough
mathematics to reconstruct the method, the evidence supporting the results, and
implementation implications when relevant.

## Choose The Output Mode

- **Compact summary:** target 1-2 generated PDF pages and keep the main prose
  under 1000 words.
- **Detailed article note:** keep the main narrative compact, then use
  appendices for derivations, baselines, architecture, implementation detail,
  and evaluation caveats. Read
  [references/detailed-mode-guide.md](references/detailed-mode-guide.md)
  before drafting this mode.

Follow an explicit user length limit over these defaults. When revising an
existing focused note, preserve its scope unless the user asks to expand it;
create a separate detailed note when both forms are useful.

## Workflow

1. Read local project instructions first, especially `AGENTS.md`, README files,
   note templates, and hook commands.
2. Select the output mode and inspect strong local examples before fixing the
   outline.
3. Inspect the full paper, including appendices and supplementary material, not
   only the abstract. Use PDF/arXiv tools, page images, source files, figure
   extraction, or a dedicated PDF skill when available. Identify the paper's
   principal method or architecture figure, when one exists, and record its
   figure number, page, and source version.
4. Inspect official code, configuration, or documentation when making
   implementation or reproducibility claims. Record the version or commit when
   it matters, and report paper/code discrepancies rather than silently choosing
   one.
5. Draft a short plan: audience, length, central contribution, equations,
   evidence, figures, applications, and implementation angles.
6. Write the summary in Markdown, following the destination repository's math,
   link, image, citation, and index conventions.
7. Run a separate fidelity pass over claims, notation, units, tensor axes,
   normalization, sources of randomness, and paper-versus-code facts.
8. Validate with repository formatting hooks and preview/build commands. When
   delivering a PDF, generate it and visually inspect every rendered page for
   clipped equations, broken links, overflow, whitespace, and awkward breaks.

## Summary Shape

Prefer this structure unless the project has a stronger local convention:

- Title with paper name and citation/link.
- One-paragraph thesis: what problem the paper solves and the main idea.
- Setup and notation: variables, assumptions, data shapes, model components.
- Method: key objective, equations, algorithm, architecture, or derivation.
- Results and evidence: metric, dataset, baseline or ablation, comparison, and
  caveat.
- The paper's principal method or architecture figure when it materially
  clarifies the method and reuse is permitted; otherwise an original schematic,
  diagram, or compact table when that communicates more clearly than prose.
- Potential applications: where the method could contribute to forecasting,
  emulation, uncertainty quantification, simulation, inference, or decisions.
- Implementation notes: data flow, tensor layout, APIs, numerical concerns,
  likely failure modes, or pseudocode when useful.
- Limitations and open questions.

Do not make the summary a generic abstract rewrite.

## Length Discipline

- In compact mode, target 1-2 generated PDF pages.
- In detailed mode, keep the main narrative under 1000 words when practical and
  move supporting mathematics and evidence into appendices in the same article.
- Let the detailed PDF use the pages required for legible equations, tables, and
  references; do not compress it merely to satisfy the compact-mode page target.
- Prefer equations, compact notation lists, and diagrams over long prose.

## Mathematics

- Include enough math for the summary to be operational:
  - problem variables and assumptions,
  - objective functions, losses, update rules, or probabilistic factorisations,
  - tensor shapes and normalization axes,
  - important approximations, invariances, or conservation constraints,
  - computational complexity or stability concerns when central.
- Define symbols near first use. Use notation tables or bullets for dense
  symbol sets.
- Prefer the paper's notation. If explanatory notation is clearer, define it as
  an explicit translation rather than presenting it as the paper's notation.
- Keep distinct objects distinct, especially physical and artificial time,
  random seed and evolving state, model instance and sampling seed, marginal
  and joint distributions, and training and inference variables.
- When discussing implementation, connect equations to code-level objects:
  tensors, modules, functions, batches, channels, grids, time steps, solvers, or
  sampling loops.

## Figures And Diagrams

- Use a visual only when it earns its space. It is valid to omit one when
  equations or tables explain the method more precisely.
- Prefer the paper's principal method or architecture figure when it exists,
  materially clarifies the method, and its licence or usage context permits
  reuse. Identify it by figure number and paper version, preserve necessary
  caption context, and attribute it directly.
- Otherwise create an original schematic, Mermaid diagram, generated bitmap, or
  small plotted diagram that captures architecture, data flow, algorithm stages,
  or mathematical structure.
- Embed diagrams directly in Markdown using local relative paths. Avoid
  hotlinked remote images for core figures.
- Add concise explanatory text around each figure so it earns its space.

## Evidence And Citation

- Cite the paper version and any secondary sources used. Prefer official code or
  configuration for implementation facts.
- Distinguish paper claims, mathematical consequences, code facts,
  interpretation, and speculation.
- Check central interpretive claims directly against equations, assumptions,
  appendices, and code. Preserve useful intuition while qualifying what does not
  follow mathematically.
- For results, state what metric, dataset, baseline, or ablation supports the
  claim. Avoid vague "performs better" language without context.

## Potential Applications

Discuss applications only when they clarify why the paper matters. Start from
the stated use case, then consider whether the core capability could fill one or
more of these roles:

- **Forecasting and learned dynamics:** predict fields, trajectories, events,
  distributions, or diagnostics in ambient or latent spaces using learned
  time-stepping, sequence models, or operator learning, with probabilistic
  approaches such as ensembles, diffusion, flow matching, or neural processes
  when relevant.
- **Simulation and emulation:** generate datasets across parameters,
  initial or boundary conditions, forcing, regimes, resolutions, or fidelity;
  replace expensive simulators with scalar, multi-output, field, or trajectory
  surrogates for sensitivity analysis, simulator calibration, history matching,
  or digital twins.
- **Uncertainty quantification:** produce or post-process point, interval,
  quantile, ensemble, distributional, or generative predictions; distinguish
  aleatoric and epistemic uncertainty when supported and identifiable; assess
  proper scores, reliability, sharpness, coverage, tails, and joint spatial or
  temporal coherence.
- **Inference and decisions:** support state or parameter estimation, inverse
  problems, data assimilation, active learning, experimental design, anomaly
  detection, optimisation, control, or risk-aware decisions.

For physical systems, identify which inductive biases or structural assumptions
the method or application introduces, preserves, or violates, such as
conservation laws, boundary conditions, symmetries, locality, causality, or
multiscale structure; also check stability and behaviour across resolution
changes. State what transfers from the paper, what must be adapted, what data,
simulator, or observations are required, and what metric or failure test would
validate the application. Label speculation as interpretation, not a paper
claim.

## Implementation Notes

Include implementation details when relevant, but keep them scoped:

- data preprocessing and normalization,
- tensor layout and shape transformations,
- model components and where they plug into existing code,
- training objective and optimizer-facing losses,
- sampling or inference procedure,
- numerical pitfalls,
- minimal pseudocode or API sketches.

If implementation questions are substantial, plan them separately from the
summary so the summary stays concise.
