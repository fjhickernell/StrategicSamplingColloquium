"""Bounded tools; no reference answer is exposed to the decision policy."""
from dataclasses import dataclass, field
import math
import time
import numpy as np
import qmcpy as qp
from scipy.special import ndtri
from scipy.stats import t
from .model import DIMENSION, response


def inputs(method, n, replications, seed):
    if method not in ('MC', 'RQMC') or n < 2 or n & (n-1) or replications < 2:
        raise ValueError('Use MC/RQMC, power-of-two n, and at least two replications')
    sampler = qp.IIDStdUniform if method == 'MC' else qp.Sobol
    u = sampler(dimension=DIMENSION, replications=replications, seed=int(seed)).gen_samples(n)
    if np.any((u <= 0) | (u >= 1)):
        raise ValueError('Gaussian transform requires points strictly inside (0,1)')
    return ndtri(u)


def evaluate(method, n, replications, seed, cells):
    start = time.perf_counter()
    means = response(inputs(method, n, replications, seed), cells).mean(axis=1)
    se = float(means.std(ddof=1) / np.sqrt(replications))
    return dict(method=method, n=n, replications=replications, seed=int(seed), cells=cells,
                estimate=float(means.mean()), half_width_99=float(t.ppf(.995, replications-1)*se),
                replicate_means=means.tolist(), beam_solves=n*replications,
                stiffness_evaluations=n*replications*4*cells, seconds=time.perf_counter()-start)


@dataclass
class BeamLab:
    seed: int = 20260917
    tolerance: float = 0.0005
    records: list = field(default_factory=list)
    budget: int = 140000

    def __post_init__(self):
        if not math.isfinite(self.tolerance) or self.tolerance <= 0:
            raise ValueError('Tolerance must be finite and positive')

    def specification(self):
        return dict(problem='Mean normalized midpoint deflection, clamped beam, unit load',
                    stiffness='Mean-one lognormal field; 8 cosine modes; spatial RMS log SD 0.45',
                    tolerance=self.tolerance, solver_allowance=self.tolerance/4,
                    sampling_allowance=self.tolerance*3/4, replications=16,
                    pilot_n=128, validation_sizes=[128,256,512,1024,2048,4096],
                    cells=[2,4,8,16,32,64], budget=self.budget,
                    protocol='Check paired refinement, pilot both methods at an accepted resolution, validate once. '
                    '99% Student-t intervals and refinement diagnostics are not certified bounds.')

    def _seed(self, phase, method=0, cells=0):
        return int(np.random.SeedSequence([self.seed, phase, method, cells]).generate_state(1)[0])

    def _reserve(self, solves):
        if any(r['phase']=='validation' for r in self.records):
            raise ValueError('Validation has finished; no further data collection is allowed')
        if sum(r['beam_solves'] for r in self.records)+solves > self.budget:
            raise ValueError('Beam-solve budget exceeded')

    def check_solver(self, cells: int):
        if cells not in (2,4,8,16,32,64):
            raise ValueError('Unsupported spatial cell count')
        if any(r['phase']=='refinement' and r['cells']==cells for r in self.records):
            raise ValueError('This refinement has already been measured')
        self._reserve(256)
        start = time.perf_counter()
        z = inputs('RQMC', 16, 8, self._seed(0))
        difference = response(z, cells*2)-response(z, cells)
        # Conservative finite-panel diagnostic, not a bound on unseen inputs or bias.
        diagnostic = float(np.max(np.abs(difference)))
        row = dict(phase='refinement', cells=cells, fine_cells=2*cells,
                   paired_inputs=128, beam_solves=256, stiffness_evaluations=128*12*cells,
                   maximum_paired_difference=diagnostic,
                   mean_paired_difference=float(difference.mean()),
                   accepted=diagnostic <= self.tolerance/4, seconds=time.perf_counter()-start)
        self.records.append(row)
        return row.copy()

    def pilot(self, method: str, cells: int):
        if method not in ('MC','RQMC'):
            raise ValueError('Unknown method')
        if not any(r['phase']=='refinement' and r['cells']==cells and r['accepted'] for r in self.records):
            raise ValueError('First obtain an acceptable paired refinement at this resolution')
        if any(r['phase']=='pilot' and r['method']==method for r in self.records):
            raise ValueError('Only one pilot per method is allowed')
        pilots=[r for r in self.records if r['phase']=='pilot']
        if pilots and pilots[0]['cells'] != cells:
            raise ValueError('Both pilots must use the same spatial cell count')
        self._reserve(2048)
        row=evaluate(method,128,16,self._seed(1,int(method=='RQMC')),cells)
        row['phase']='pilot'
        self.records.append(row)
        return {k:v for k,v in row.items() if k!='replicate_means'}

    def validate(self, method: str, n: int, cells: int):
        pilots=[r for r in self.records if r['phase']=='pilot']
        if len(pilots)!=2 or method not in ('MC','RQMC'):
            raise ValueError('Both sampling pilots are required')
        if n not in (128,256,512,1024,2048,4096) or cells!=pilots[0]['cells']:
            raise ValueError('Use a supported sample count and the pilot spatial cell count')
        self._reserve(n*16)
        row=evaluate(method,n,16,self._seed(2,int(method=='RQMC')),cells)
        row.update(phase='validation', sampling_target_met=row['half_width_99']<=self.tolerance*3/4)
        self.records.append(row)
        return {k:v for k,v in row.items() if k!='replicate_means'}


def choose(pilots, allowance):
    candidates=[]
    for p in pilots:
        exponent=0.5 if p['method']=='MC' else 1.0
        raw=128*max(1,(1.5*p['half_width_99']/allowance)**(1/exponent))
        requested=2**max(7,math.ceil(math.log2(raw)))
        candidates.append((requested,p['method']))
    requested,method=min(candidates)
    return method,min(4096,requested)
