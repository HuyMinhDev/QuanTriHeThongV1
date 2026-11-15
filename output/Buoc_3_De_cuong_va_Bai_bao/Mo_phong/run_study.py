"""Deterministic finite-instance validation; no real-data effectiveness claims.

Writes only ../Kiem_tra/simulation_results.json and simulation_results.csv.
The randomly generated binary scenario coefficients are synthetic, not
bootstrap estimates of item popularity from MovieLens or Amazon.
"""
from __future__ import annotations

import csv
from dataclasses import asdict, replace
import hashlib
import itertools
import json
import math
from pathlib import Path
import platform
import random
import sys

import scipy

import core
from milp_backend import solve


SEED = 20261115
N_INSTANCES = 40
CHECK_TOL = 1e-7
HERE = Path(__file__).resolve().parent
OUTPUT = HERE.parent / 'Kiem_tra'


def require(condition, message):
    if not condition:
        raise AssertionError(message)


def close(a, b, message):
    require(math.isfinite(a) and math.isfinite(b), message + ': nonfinite value')
    require(abs(a-b) <= CHECK_TOL, f'{message}: {a} != {b}')


def hinge_cvar(values, alpha):
    """Independent scalar check via all hinge breakpoints, not tail sorting."""
    return min(t + sum(max(h-t, 0.) for h in values) /
               ((1-alpha)*len(values)) for t in {0., 1., *values})


def checked_risk(inst, ranking):
    exposures = core.exposure(inst, ranking)
    value = hinge_cvar(exposures, inst.alpha)
    close(value, core.cvar(exposures, inst.alpha), 'hinge/tail CVaR agreement')
    return value


def prefix_record(prefix):
    return [{'user': u, 'rank': r, 'item': i}
            for (u, r), i in sorted(prefix.items())]


def generated_instance(rng):
    candidates = ((0, 1, 2), (1, 2, 3))
    scores = tuple({i: round(rng.uniform(.2, 1.), 4) for i in row}
                   for row in candidates)
    genres = {}
    for i in range(4):
        labels = {f'g{rng.randrange(3)}'}
        if rng.random() < .3:
            labels.add(f'g{rng.randrange(3)}')
        genres[i] = tuple(sorted(labels))
    heads = {i: tuple(rng.randrange(2) for _ in range(4)) for i in range(4)}
    return core.Instance(
        candidates=candidates, scores=scores, genres=genres, heads=heads,
        weights=(2., 1.), epsilon=rng.choice((.3, .6)), diversity=(1, 1),
        alpha=rng.choice((0., .35, .5, .75, .9)),
        theta=rng.choice((.25, .5, .75, 1.)))


def prefixes(inst):
    """Includes noncontiguous fixed positions and one fully fixed leaf."""
    c0, c1 = inst.candidates
    leaf = core.baseline(inst)
    return [
        {},
        {(0, 0): c0[0]},
        {(1, 1): c1[-1]},
        {(0, 1): c0[1], (1, 0): c1[0]},
        {(0, 0): c0[0], (0, 1): c0[2], (1, 1): c1[1]},
        {(u, r): leaf[u][r] for u in range(inst.B) for r in range(inst.K)},
    ]


def validate_bounds(inst, prefix):
    completions = list(core.structural_rankings(inst, prefix))
    require(bool(completions), 'test prefix unexpectedly structurally infeasible')
    truth = min(checked_risk(inst, row) for row in completions)
    bounds = core.lower_bounds(inst, prefix)
    require(not bounds['structural_infeasible'], 'bound rejected valid structural prefix')
    sep, mix = bounds['separate'], bounds['mixture']
    require(sep <= mix + CHECK_TOL, f'LB_sep > LB_mix: {sep}, {mix}')
    require(mix <= truth + CHECK_TOL, f'LB_mix > structural optimum: {mix}, {truth}')
    cap = 1/((1-inst.alpha)*inst.S)
    for q in bounds['mixtures']:
        close(sum(q), 1., 'dual mixture must sum to one')
        require(min(q) >= -CHECK_TOL and max(q) <= cap+CHECK_TOL,
                'mixture outside empirical CVaR dual envelope')
        exact_linear_min = min(sum(a*h for a, h in zip(q, core.exposure(inst, row)))
                               for row in completions)
        expected = bounds['mixture_values'][bounds['mixtures'].index(q)]
        close(exact_linear_min, expected, 'sorting closed form vs enumeration')
    if len(prefix) == inst.B*inst.K:
        close(mix, truth, 'full-prefix risk bound must be exact')
    return {'prefix': prefix_record(prefix), 'structural_completions': len(completions),
            'structural_minimum_risk': truth, 'bound_separate': sep,
            'bound_mixture': mix, 'mixture_strictly_improves': mix > sep+CHECK_TOL,
            'separate_rejects_at_theta': sep > inst.theta+CHECK_TOL,
            'mixture_rejects_at_theta': mix > inst.theta+CHECK_TOL,
            'componentwise_minima': bounds['componentwise'],
            'mixtures': bounds['mixtures'], 'mixture_values': bounds['mixture_values']}


def validate_instance(inst, index):
    residuals = [validate_bounds(inst, p) for p in prefixes(inst)]
    root = residuals[0]
    enum_risk = core.enumerate_oracle(inst, objective='risk', ignore_risk=True)
    require(enum_risk['status'] == 'FEASIBLE' and enum_risk['optimal'],
            'baseline guarantees score/coverage feasibility in generated study')
    truth = enum_risk['metrics']['risk']
    require(root['structural_minimum_risk'] <= truth+CHECK_TOL,
            'score-constrained optimum below structural relaxation')

    integer = solve(inst, objective='risk', ignore_risk=True, time_limit=8)
    require(integer['status'] == 'FEASIBLE' and integer['optimal'],
            f'MILP did not certify optimum for instance {index}: {integer}')
    close(integer['metrics']['risk'], truth, f'enumeration/MILP risk instance {index}')

    relaxation = solve(inst, objective='risk', ignore_risk=True,
                       relax_integrality=True, time_limit=8)
    require(relaxation['status'] == 'RELAXATION' and relaxation['optimal'],
            f'LP did not certify optimum for instance {index}')
    lp_value = relaxation['objective']
    require(root['bound_mixture'] <= lp_value+CHECK_TOL,
            f'mixture bound exceeded LP relaxation for instance {index}')
    require(lp_value <= truth+CHECK_TOL,
            f'LP relaxation exceeded integer optimum for instance {index}')

    exact_feasibility = core.enumerate_oracle(inst)
    expected_status = exact_feasibility['status']
    require(expected_status in ('FEASIBLE', 'INFEASIBLE'), 'unlimited enumeration returned unknown')
    standard = core.wcr(inst)
    fallback = core.wcr(inst, max_checks=0)
    for variant, answer in [('standard', standard), ('forced_fallback', fallback)]:
        require(answer['status'] == expected_status,
                f'WCR {variant} feasibility disagreement on instance {index}')
        if expected_status == 'FEASIBLE':
            require(core.verify(inst, answer['ranking'])['feasible'],
                    f'WCR {variant} returned invalid witness')
        else:
            require(answer.get('ranking') is None, 'infeasible result contained ranking')
    if expected_status == 'FEASIBLE':
        require(fallback['fallback_slots'] == inst.B*inst.K,
                'zero candidate-check budget did not use witness fallback for every slot')

    return {'instance_id': index, 'instance': asdict(inst), 'prefix_checks': residuals,
            'minimum_risk_without_risk_budget': truth,
            'minimum_risk_scope': 'structure + score floors + coverage; risk budget omitted',
            'lp_relaxation_minimum_risk': lp_value,
            'milp_minimum_risk': integer['metrics']['risk'],
            'milp_evidence': integer['evidence'], 'lp_evidence': relaxation['evidence'],
            'exact_feasibility': exact_feasibility,
            'wcr': standard, 'wcr_forced_fallback': fallback}


def blocked_instance():
    return core.Instance(
        candidates=((0, 1), (0,)), scores=({0: .9, 1: .8}, {0: 1.}),
        genres={0: ('g',), 1: ('g',)},
        heads={0: (1, 1, 1, 1), 1: (0, 0, 0, 0)}, weights=(1.,),
        epsilon=.2, diversity=(1, 1), alpha=.5, theta=.5)


def partial_budget_greedy(inst):
    """Named counterexample only: score-first, checks current risk, no completion oracle."""
    prefix = {}
    trace = []
    for u in range(inst.B):
        for r in range(inst.K):
            used = {i for (v, _), i in prefix.items() if v == u}
            accepted = False
            for i in sorted(set(inst.candidates[u])-used,
                            key=lambda i: (-inst.weights[r]*inst.scores[u][i], i)):
                trial = {**prefix, (u, r): i}
                exposure = [sum(inst.weights[j]*inst.heads[item][s]
                                for (v, j), item in trial.items())/inst.denominator
                            for s in range(inst.S)]
                risk = hinge_cvar(exposure, inst.alpha)
                permitted = risk <= inst.theta+core.TOL
                trace.append({'user': u, 'rank': r, 'item': i,
                              'partial_risk_full_denominator': risk,
                              'current_budget_passes': permitted})
                if permitted:
                    prefix = trial
                    accepted = True
                    break
            if not accepted:
                return {'status': 'BLOCKED', 'prefix': prefix_record(prefix), 'trace': trace}
    ranking = tuple(tuple(prefix[u, r] for r in range(inst.K)) for u in range(inst.B))
    return {'status': 'COMPLETED', 'ranking': ranking, 'trace': trace,
            'metrics': core.verify(inst, ranking)}


def named_examples():
    blocked = blocked_instance()
    naive = partial_budget_greedy(blocked)
    require(naive['status'] == 'BLOCKED', 'named score-first greedy should block')
    good = ((1,), (0,))
    require(core.verify(blocked, good)['feasible'], 'blocked-greedy alternative invalid')
    require(core.enumerate_oracle(blocked, prefix={(0, 0): 0})['status'] == 'INFEASIBLE',
            'bad first choice unexpectedly has a completion')
    blocked_wcr = core.wcr(blocked)
    require(blocked_wcr['status'] == 'FEASIBLE', 'WCR failed named blocked case')

    weighted = core.Instance(
        candidates=((0, 1),), scores=({0: 1., 1: .9},),
        genres={0: ('a',), 1: ('b',)}, heads={0: (1, 1), 1: (0, 0)},
        weights=(2., 1.), epsilon=.1, diversity=(2,), alpha=.5, theta=1/3)
    bad_metrics = core.verify(weighted, ((0, 1),))
    good_metrics = core.verify(weighted, ((1, 0),))
    require(not bad_metrics['feasible'] and good_metrics['feasible'], 'weighted order example failed')
    close(bad_metrics['risk'], 2/3, 'weighted bad order')
    close(good_metrics['risk'], 1/3, 'weighted good order')

    coupled = core.Instance(
        candidates=((0, 1),), scores=({0: 1., 1: 1.},),
        genres={0: ('g',), 1: ('g',)}, heads={0: (1, 0), 1: (0, 1)},
        weights=(1.,), epsilon=0., diversity=(1,), alpha=.5, theta=.4)
    coupled_rows = []
    for theta in (.4, .75):
        inst = replace(coupled, theta=theta)
        bounds = core.lower_bounds(inst)
        truth = core.enumerate_oracle(inst, objective='risk', ignore_risk=True)
        lp = solve(inst, objective='risk', ignore_risk=True, relax_integrality=True)
        close(bounds['separate'], 0., 'coupled separate lower bound')
        close(bounds['mixture'], .5, 'coupled mixture lower bound')
        close(truth['metrics']['risk'], 1., 'coupled integral risk optimum')
        require(lp['optimal'], 'coupled LP not optimal')
        close(lp['objective'], .5, 'coupled LP relaxation risk')
        answer = core.wcr(inst)
        require(answer['status'] == 'INFEASIBLE', 'coupled instance should be infeasible')
        if theta == .4:
            require(answer.get('reason') == 'MIXTURE_BOUND' and answer['oracle_calls'] == 0,
                    'strong bound did not reject coupled theta=.4')
        else:
            require(bounds['mixture'] < theta and answer['oracle_calls'] == 1,
                    'coupled theta=.75 should require the exact oracle')
        coupled_rows.append({'theta': theta, 'bounds': bounds, 'minimum_integral_risk': 1.,
                             'lp_relaxation_risk': lp['objective'], 'wcr': answer})

    no_initial = core.wcr(blocked, state_limit=0)
    require(no_initial['status'] == 'UNKNOWN' and no_initial.get('ranking') is None,
            'unknown initial oracle mislabeled infeasible')

    def unknown_after_initial(prefix):
        if not prefix:
            return core.enumerate_oracle(blocked)
        return {'status': 'UNKNOWN', 'ranking': None, 'reason': 'injected unresolved completion query'}

    with_initial = core.wcr(blocked, oracle=unknown_after_initial)
    require(with_initial['status'] == 'FEASIBLE' and
            core.verify(blocked, with_initial['ranking'])['feasible'],
            'unknown residual oracle did not preserve known witness')
    require(with_initial['fallback_slots'] == blocked.B*blocked.K,
            'expected witness fallback on both named slots')

    return {'blocked_greedy': {'instance': asdict(blocked), 'naive_partial_greedy': naive,
                              'feasible_alternative': good,
                              'alternative_metrics': core.verify(blocked, good),
                              'wcr': blocked_wcr},
            'weighted_order': {'instance': asdict(weighted), 'bad_order': ((0, 1),),
                               'bad_metrics': bad_metrics, 'good_order': ((1, 0),),
                               'good_metrics': good_metrics, 'wcr': core.wcr(weighted)},
            'coupled_head_labels': {'instance': asdict(coupled), 'threshold_cases': coupled_rows,
                                    'interpretation': 'finite-mixture bound is not a positive feasibility certificate; integrality gap remains'},
            'unknown_status_cases': {'without_initial_witness': no_initial,
                                     'unknown_residual_queries_with_witness': with_initial}}


def clean_json(value):
    if isinstance(value, dict):
        return {str(k): clean_json(v) for k, v in value.items()}
    if isinstance(value, (list, tuple)):
        return [clean_json(v) for v in value]
    if isinstance(value, float):
        return value if math.isfinite(value) else None
    if hasattr(value, 'item'):
        return clean_json(value.item())
    return value


def file_hash(name):
    return hashlib.sha256((HERE/name).read_bytes()).hexdigest()


def main():
    hashes = {name: file_hash(name) for name in ('core.py', 'milp_backend.py', 'run_study.py')}
    rng = random.Random(SEED)
    records = [validate_instance(generated_instance(rng), j+1) for j in range(N_INSTANCES)]
    examples = named_examples()
    residuals = [p for row in records for p in row['prefix_checks']]
    roots = [row['prefix_checks'][0] for row in records]
    summary = {
        'instances': len(records), 'prefix_checks': len(residuals),
        'structural_completions_checked_across_prefixes': sum(p['structural_completions'] for p in residuals),
        'milp_integer_risk_comparisons': len(records), 'lp_relaxation_comparisons': len(records),
        'separate_to_mixture_strict_improvements_prefixes': sum(p['mixture_strictly_improves'] for p in residuals),
        'separate_to_mixture_strict_improvements_roots': sum(p['mixture_strictly_improves'] for p in roots),
        'separate_bound_rejectable_prefixes': sum(p['separate_rejects_at_theta'] for p in residuals),
        'mixture_bound_rejectable_prefixes': sum(p['mixture_rejects_at_theta'] for p in residuals),
        'additional_mixture_rejectable_prefixes': sum(p['mixture_rejects_at_theta'] and not p['separate_rejects_at_theta'] for p in residuals),
        'separate_bound_rejectable_roots': sum(p['separate_rejects_at_theta'] for p in roots),
        'mixture_bound_rejectable_roots': sum(p['mixture_rejects_at_theta'] for p in roots),
        'exact_feasible_instances': sum(row['exact_feasibility']['status'] == 'FEASIBLE' for row in records),
        'exact_infeasible_instances': sum(row['exact_feasibility']['status'] == 'INFEASIBLE' for row in records),
        'wcr_exact_status_agreements': sum(row['wcr']['status'] == row['exact_feasibility']['status'] for row in records),
        'forced_fallback_status_agreements': sum(row['wcr_forced_fallback']['status'] == row['exact_feasibility']['status'] for row in records),
        'maximum_milp_enumeration_risk_error': max(abs(row['milp_minimum_risk']-row['minimum_risk_without_risk_budget']) for row in records),
        'assertion_failures': 0,
    }
    require(summary['wcr_exact_status_agreements'] == N_INSTANCES, 'incomplete status agreement')
    for name, value in hashes.items():
        require(file_hash(name) == value, f'{name} changed during the study')
    payload = clean_json({
        'metadata': {'seed': SEED, 'instance_count': N_INSTANCES,
                     'scope': 'finite synthetic mathematical/prototype validation only',
                     'scenario_generation': 'independent synthetic binary coefficients; not real-data bootstrap labels',
                     'dimensions': {'B': 2, 'candidates_per_user': 3, 'K': 2, 'S': 4},
                     'epsilon_choices': [.3, .6], 'theta_choices': [.25, .5, .75, 1.],
                     'alpha_choices': [0., .35, .5, .75, .9], 'rank_weights': [2., 1.],
                     'genre_floor_per_user': 1, 'comparison_tolerance': CHECK_TOL,
                     'python': sys.version, 'scipy': scipy.__version__, 'platform': platform.platform(),
                     'source_sha256': hashes,
                     'limitations': ['No real datasets, training, held-out accuracy, or latency benchmark.',
                                     'Forty finite instances cannot establish distribution-wide superiority.',
                                     'LP/MILP results are numerical solver evidence; primal assignments are independently checked.',
                                     'Bound-rejectable prefix counts describe this tested collection, not measured speedups.']},
        'summary': summary, 'named_examples': examples, 'instances': records})
    OUTPUT.mkdir(parents=True, exist_ok=True)
    json_path = OUTPUT/'simulation_results.json'
    json_path.write_text(json.dumps(payload, ensure_ascii=False, indent=2, allow_nan=False)+'\n', encoding='utf-8')
    csv_path = OUTPUT/'simulation_results.csv'
    fields = ['instance_id', 'epsilon', 'alpha', 'theta', 'bound_separate', 'bound_mixture',
              'structural_minimum_risk', 'lp_relaxation_minimum_risk', 'integer_minimum_risk',
              'milp_minimum_risk', 'exact_status', 'wcr_status', 'wcr_fallback_status',
              'root_mixture_strict', 'prefix_mixture_strict_count', 'prefix_mixture_rejectable_count',
              'wcr_candidate_checks', 'wcr_bound_rejections', 'wcr_fallback_slots', 'wcr_oracle_calls']
    with csv_path.open('w', newline='', encoding='utf-8') as handle:
        writer = csv.DictWriter(handle, fieldnames=fields)
        writer.writeheader()
        for row in records:
            inst = row['instance']; root = row['prefix_checks'][0]; out = row['wcr']
            writer.writerow({
                'instance_id': row['instance_id'], 'epsilon': inst['epsilon'],
                'alpha': inst['alpha'], 'theta': inst['theta'],
                'bound_separate': root['bound_separate'], 'bound_mixture': root['bound_mixture'],
                'structural_minimum_risk': root['structural_minimum_risk'],
                'lp_relaxation_minimum_risk': row['lp_relaxation_minimum_risk'],
                'integer_minimum_risk': row['minimum_risk_without_risk_budget'],
                'milp_minimum_risk': row['milp_minimum_risk'],
                'exact_status': row['exact_feasibility']['status'], 'wcr_status': out['status'],
                'wcr_fallback_status': row['wcr_forced_fallback']['status'],
                'root_mixture_strict': root['mixture_strictly_improves'],
                'prefix_mixture_strict_count': sum(p['mixture_strictly_improves'] for p in row['prefix_checks']),
                'prefix_mixture_rejectable_count': sum(p['mixture_rejects_at_theta'] for p in row['prefix_checks']),
                'wcr_candidate_checks': out.get('candidate_checks', 0),
                'wcr_bound_rejections': out.get('bound_rejections', 0),
                'wcr_fallback_slots': out['fallback_slots'], 'wcr_oracle_calls': out['oracle_calls']})
    # Confirm serialized artifacts round-trip without nonstandard numeric tokens.
    loaded = json.loads(json_path.read_text(encoding='utf-8'),
                        parse_constant=lambda token: (_ for _ in ()).throw(ValueError(token)))
    require(loaded['summary'] == summary, 'JSON round-trip mismatch')
    with csv_path.open(newline='', encoding='utf-8') as handle:
        require(len(list(csv.DictReader(handle))) == N_INSTANCES, 'CSV row count mismatch')
    print(json.dumps(summary, ensure_ascii=False, allow_nan=False))


if __name__ == '__main__':
    main()
