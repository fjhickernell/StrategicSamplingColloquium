# Sampling More Strategically But Just as Flexibly as IID

Source for Fred J. Hickernell's Applied Mathematics and Statistics Seminar at Illinois Tech on November 16, 2026, at 1:50 PM America/Chicago. This repository contains the Quarto Reveal.js deck, a companion notebook, reproducible examples, and a small website. The talk builds on, but is separate from, the MCQMC 2026 talks and manuscripts.

[Seminar website and slides](https://fjhickernell.github.io/StrategicSamplingColloquium/)

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
coverage figures, trip-time/Keister/Asian-option error comparisons, kernel
discrepancy calculations, and synthetic-beam comparisons, including the error
at every sample size with 64 randomly lost evaluations.
The optional [Pydantic AI beam tool loop](examples/beam/README.md) uses a
scripted policy by default and needs `pydantic-ai-slim`; the notebook itself
uses the standard `qmcpy` environment.

## Collaborator portraits

Follow [the shared collaborator workflow](classlib/docs/collaborators.md).
`data/collaborators.yml` explicitly selects this talk's people and order from
the pinned master names catalog. Master photographs remain in iCloud Drive's
`Collaborator Headshots` archive; this repository holds the selected
publishing copies and hash manifest needed by GitHub Pages.

```bash
bash classlib/tools/collaborator_assets.sh data/collaborators.yml --refresh
bash classlib/tools/collaborator_assets.sh data/collaborators.yml --check
```

Refresh reads iCloud deliberately. The slide pre-render check and public CI
use the committed copies and need no iCloud access. The QMCPy gallery features Choi and Sorokin first, then the remaining people
in surname order, with one six-column grid aligning all portrait rows.

## Sources

- The title and abstract in `index.qmd` are the author's approved seminar text.
- Figure origins and generation steps are recorded in [`assets/figures/README.md`](assets/figures/README.md).
- The deck uses the pinned HickernellAcademicLib `classlib` submodule for shared presentation styling.
- The introductory narrative adapts public MATH 565 slides; the lattice and Kronecker research narrative draws on the public MCQMC 2026 decks. The current lattice-prefix comparison independently checks generating vectors from Jiangrui Kang’s manuscript; its source and validation are recorded in `assets/figures/README.md` and `examples/wsesd/`.
- The synthetic beam code adapts the author’s Simon Grant prototype. Proposal text and saved grant results are not included.
