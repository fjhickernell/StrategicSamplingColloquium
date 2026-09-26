"""Pydantic AI tool loop with an executable baseline and optional live model."""
import argparse
import hashlib
import importlib.metadata
import json
import platform
from pathlib import Path
from datetime import datetime, timezone
from typing import Literal
from pydantic_ai import Agent, RunContext
from pydantic_ai.models.function import FunctionModel
from pydantic_ai.messages import ModelResponse, TextPart, ToolCallPart, ToolReturnPart
from pydantic_ai.usage import UsageLimits
from .laboratory import BeamLab, choose

INSTRUCTIONS = '''Investigate the stochastic clamped beam using only the supplied tools.
Inspect the specification. Determine a sufficient number of spatial cells using paired
mesh refinements; start coarse and refine if necessary. A passing diagnostic is evidence,
not a bound. Run both MC and RQMC pilots at the same accepted resolution. Compare measured
uncertainty and costs, choose a method and fixed sample budget, and validate once with
fresh randomness. For planning you may use n^-1/2 for MC and n^-1 for RQMC with a 1.5 margin;
these are heuristics. Do not assume which method wins. Report tool evidence, mesh choice,
sampling uncertainty and limitations. Do not claim LLM superiority, certified accuracy,
or multilevel operation. If the target is missed, report it without further validation.'''


def scripted_policy(messages, info):
    returns=[p for m in messages for p in m.parts if isinstance(p,ToolReturnPart)]
    def call(name, **kwargs):
        return ModelResponse(parts=[ToolCallPart(name,kwargs)])
    if not returns:
        return call('describe_experiment')
    checks=[p.content for p in returns if p.tool_name=='check_spatial_resolution']
    accepted=[r for r in checks if r['accepted']]
    if not accepted:
        cells=2 if not checks else checks[-1]['cells']*2
        if cells>64:
            return ModelResponse(parts=[TextPart('No tested spatial resolution passed; experiment stopped.')])
        return call('check_spatial_resolution',cells=cells)
    cells=accepted[0]['cells']
    pilots=[p.content for p in returns if p.tool_name=='run_pilot']
    if len(pilots)<2:
        return call('run_pilot',method=('MC','RQMC')[len(pilots)],cells=cells)
    validations=[p.content for p in returns if p.tool_name=='run_validation']
    if not validations:
        spec=next(p.content for p in returns if p.tool_name=='describe_experiment')
        method,n=choose(pilots,spec['sampling_allowance'])
        return call('run_validation',method=method,n=n,cells=cells)
    r=validations[0]
    return ModelResponse(parts=[TextPart(
        f"Scripted policy selected {cells} spatial cells and {r['method']}, then "
        f"validated with {r['beam_solves']:,} fresh beam solves. Estimate {r['estimate']:.9f}; "
        f"approximate 99% sampling half-width {r['half_width_99']:.3g}; "
        f"sampling target met: {r['sampling_target_met']}. Mesh refinement is a diagnostic, "
        "not a certified bound. This run used no language model and no multilevel method."
    )])


def build_agent(model):
    agent=Agent(model,deps_type=BeamLab,instructions=INSTRUCTIONS)
    @agent.tool
    def describe_experiment(ctx: RunContext[BeamLab]) -> dict:
        """Get the model, allowances and computational budget; no reference solution."""
        return ctx.deps.specification()
    @agent.tool
    def check_spatial_resolution(ctx: RunContext[BeamLab], cells: int) -> dict:
        """Compare cells and 2*cells on the same 128 stiffness fields; cells=2,...,64."""
        return ctx.deps.check_solver(cells)
    @agent.tool
    def run_pilot(ctx: RunContext[BeamLab], method: Literal['MC','RQMC'], cells: int) -> dict:
        """Run one 16-by-128 pilot at an accepted spatial resolution."""
        return ctx.deps.pilot(method,cells)
    @agent.tool
    def run_validation(ctx: RunContext[BeamLab], method: Literal['MC','RQMC'], n: int, cells: int) -> dict:
        """One independent 16-replication validation; power-of-two n from 128 to 4096."""
        return ctx.deps.validate(method,n,cells)
    return agent


def run(output, model=None, seed=20260917, tolerance=0.0005):
    output=Path(output)
    output.mkdir(parents=True,exist_ok=True)
    lab=BeamLab(seed=seed,tolerance=tolerance)
    agent=build_agent(model or FunctionModel(scripted_policy,model_name='scripted-beam-policy'))
    result=agent.run_sync('Choose spatial resolution and sampling method for the beam expectation.',
                         deps=lab,usage_limits=UsageLimits(request_limit=16,tool_calls_limit=14))
    metadata=dict(timestamp_utc=datetime.now(timezone.utc).isoformat(),
                  mode='live-model' if model else 'scripted-policy (no LLM)', model=model,
                  seed=seed, python=platform.python_version(), platform=platform.platform(),
                  versions={p:importlib.metadata.version(p) for p in
                            ['qmcpy','numpy','scipy','matplotlib','pydantic','pydantic-ai-slim']},
                  source_sha256={p.name:hashlib.sha256(p.read_bytes()).hexdigest()
                                 for p in Path(__file__).parent.glob('*.py')},
                  specification=lab.specification(),records=lab.records,
                  total_beam_solves=sum(r['beam_solves'] for r in lab.records),
                  total_stiffness_evaluations=sum(r['stiffness_evaluations'] for r in lab.records),
                  numerical_seconds=sum(r['seconds'] for r in lab.records),
                  completed=bool(lab.records and lab.records[-1]['phase']=='validation'),
                  agent_summary=result.output)
    (output/'run.json').write_text(json.dumps(metadata,indent=2)+'\n')
    (output/'agent-messages.json').write_bytes(result.all_messages_json())
    print(result.output)
    print(f"Total beam solves including refinement and pilots: {metadata['total_beam_solves']:,}")
    return metadata


if __name__=='__main__':
    parser=argparse.ArgumentParser()
    parser.add_argument('--output',default='outputs/beam')
    parser.add_argument('--model',help='Pydantic AI provider:model; omitted means scripted baseline')
    parser.add_argument('--seed',type=int,default=20260917)
    parser.add_argument('--tolerance',type=float,default=0.0005)
    args=parser.parse_args()
    run(args.output,args.model,args.seed,args.tolerance)
