"""Independently reconstruct bit-reversed lattice prefix discrepancies.

For a translation-invariant kernel g(k)=K(k*z/N,0)-1, a complete even
subgroup has the same cross sum with every odd point. Thus, with h=N/2,
S_N(h+j)=S_h(h)+S_h(j)+2*j*sum(g(1::2)), where S is the unnormalized
pair sum and S_h uses g(2*k). This computes every prefix without the
original experiment engine. No new CBC optimization is performed.
"""
from pathlib import Path
import argparse
import csv
import json
import math
import re
import shutil
import subprocess
import time
import numpy as np

PROJECT = Path(__file__).resolve().parents[2]
N = 2**20

def read_vectors(repo):
    text = (repo/'benchmark_provenance.tex').read_text()
    labels = {'KCN':'KCN', 'CBCDBD':'DBD', 'W001':'$W_{0.01}$', 'W025':'$W_{1/4}$'}
    vectors = {}
    for name,label in labels.items():
        block = text.split('\\noindent '+label+':',1)[1]
        block = block.split('\\begin{gathered}',1)[1].split('\\end{gathered}',1)[0]
        vector = [int(v) for v in re.findall(r'\d+',block)]
        assert len(vector)==13 and all(0<z<N and z%2 for z in vector)
        vectors[name]=vector
    return vectors

def kernel(vector):
    k = np.arange(N, dtype=np.int64)
    logs = np.zeros(N)
    for j, z in enumerate(vector, 1):
        r = k*z % N
        # Exact integer numerator before the sole floating-point division.
        numerator = 6*r*r - 6*r*N + N*N
        logs += np.log1p(numerator / (6*N*N*j*j))
    return np.expm1(logs)

def all_prefixes(g):
    pair_sums = np.array([0., g[0]])
    for level in range(1, 21):
        h = 2**(level-1)
        stride = N // (2*h)
        cross = math.fsum(g[stride::2*stride])
        pair_sums = np.concatenate((pair_sums,
            pair_sums[-1] + pair_sums[1:] + 2*np.arange(1,h+1)*cross))
    assert np.all(pair_sums[1:] > 0)
    return np.sqrt(pair_sums[1:]) / np.arange(1,N+1)

def bitreverse(indices):
    out = np.zeros_like(indices)
    for i in range(20): out |= ((indices>>i)&1) << (19-i)
    return out

def direct(g, n):
    points = bitreverse(np.arange(n, dtype=np.int64))
    differences = (points[:,None]-points[None,:]) % N
    return math.sqrt(math.fsum(g[differences].ravel())) / n

def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--manuscript',type=Path,default=PROJECT.parent/'wsesd-cbc-manuscript')
    parser.add_argument('--output',type=Path,default=PROJECT/'outputs/wsesd-review')
    parser.add_argument('--asset-directory',type=Path,
        help='Also save the talk figure and verification record here')
    args = parser.parse_args()
    repo,out = args.manuscript.resolve(),args.output.resolve()
    out.mkdir(parents=True,exist_ok=True)
    vectors = read_vectors(repo)
    configs = list(csv.DictReader((repo/'results/supplement_S3_methods.csv').open()))
    assert all(int(row['N_max'])==N for row in configs)
    start = time.perf_counter()
    curves = {}
    direct_errors = []
    for name, vector in vectors.items():
        for s in [3,6,13]:
            g = kernel(vector[:s])
            d = all_prefixes(g)
            curves[f'{name}_{s}'] = d
            for n in [17,37,129,257]:
                direct_errors.append(abs(d[n-1]/direct(g,n)-1))
            print(name,s,'D_N',d[-1],flush=True)
    endpoints = list(csv.DictReader((repo/'results/supplement_S1_endpoints.csv').open()))
    endpoint_errors = []
    for row in endpoints:
        for method in vectors:
            actual = curves[f'{method}_{row["s"]}'][int(row['n'])-1]
            endpoint_errors.append(abs(actual/float(row[method])-1))
    summary = []
    for row in csv.DictReader((repo/'results/table1.csv').open()):
        sizes = np.arange(1024,N+1)
        dyadic = (sizes & (sizes-1)) == 0
        sizes = sizes[dyadic if row['class']=='P' else ~dyadic]
        ratio = curves[f'{row["A"]}_13'][sizes-1] / curves[f'{row["B"]}_13'][sizes-1]
        q10,q50,q90 = np.quantile(ratio,[.1,.5,.9])
        summary.append(dict(A=row['A'],B=row['B'],size_class=row['class'],
            q50=float(q50),win_count=int(np.sum(ratio<1)),
            max_ratio=float(ratio.max()),
            q50_difference=float(q50)-float(row['q50']),
            win_count_difference=int(np.sum(ratio<1))-int(row['win_count'])))
    assert max(direct_errors)<1e-12
    assert max(endpoint_errors)<1e-6
    assert all(row['win_count_difference']==0 for row in summary)
    assert max(abs(row['q50_difference']) for row in summary)<1e-7
    report = dict(source_commit=subprocess.check_output(['git','rev-parse','HEAD'],cwd=repo,text=True).strip(),
        kernel='product(1+j^-2 B2(frac(x-y)))',dimensions=[3,6,13],N=N,
        direct_checks=len(direct_errors),endpoint_checks=len(endpoint_errors),
        max_direct_relative_difference=max(direct_errors),
        max_endpoint_relative_difference=max(endpoint_errors),summary=summary,
        seconds=time.perf_counter()-start,
        limitation='Evaluates supplied vectors; does not verify their CBC construction or integration arrays')
    np.savez_compressed(out/'independent_discrepancy.npz',**curves)
    (out/'verification.json').write_text(json.dumps(report,indent=2)+'\n')
    plot(curves,out)
    if args.asset_directory:
        destination=args.asset_directory.resolve()
        destination.mkdir(parents=True,exist_ok=True)
        for extension in ['png','svg']:
            shutil.copyfile(out/f'wsesd_prefix_discrepancy.{extension}',
                destination/f'wsesd_prefix_discrepancy.{extension}')
        shutil.copyfile(out/'verification.json',destination/'wsesd_prefix_discrepancy.json')
    print(json.dumps(report,indent=2))

def plot(curves,out):
    import matplotlib
    matplotlib.use('Agg')
    import matplotlib.pyplot as plt
    from matplotlib.ticker import FixedLocator,FixedFormatter
    plt.rcParams.update({'font.size':20,'mathtext.fontset':'stix','axes.spines.top':False,
        'axes.spines.right':False,'axes.grid':False,'svg.fonttype':'path'})
    colors={'KCN':'#0072B2','CBCDBD':'#009E73','W001':'#D55E00','W025':'#B55A96'}
    labels={'KCN':'Kuo–Cools–Nuyens (KCN)','CBCDBD':'CBC–DBD','W001':r'WSESD: $\omega_n=n^{0.98}$','W025':r'WSESD: $\omega_n=n^{0.5}$'}
    fig,(ax,bx)=plt.subplots(1,2,figsize=(14,5.8),gridspec_kw={'width_ratios':[1.12,1]})
    n=np.arange(1024,N+1)
    iid=np.sqrt(np.expm1(np.log1p(1/(6*np.arange(1,14)**2)).sum())/n)
    ax.loglog(n,iid,color='#777777',ls='--',lw=1.8,label='IID (exact reference)')
    for name in ['KCN','W001']:
        ax.loglog(n,curves[f'{name}_13'][n-1],color=colors[name],lw=1.2,label=labels[name],rasterized=True)
    ax.set(xlabel='Sample size n',ylabel='Root ESD',title='')
    ticks=2**np.arange(10,21,2)
    ax.xaxis.set_major_locator(FixedLocator(ticks))
    ax.xaxis.set_major_formatter(FixedFormatter([rf'$2^{{{k}}}$' for k in range(10,21,2)]))
    ax.minorticks_off()
    ax.legend(frameon=False,fontsize=17,loc='lower left',
        bbox_to_anchor=(0,1.02),borderaxespad=0)
    # Every box uses all non-dyadic integers in one open doubling interval.
    # Boxes sit between their bounding powers of two on the log2 n axis.
    # Whiskers deliberately show the full range, not the 1.5-IQR convention.
    ratios=[]
    for k in range(10,20):
        sizes=np.arange(2**k+1,2**(k+1))
        ratios.append(curves['W001_13'][sizes-1]/curves['KCN_13'][sizes-1])
    bx.boxplot(ratios,positions=np.arange(10,20)+.5,widths=.6,whis=(0,100),
        showfliers=False,patch_artist=True,
        boxprops={'facecolor':'#F9D8C4','edgecolor':colors['W001'],'linewidth':1.3},
        whiskerprops={'color':colors['W001'],'linewidth':1.2},
        capprops={'color':colors['W001'],'linewidth':1.2},
        medianprops={'color':colors['W001'],'linewidth':2})
    bx.axhline(1,color='#555555',ls='--',lw=1)
    bx.set(xlabel='Sample size n',ylabel='Root ESD: WSESD / KCN',
        xticks=np.arange(10,21),xlim=(9.75,20.25),
        ylim=(min(float(r.min()) for r in ratios)-.03,1.16))
    bx.set_xticklabels([rf'$2^{{{k}}}$' for k in range(10,21)],fontsize=17)
    bx.xaxis.label.set_size(18)
    bx.yaxis.label.set_size(18)
    fig.subplots_adjust(left=.09,right=.985,top=.76,bottom=.23,wspace=.38)
    fig.savefig(out/'wsesd_prefix_discrepancy.png',dpi=200)
    svg_path=out/'wsesd_prefix_discrepancy.svg'
    fig.savefig(svg_path,dpi=200)
    svg_path.write_text('\n'.join(line.rstrip() for line in svg_path.read_text().splitlines())+'\n')
    plt.close(fig)

if __name__ == '__main__': main()
