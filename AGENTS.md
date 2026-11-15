<!-- classlib-consumer-contract:start -->
## Shared classlib guidance

This repository consumes `classlib` as a pinned submodule. Initialize the
recorded submodule commit before substantive work; do not replace it with a
moving branch tip during routine setup or validation.

Before substantive work involving shared teaching, presentation, webpage,
content, component, or infrastructure conventions, read
`classlib/AGENTS.md`. Guidance applies in this order:

1. applicable global instructions;
2. shared guidance in the pinned `classlib/AGENTS.md`;
3. explicit consumer-local instructions and exceptions.

Keep universal guidance in `classlib` rather than copying it locally. Record a
genuine local exception explicitly, including its scope and reason. Flag an
apparent accidental conflict for review instead of silently resolving it.
<!-- classlib-consumer-contract:end -->

# Strategic Sampling seminar

This repository holds the Illinois Tech Applied Mathematics and Statistics Seminar deck and
its companion Quarto site. The talk is separate from MCQMC 2026; that
repository is a source for verified research, figures, and presentation ideas,
not a place to develop this talk.

Keep the author's approved title and abstract in `index.qmd`. Record confirmed
event details only; do not infer the room or talk length. Develop talk-specific
slides and assets here. Keep research claims tied to checked sources, and do
not present exploratory or unpublished results as established conclusions.

Render both the root website and `slides/` after substantive changes; inspect
the affected pages and slides before publication. Keep generated files out of
Git and reconcile `notes/NEXT.md` when the immediate work changes.

## Collaborator workflow

Follow the shared `classlib/docs/collaborators.md` workflow. Names and stable
IDs come from the pinned master catalog; master photographs remain in iCloud
Drive's `Collaborator Headshots` archive. `data/collaborators.yml` explicitly
selects this talk's people and gallery order. Refresh its selected publishing
copies and generated caption include with the shared helper; the slide
pre-render check validates them without iCloud access. Do not hand-edit
`slides/_includes/qmcpy-contributors.qmd` or infer a talk roster from the full
master catalog. Keep Sou-Cheng Choi and Aleksei Sorokin featured in the QMCPy top row,
with the other collaborators in surname order in one aligned grid;
retain the separately approved chronological student-contribution rows.
Selected publishing portraits, their hash manifest, and the generated gallery
include are versioned build inputs so public CI does not require iCloud;
rendered website/slide output and local previews remain ignored.

## Explicit local exception

The approved abstract spells “low-discrepancy” with a hyphen. Preserve that
author-approved wording on the public landing page, despite the shared slide
style guide's preference for “low discrepancy” without a hyphen.
