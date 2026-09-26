# Sampling More Strategically But Just as Flexibly as IID

Source for Fred J. Hickernell's Illinois Tech School of Computing colloquium on November 9, 2026, at 1:50 PM America/Chicago. This repository contains the Quarto Reveal.js deck, a companion notebook, reproducible examples, and a small website. The talk builds on, but is separate from, the MCQMC 2026 talks and manuscripts.

[Colloquium website and slides](https://fjhickernell.github.io/StrategicSamplingColloquium/)

## Build

Clone with submodules, then render the website and slides:

```bash
git clone --recurse-submodules git@github.com:fjhickernell/StrategicSamplingColloquium.git
cd StrategicSamplingColloquium
quarto render
quarto render slides
# Open notebooks/StrategicSampling.ipynb in the qmcpy Jupyter kernel
```

The site publishes the rendered slides under `slides/` through `.github/workflows/publish.yml`.

## Companion notebook

[StrategicSampling.ipynb](notebooks/StrategicSampling.ipynb) builds the introductory
coverage and integration-error figures and a fresh synthetic-beam comparison.
The optional [Pydantic AI beam tool loop](examples/beam/README.md) uses a
scripted policy by default and needs `pydantic-ai-slim`; the notebook itself
uses the standard `qmcpy` environment.

## Sources

- The title and abstract in `index.qmd` are the author's approved colloquium text.
- Figure origins and generation steps are recorded in [`assets/figures/README.md`](assets/figures/README.md).
- The deck uses the pinned HickernellAcademicLib `classlib` submodule for shared presentation styling.
- The introductory narrative adapts public MATH 565 slides; the lattice and Kronecker research narrative and one figure are sourced from the public MCQMC 2026 decks.
- The synthetic beam code adapts the author’s Simon Grant prototype. Proposal text and saved grant results are not included.
