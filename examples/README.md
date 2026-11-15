# Computational examples

The `beam/` package is a self-contained synthetic example adapted from the
author's Simon Grant prototype. See its README for the mathematical and
Pydantic AI scope. `notebooks/StrategicSampling.ipynb` recomputes the talk's
beam comparison with the standard `qmcpy` kernel.

`wsesd/check_discrepancy.py` independently reconstructs all lattice-prefix
discrepancies from the current manuscript's recorded generating vectors.
It checks direct kernel sums, published endpoints, and all eight main-table
win counts before making the talk's compact comparison figure. It does not
reconstruct the CBC optimization or integration experiments.

With Jiangrui's manuscript checkout beside this repository, run in the
standard `qmcpy` environment:

```bash
python examples/wsesd/check_discrepancy.py --asset-directory assets/figures
```

Use `--manuscript PATH` for another checkout location. Full reconstructed
curves and the verification report go to the ignored `outputs/wsesd-review/`;
the optional asset argument also refreshes the SVG, PNG, and JSON provenance
record used by the deck. All counts refer to the fixed supplied vectors,
kernel, dimensions, and finite maximum specified in that source snapshot.
