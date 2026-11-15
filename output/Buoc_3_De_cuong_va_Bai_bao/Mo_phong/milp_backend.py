"""SciPy/HiGHS model for the finite scenario formulation.

Returns solver evidence, not an independently verified UNSAT proof.
Every primal incumbent is checked by core.verify after decoding.
"""
import math
import numpy as np
from scipy.optimize import Bounds,LinearConstraint,milp
from scipy.sparse import coo_matrix
from core import TOL,baseline,utilities,verify


def solve(inst,prefix=None,objective='feasibility',ignore_risk=False,time_limit=5,relax_integrality=False):
    prefix=prefix or {}; xkeys=[(u,i,r) for u,c in enumerate(inst.candidates) for i in c for r in range(inst.K)]
    index={k:j for j,k in enumerate(xkeys)};n=len(index)
    groups=[sorted(set().union(*(set(inst.genres[i]) for i in c))) for c in inst.candidates]
    zindex={}
    for u,gg in enumerate(groups):
        for g in gg:zindex[u,g]=n;n+=1
    eta=n;n+=1;vindex=list(range(n,n+inst.S));n+=inst.S
    lo=np.zeros(n);hi=np.ones(n);integral=np.zeros(n)
    for j in list(index.values())+list(zindex.values()):integral[j]=0 if relax_integrality else 1
    rows=[];cols=[];data=[];lower=[];upper=[]
    def constraint(coeff,lb=-math.inf,ub=math.inf):
        row=len(lower)
        for j,value in coeff.items():
            if value:rows.append(row);cols.append(j);data.append(value)
        lower.append(lb);upper.append(ub)
    for u,c in enumerate(inst.candidates):
        for r in range(inst.K):constraint({index[u,i,r]:1 for i in c},1,1)
        for i in c:constraint({index[u,i,r]:1 for r in range(inst.K)},ub=1)
    for (u,r),i in prefix.items():
        if (u,i,r) not in index:return {'status':'INFEASIBLE','ranking':None,'reason':'prefix outside candidates'}
        lo[index[u,i,r]]=hi[index[u,i,r]]=1
    base=utilities(inst,baseline(inst))
    for u,c in enumerate(inst.candidates):
        constraint({index[u,i,r]:inst.weights[r]*inst.scores[u][i] for i in c for r in range(inst.K)},lb=(1-inst.epsilon)*base[u])
        for g in groups[u]:
            ids=[i for i in c if g in inst.genres[i]]; z=zindex[u,g]
            aa={index[u,i,r]:1 for i in ids for r in range(inst.K)}
            constraint({**{j:-a for j,a in aa.items()},z:1},ub=0)
            constraint({**aa,z:-min(inst.K,len(ids))},ub=0)
        constraint({zindex[u,g]:1 for g in groups[u]},lb=inst.diversity[u])
    for s in range(inst.S):
        aa={index[u,i,r]:inst.weights[r]*inst.heads[i][s]/inst.denominator for u,c in enumerate(inst.candidates) for i in c for r in range(inst.K)}
        aa[eta]=-1;aa[vindex[s]]=-1;constraint(aa,ub=0)
    riskcoef={eta:1,**{j:1/((1-inst.alpha)*inst.S) for j in vindex}}
    if not ignore_risk:constraint(riskcoef,ub=inst.theta)
    cost=np.zeros(n)
    if objective=='risk':
        for j,a in riskcoef.items():cost[j]=a
    elif objective=='quality':
        for (u,i,r),j in index.items():cost[j]=-inst.weights[r]*inst.scores[u][i]/inst.denominator
        universe=max(1,len(set().union(*(set(v) for v in inst.genres.values()))))
        for j in zindex.values():cost[j]=-inst.diversity_weight/(inst.B*universe)
    matrix=coo_matrix((data,(rows,cols)),shape=(len(lower),n)).tocsc()
    out=milp(cost,integrality=integral,bounds=Bounds(lo,hi),
             constraints=LinearConstraint(matrix,np.array(lower),np.array(upper)),
             options={'time_limit':time_limit,'mip_rel_gap':0.0,'presolve':True})
    evidence={'solver_status':int(out.status),'message':out.message,'variables':n,
              'constraints':len(lower),'mip_gap':getattr(out,'mip_gap',None),
              'dual_bound':getattr(out,'mip_dual_bound',None)}
    if relax_integrality:
        return {'status':'RELAXATION','optimal':out.status==0,'objective':None if out.fun is None else float(out.fun),'evidence':evidence}
    if out.x is not None:
        ranking=tuple(tuple(max(c,key=lambda i:out.x[index[u,i,r]]) for r in range(inst.K)) for u,c in enumerate(inst.candidates))
        checked=verify(inst,ranking,ignore_risk)
        prefix_ok=all(ranking[u][r]==i for (u,r),i in prefix.items())
        if checked['feasible'] and prefix_ok:
            return {'status':'FEASIBLE','ranking':ranking,'metrics':checked,'optimal':out.status==0,'evidence':evidence}
        return {'status':'UNKNOWN','ranking':None,'reason':'incumbent failed independent primal check','evidence':evidence}
    return {'status':'INFEASIBLE' if out.status==2 else 'UNKNOWN','ranking':None,'optimal':False,'evidence':evidence}
