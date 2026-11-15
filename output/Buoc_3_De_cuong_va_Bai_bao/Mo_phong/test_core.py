import itertools
import math
import random
import unittest
import core


class ResearchChecks(unittest.TestCase):
    def require(self, name):
        self.assertTrue(hasattr(core, name), 'Missing required behavior: '+name)
        return getattr(core, name)

    def blocked_greedy(self):
        I=self.require('Instance')
        return I(candidates=((0,1),(0,)), scores=({0:.9,1:.8},{0:1.}),
                 genres={0:('g',),1:('g',)}, heads={0:(1,1,1,1),1:(0,0,0,0)},
                 weights=(1.,), epsilon=.2, diversity=(1,1), alpha=.5, theta=.5)

    def coupled(self, theta=.4):
        I=self.require('Instance')
        return I(candidates=((0,1),),scores=({0:1.,1:1.},),
                 genres={0:('g',),1:('g',)},heads={0:(1,0),1:(0,1)},
                 weights=(1.,),epsilon=0.,diversity=(1,),alpha=.5,theta=theta)

    def test_fractional_tail_and_endpoint_cvar(self):
        cvar=self.require('cvar')
        self.assertAlmostEqual(cvar([1,.2,0,0],.5),.6)
        self.assertAlmostEqual(cvar([1,.2,0,0],0),.3)
        self.assertAlmostEqual(cvar([1,0,0,0,0],.7),2/3)
        self.assertAlmostEqual(cvar([1,.2,0,0],.9),1)

    def test_cvar_dual_envelope_matches_atom_calculation(self):
        dual=self.require('tail_weights'); cvar=self.require('cvar')
        values=[.1,.9,.4,.3,.5]; alpha=.37
        rho=dual(values,alpha)
        self.assertAlmostEqual(sum(rho),1)
        self.assertLessEqual(max(rho),1/((1-alpha)*len(values))+1e-12)
        self.assertAlmostEqual(sum(q*h for q,h in zip(rho,values)),cvar(values,alpha))

    def test_local_greedy_budget_can_destroy_completion(self):
        verify=self.require('verify'); oracle=self.require('enumerate_oracle')
        inst=self.blocked_greedy()
        self.assertFalse(verify(inst,((0,),(0,)))['feasible'])
        self.assertTrue(verify(inst,((1,),(0,)))['feasible'])
        self.assertEqual(oracle(inst,prefix={(0,0):0})['status'],'INFEASIBLE')
        self.assertEqual(oracle(inst,prefix={(0,0):1})['status'],'FEASIBLE')

    def test_position_weighted_exposure_distinguishes_order(self):
        I=self.require('Instance'); verify=self.require('verify')
        inst=I(candidates=((0,1),),scores=({0:1.,1:.9},),
               genres={0:('a',),1:('b',)},heads={0:(1,1),1:(0,0)},
               weights=(2.,1.),epsilon=.1,diversity=(2,),alpha=.5,theta=1/3)
        self.assertFalse(verify(inst,((0,1),))['feasible'])
        r=verify(inst,((1,0),))
        self.assertTrue(r['feasible']); self.assertAlmostEqual(r['risk'],1/3)

    def test_mixture_bound_catches_joint_scenario_support(self):
        lower=self.require('lower_bounds')
        lb=lower(self.coupled())
        self.assertEqual(lb['separate'],0)
        self.assertAlmostEqual(lb['mixture'],.5)
        self.assertGreater(lb['mixture'],.4)

    def test_small_bound_is_not_positive_feasibility_certificate(self):
        lower=self.require('lower_bounds'); oracle=self.require('enumerate_oracle')
        inst=self.coupled(.75)
        self.assertLess(lower(inst)['mixture'],inst.theta)
        self.assertEqual(oracle(inst)['status'],'INFEASIBLE')
        ref=oracle(inst,objective='risk',ignore_risk=True)
        self.assertAlmostEqual(ref['metrics']['risk'],1)

    def test_lower_bounds_valid_on_random_residual_assignments(self):
        lower=self.require('lower_bounds'); exposure=self.require('exposure')
        cvar=self.require('cvar'); I=self.require('Instance')
        rng=random.Random(109)
        for trial in range(12):
            heads={i:tuple(rng.randrange(2) for _ in range(4)) for i in range(4)}
            inst=I(candidates=((0,1,2),(1,2,3)),scores=({i:1. for i in (0,1,2)},{i:1. for i in (1,2,3)}),
                   genres={i:('g',) for i in range(4)},heads=heads,weights=(2.,1.),
                   epsilon=0,diversity=(1,1),alpha=.35,theta=1)
            prefix={(0,0):trial%3}
            rankings=[r for r in itertools.product(*(itertools.permutations(c,2) for c in inst.candidates)) if r[0][0]==prefix[(0,0)]]
            truth=min(cvar(exposure(inst,r),inst.alpha) for r in rankings)
            lb=lower(inst,prefix)
            self.assertLessEqual(lb['separate'],lb['mixture']+1e-10)
            self.assertLessEqual(lb['mixture'],truth+1e-10)

    def test_witness_fallback_with_no_extra_checks_remains_feasible(self):
        wcr=self.require('wcr'); verify=self.require('verify')
        inst=self.blocked_greedy()
        out=wcr(inst,max_checks=0)
        self.assertEqual(out['status'],'FEASIBLE')
        self.assertTrue(verify(inst,out['ranking'])['feasible'])
        self.assertEqual(out['fallback_slots'],2)

    def test_unknown_without_initial_witness_is_not_infeasible(self):
        wcr=self.require('wcr')
        out=wcr(self.blocked_greedy(),state_limit=0)
        self.assertEqual(out['status'],'UNKNOWN')
        self.assertIsNone(out.get('ranking'))

    def test_milp_agrees_with_exhaustive_risk_optimum(self):
        milp=self.require('milp_oracle'); enum=self.require('enumerate_oracle')
        for inst in [self.blocked_greedy(),self.coupled(1)]:
            a=enum(inst,objective='risk',ignore_risk=True)
            b=milp(inst,objective='risk',ignore_risk=True,time_limit=8)
            self.assertEqual(b['status'],'FEASIBLE')
            self.assertTrue(b['optimal'])
            self.assertAlmostEqual(a['metrics']['risk'],b['metrics']['risk'],places=7)

    def test_milp_cannot_invent_missing_categories(self):
        milp=self.require('milp_oracle'); I=self.require('Instance')
        inst=I(candidates=((0,1),),scores=({0:1.,1:1.},),genres={0:('g',),1:('g',)},
               heads={0:(0,0),1:(0,0)},weights=(2.,1.),epsilon=0,diversity=(2,),alpha=.5,theta=1)
        self.assertEqual(milp(inst,time_limit=8)['status'],'INFEASIBLE')

    def test_initial_bound_proves_infeasibility_without_oracle_search(self):
        wcr=self.require('wcr')
        out=wcr(self.coupled(.4),state_limit=0)
        self.assertEqual(out['status'],'INFEASIBLE')
        self.assertEqual(out.get('reason'),'MIXTURE_BOUND')
        self.assertEqual(out['oracle_calls'],0)

    def test_priority_uses_incremental_category_gain(self):
        priority=self.require('candidate_priority'); I=self.require('Instance')
        inst=I(candidates=((0,1,2),),scores=({0:.9,1:.8,2:.79},),
               genres={0:('a',),1:('a',),2:('b',)},heads={i:(0,0) for i in range(3)},
               weights=(2.,1.),epsilon=.5,diversity=(1,),alpha=.5,theta=1,diversity_weight=1)
        self.assertGreater(priority(inst,{(0,0):0},0,1,2),priority(inst,{(0,0):0},0,1,1))


if __name__=='__main__':
    unittest.main(verbosity=2)
