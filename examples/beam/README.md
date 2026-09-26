# Synthetic beam example

These four Python modules adapt Fred J. Hickernell's stochastic clamped-beam
prototype prepared for the Simon Grant work. They contain the mathematical beam
model, numerical laboratory, and bounded Pydantic AI tool loop. Proposal text,
saved grant results, credentials, and private research notes are not included.
The companion notebook recomputes its own small MC/RQMC comparison.

`model.py` and `laboratory.py` run in the standard `qmcpy` environment with
NumPy, SciPy, and QMCPy. The optional `agent.py` additionally requires
`pydantic-ai-slim`. Its default run uses a deterministic scripted policy via
Pydantic AI's `FunctionModel`; it makes no language-model API calls. A live
model may be supplied explicitly with `--model`, but no conclusion about live
model performance is represented by this example.

From the repository root:

```bash
python -m examples.beam.agent --output /tmp/strategic-beam-demo
```

The tool loop checks paired spatial refinements, runs an IID and RQMC pilot,
and validates one chosen configuration on fresh inputs. Its finite-panel mesh
comparison and approximate replicate-based interval do not certify total error.
This is a synthetic eight-input beam model, not a calibrated engineering case.
