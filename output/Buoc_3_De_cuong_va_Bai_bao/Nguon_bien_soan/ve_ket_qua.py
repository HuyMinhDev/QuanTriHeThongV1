"""Plot recorded synthetic bounds; no data generation or fitted results."""
from pathlib import Path
import json
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

base=Path(__file__).resolve().parent.parent
data=json.loads((base/'Kiem_tra/simulation_results.json').read_text())
rows=[p for inst in data['instances'] for p in inst['prefix_checks']]
x=[r['structural_minimum_risk'] for r in rows]
fig,ax=plt.subplots(figsize=(7.3,4.2),layout='constrained')
ax.scatter(x,[r['bound_separate'] for r in rows],label='Componentwise bound',s=32,alpha=.6,marker='o',facecolors='none',edgecolors='#4C78A8')
ax.scatter(x,[r['bound_mixture'] for r in rows],label='Mixture bound',s=18,alpha=.65,marker='x',color='#E45756')
ax.plot([0,1],[0,1],color='#333333',linestyle='--',linewidth=1,label='Exact bound')
ax.set(xlabel='Exact minimum structural CVaR (enumeration)',ylabel='Necessary lower bound',xlim=(-.03,1.03),ylim=(-.03,1.03),title='Finite synthetic validation: 240 prefixes, 40 instances')
ax.grid(alpha=.18);ax.legend(loc='upper left',fontsize=9)
fig.savefig(base/'Kiem_tra/bound_comparison.png',dpi=220)
fig.savefig(base/'Kiem_tra/bound_comparison.pdf')
print('Plotted',len(rows),'recorded prefixes')
