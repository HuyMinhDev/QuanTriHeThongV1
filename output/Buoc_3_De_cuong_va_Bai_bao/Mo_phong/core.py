"""Finite-instance research prototype; no real-data benchmark claims.

alpha denotes confidence, beta=1-alpha is upper-tail probability mass.
Certificates apply to the supplied instance and numeric tolerance only.
"""
from dataclasses import dataclass
import itertools
import math

TOL=1e-8


@dataclass(frozen=True)
class Instance:
    candidates: tuple
    scores: tuple
    genres: dict
    heads: dict
    weights: tuple
    epsilon: float
    diversity: tuple
    alpha: float
    theta: float
    diversity_weight: float=.1

    def __post_init__(self):
        if not self.candidates or not self.weights or not 0<=self.alpha<1:
            raise ValueError('Nonempty users/slots and 0<=alpha<1 required')
        if len(self.scores)!=self.B or len(self.diversity)!=self.B:
            raise ValueError('One score map and diversity floor per user required')
        if not 0<=self.epsilon<=1 or not 0<=self.theta<=1:
            raise ValueError('epsilon/theta outside [0,1]')
        if any(not math.isfinite(w) or w<=0 for w in self.weights):
            raise ValueError('Positive finite rank weights required')
        lengths=set()
        for u,c in enumerate(self.candidates):
            if len(set(c))!=len(c): raise ValueError('Duplicate candidate ID')
            for i in c:
                s=self.scores[u][i]
                if not math.isfinite(s) or not 0<=s<=1: raise ValueError('scores must be in [0,1]')
                if i not in self.genres or i not in self.heads: raise ValueError('Missing metadata')
                if any(h not in (0,1) for h in self.heads[i]): raise ValueError('Binary scenario labels required')
                lengths.add(len(self.heads[i]))
        if len(lengths)!=1 or next(iter(lengths),0)==0: raise ValueError('Consistent nonempty scenarios required')

    @property
    def B(self): return len(self.candidates)
    @property
    def K(self): return len(self.weights)
    @property
    def S(self): return len(next(iter(self.heads.values())))
    @property
    def denominator(self): return self.B*sum(self.weights)


def tail_weights(values,alpha):
    if not values or not 0<=alpha<1: raise ValueError('Invalid CVaR inputs')
    mass=(1-alpha)*len(values)
    remaining=mass; rho=[0.]*len(values)
    for s in sorted(range(len(values)),key=lambda s:(-values[s],s)):
        take=min(1.,remaining)
        rho[s]=take/mass
        remaining-=take
        if remaining<=1e-12: break
    return rho


def cvar(values,alpha):
    return sum(q*v for q,v in zip(tail_weights(values,alpha),values))


def baseline(inst):
    return tuple(tuple(sorted(c,key=lambda i:(-inst.scores[u][i],i))[:inst.K]) for u,c in enumerate(inst.candidates))


def utilities(inst,ranking):
    return [sum(inst.weights[r]*inst.scores[u][i] for r,i in enumerate(row)) for u,row in enumerate(ranking)]


def exposure(inst,ranking):
    return [sum(inst.weights[r]*inst.heads[i][s] for row in ranking for r,i in enumerate(row))/inst.denominator for s in range(inst.S)]


def verify(inst,ranking,ignore_risk=False):
    if ranking is None or len(ranking)!=inst.B:
        return {'feasible':False,'reason':'missing users'}
    if any(len(row)!=inst.K or len(set(row))!=inst.K or not set(row)<=set(inst.candidates[u]) for u,row in enumerate(ranking)):
        return {'feasible':False,'reason':'invalid structure'}
    util=utilities(inst,ranking); base=utilities(inst,baseline(inst))
    cov=[len(set().union(*(set(inst.genres[i]) for i in row))) for row in ranking]
    h=exposure(inst,ranking); risk=cvar(h,inst.alpha)
    deficits=[max(0.,(1-inst.epsilon)*b-v) for b,v in zip(base,util)]
    divdef=[max(0,d-v) for d,v in zip(inst.diversity,cov)]
    objective=sum(util)/inst.denominator+inst.diversity_weight*sum(cov)/(inst.B*max(1,len(set().union(*(set(v) for v in inst.genres.values())))))
    return {'feasible':max(deficits,default=0)<=TOL and max(divdef,default=0)==0 and (ignore_risk or risk<=inst.theta+TOL),
            'utilities':util,'base_utilities':base,'coverage':cov,'scenario_exposure':h,'risk':risk,
            'utility_deficits':deficits,'diversity_deficits':divdef,'risk_violation':max(0,risk-inst.theta),
            'objective':objective,'risk_budget_enforced':not ignore_risk}


def residual(inst,prefix):
    prefix=prefix or {}; rows=[]
    if any(not (0<=u<inst.B and 0<=r<inst.K) for u,r in prefix): return None
    for u,c in enumerate(inst.candidates):
        fixed=[i for (v,r),i in prefix.items() if v==u]
        if len(set(fixed))!=len(fixed) or not set(fixed)<=set(c): return None
        slots=[r for r in range(inst.K) if (u,r) not in prefix]
        available=[i for i in c if i not in fixed]
        if len(available)<len(slots): return None
        rows.append((slots,available))
    return rows


def structural_rankings(inst,prefix=None):
    prefix=prefix or {}; rem=residual(inst,prefix)
    if rem is None: return
    def visit(u,rows):
        if u==inst.B:
            yield tuple(rows);return
        slots,available=rem[u]
        for chosen in itertools.permutations(available,len(slots)):
            row=[prefix.get((u,r)) for r in range(inst.K)]
            for r,i in zip(slots,chosen): row[r]=i
            yield from visit(u+1,rows+[tuple(row)])
    yield from visit(0,[])


def lower_bounds(inst,prefix=None):
    prefix=prefix or {}; rem=residual(inst,prefix)
    if rem is None: return {'structural_infeasible':True,'separate':math.inf,'mixture':math.inf}
    def fixed_cost(coeff):
        return sum(inst.weights[r]*coeff[i] for (u,r),i in prefix.items())
    def structural_min(coeff):
        cost=fixed_cost(coeff)
        for slots,available in rem:
            w=sorted((inst.weights[r] for r in slots),reverse=True)
            a=sorted(coeff[i] for i in available)[:len(slots)]
            cost+=sum(x*y for x,y in zip(w,a))
        return cost/inst.denominator
    ids=set().union(*(set(c) for c in inst.candidates))
    b=[structural_min({i:inst.heads[i][s] for i in ids}) for s in range(inst.S)]
    mixtures=[tail_weights(b,inst.alpha),[1/inst.S]*inst.S]
    # Additional valid envelope points: scenario-centred cyclic orders.
    cap=1/((1-inst.alpha)*inst.S)
    for start in range(min(inst.S,2)):
        q=[0.]*inst.S;left=1.
        for j in range(inst.S):
            s=(start+j)%inst.S; take=min(cap,left);q[s]=take;left-=take
            if left<=1e-12:break
        mixtures.append(q)
    vals=[]
    for rho in mixtures:
        coeff={i:sum(rho[s]*inst.heads[i][s] for s in range(inst.S)) for i in ids}
        vals.append(structural_min(coeff))
    return {'structural_infeasible':False,'componentwise':b,'separate':cvar(b,inst.alpha),
            'mixture':max(vals),'mixture_values':vals,'mixtures':mixtures}


def enumerate_oracle(inst,prefix=None,objective='feasibility',ignore_risk=False,state_limit=None):
    best=None; bestmet=None; seen=0; exhausted=True
    for ranking in structural_rankings(inst,prefix):
        if state_limit is not None and seen>=state_limit:
            exhausted=False;break
        seen+=1; m=verify(inst,ranking,ignore_risk)
        if not m['feasible']: continue
        value=m['risk'] if objective=='risk' else -m['objective']
        if best is None or value<bestmet[0]-1e-12:
            best=ranking;bestmet=(value,m)
        if objective=='feasibility':
            return {'status':'FEASIBLE','ranking':best,'metrics':m,'optimal':False,'states':seen}
    return {'status':'FEASIBLE' if best is not None else ('INFEASIBLE' if exhausted else 'UNKNOWN'),
            'ranking':best,'metrics':None if bestmet is None else bestmet[1],'optimal':exhausted and best is not None,'states':seen}


def candidate_priority(inst,prefix,u,r,i):
    selected=[item for (user,_),item in prefix.items() if user==u]
    covered=set().union(*(set(inst.genres[item]) for item in selected)) if selected else set()
    universe=max(1,len(set().union(*(set(v) for v in inst.genres.values()))))
    return inst.weights[r]*inst.scores[u][i]/inst.denominator+inst.diversity_weight*len(set(inst.genres[i])-covered)/(inst.B*universe)


def wcr(inst,max_checks=None,state_limit=None,oracle=None):
    initial_lb=lower_bounds(inst)
    if initial_lb['structural_infeasible'] or initial_lb['mixture']>inst.theta+TOL:
        return {'status':'INFEASIBLE','ranking':None,'reason':'MIXTURE_BOUND',
                'lower_bound':initial_lb['mixture'],'fallback_slots':0,'oracle_calls':0}
    backend=oracle or (lambda p:enumerate_oracle(inst,prefix=p,state_limit=state_limit))
    initial=backend({})
    if initial['status']!='FEASIBLE': return {**initial,'fallback_slots':0,'oracle_calls':1}
    witness=initial['ranking']
    if not verify(inst,witness)['feasible']: raise ValueError('Invalid initial witness')
    prefix={};checks=0;fallbacks=0;pruned=0;trace=[]
    for u in range(inst.B):
        for r in range(inst.K):
            used={i for (v,_),i in prefix.items() if v==u}
            chosen=None
            for i in sorted((i for i in inst.candidates[u] if i not in used),key=lambda i:(-candidate_priority(inst,prefix,u,r,i),i)):
                if max_checks is not None and checks>=max_checks: break
                trial={**prefix,(u,r):i};checks+=1
                lb=lower_bounds(inst,trial)
                if lb['structural_infeasible'] or lb['mixture']>inst.theta+TOL:
                    pruned+=1; trace.append({'user':u,'rank':r,'item':i,'outcome':'BOUND_REJECT','bound':lb['mixture']});continue
                result=backend(trial)
                trace.append({'user':u,'rank':r,'item':i,'outcome':result['status']})
                if result['status']=='FEASIBLE':
                    candidate=result['ranking']
                    if not verify(inst,candidate)['feasible'] or any(candidate[v][j]!=x for (v,j),x in trial.items()):
                        raise ValueError('Oracle returned invalid completion')
                    witness=candidate;chosen=i;break
            if chosen is None: chosen=witness[u][r];fallbacks+=1
            prefix[(u,r)]=chosen
    ranking=tuple(tuple(prefix[(u,r)] for r in range(inst.K)) for u in range(inst.B))
    assert verify(inst,ranking)['feasible']
    return {'status':'FEASIBLE','ranking':ranking,'metrics':verify(inst,ranking),'optimal':False,
            'fallback_slots':fallbacks,'candidate_checks':checks,'bound_rejections':pruned,
            'oracle_calls':1+sum(t['outcome']!='BOUND_REJECT' for t in trace),'trace':trace}


def milp_oracle(inst,**kwargs):
    from milp_backend import solve
    return solve(inst,**kwargs)
