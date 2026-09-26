# Sampling More Strategically But Just as Flexibly as IID

Source for Fred J. Hickernell's Illinois Tech School of Computing colloquium on November 9, 2026, at 1:50 PM America/Chicago. This repository contains the Quarto Reveal.js deck and a small companion website. The talk builds on, but is separate from, the MCQMC 2026 talks and manuscripts.

## Build

Clone with submodules, then render the website and slides:

```bash
git clone --recurse-submodules git@github.com:fjhickernell/StrategicSamplingColloquium.git
cd StrategicSamplingColloquium
quarto render
quarto render slides
```

The site publishes the rendered slides under `slides/` through `.github/workflows/publish.yml`.

## Sources

- The title and abstract in `index.qmd` are the author's approved colloquium text.
- The two sampling figures in `assets/figures/` come from the QMCSoftware website's “Why Add Q to MC?” article.
- The deck uses the pinned HickernellAcademicLib `classlib` submodule for shared presentation styling.
- MCQMC 2026 remains the source for conference-specific results and manuscripts; bring over individual figures or claims only with their provenance checked.
