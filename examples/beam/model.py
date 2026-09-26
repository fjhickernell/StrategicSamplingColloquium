"""Dimensionless Euler--Bernoulli beam, solved by equilibrium and compatibility.

On [0,1], (B w'')''=1, w(0)=w'(0)=w(1)=w'(1)=0.
M=B w''=a+b*x+x*x/2. Two weighted integrals determine a and b.
The reported response is 384*w(1/2); the uniform B=1 beam has response 1.
"""
from functools import lru_cache
import numpy as np
from scipy.special import roots_legendre
from scipy.linalg import solve
from scipy.integrate import solve_bvp

DIMENSION = 8
SIGMA = 0.45


def log_basis(x):
    j = np.arange(1, DIMENSION + 1, dtype=float)
    # RMS spatial log-stiffness SD is SIGMA; long waves carry most variance.
    amplitude = SIGMA * j ** -1.5 / np.sqrt(np.sum(j ** -3))
    return np.sqrt(2) * np.cos(np.pi * np.asarray(x)[..., None] * j) * amplitude


def stiffness(z, x):
    basis = log_basis(x)
    return np.exp(np.asarray(z) @ basis.T - 0.5 * np.sum(basis**2, axis=-1))


@lru_cache(maxsize=16)
def rule(cells):
    if cells not in (2, 4, 8, 16, 32, 64, 128):
        raise ValueError('Use 2, 4, 8, 16, 32, 64, or 128 spatial cells')
    # Four-point Gauss integration on each uniform cell. Even cell counts place
    # the midpoint response's kernel break exactly on a cell boundary.
    t, w = roots_legendre(4)
    x = (np.arange(cells)[:, None] + (t + 1)/2) / cells
    return x.ravel(), np.tile(w / (2*cells), cells)


def response(z, cells=16, return_reactions=False):
    z = np.asarray(z, dtype=float)
    if z.shape[-1] != DIMENSION or not np.isfinite(z).all():
        raise ValueError('Expected finite eight-dimensional Gaussian inputs')
    shape = z.shape[:-1]
    flat = z.reshape(-1, DIMENSION)
    x, weights = rule(cells)
    values, reactions = [], []
    for chunk in np.array_split(flat, max(1, int(np.ceil(len(flat) / 4096)))):
        weighted_compliance = weights / stiffness(chunk, x)
        s = np.stack([weighted_compliance @ x**k for k in range(4)], axis=-1)
        # Slope=0 and displacement=0 at x=1 are equivalent to integral M/B=0
        # and integral x*M/B=0. The matrix is a positive definite moment matrix.
        matrix = np.stack((s[:, :2], s[:, 1:3]), axis=-2)
        rhs = -0.5 * s[:, 2:4]
        ab = solve(matrix, rhs[..., None], assume_a='pos')[..., 0]
        moment = ab[:, :1] + ab[:, 1:] * x + x*x/2
        kernel = np.maximum(0.5 - x, 0)
        values.append(384 * np.sum(weighted_compliance * moment * kernel, axis=-1))
        reactions.append(ab)
    result = np.concatenate(values).reshape(shape)
    if return_reactions:
        return result, np.concatenate(reactions).reshape(shape + (2,))
    return result


def bvp_solution(z, tol=1e-9, uniform=False):
    def ode(x, y):
        b = np.ones_like(x) if uniform else stiffness(z, x)
        return np.vstack((y[1], y[2] / b, y[3], np.ones_like(x)))
    def boundary(left, right):
        return np.array([left[0], left[1], right[0], right[1]])
    x = np.linspace(0, 1, 65)
    solution = solve_bvp(ode, boundary, x, np.zeros((4, len(x))), tol=tol, max_nodes=10000)
    if not solution.success:
        raise RuntimeError(solution.message)
    return solution
