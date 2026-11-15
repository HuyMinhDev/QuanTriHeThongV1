"""Original teaching calculations, not the authors' experimental program."""
from itertools import combinations
from math import isclose


def cvar(losses, probabilities, beta):
    assert 0 < beta <= 1 and isclose(sum(probabilities), 1)
    mass, weighted_loss = beta, 0.0
    for loss, probability in sorted(zip(losses, probabilities), reverse=True):
        take = min(mass, probability)
        weighted_loss += take * loss
        mass -= take
        if mass <= 1e-12:
            break
    return weighted_loss / beta


def intent_values(ranking):
    # Table 1(a)'s labels; denominator remains the final K=2 (zero padding).
    values = {"d1": (1., 0.), "d2": (1., 0.),
              "d3": (0., 1.), "d4": (0., 1.)}
    return [sum(values[d][c] for d in ranking) / 2 for c in range(2)]


if __name__ == "__main__":
    p, beta = [0.51, 0.49], 0.5
    for ranking in [("d1", "d2"), ("d1", "d3"), ("d3", "d4")]:
        values = intent_values(ranking)
        risk = cvar([1-v for v in values], p, beta)
        mean = sum(a*b for a, b in zip(values, p))
        print(ranking, "values=", values, "mean=", round(mean, 6),
              "CVaR=", round(risk, 6))
    chosen = []
    for step in range(2):
        trials = []
        for item in ["d1", "d2", "d3", "d4"]:
            if item in chosen:
                continue
            values = intent_values(chosen+[item])
            risk = cvar([1-v for v in values], p, beta)
            mean = sum(a*b for a, b in zip(values, p))
            trials.append((risk, -mean, item))
        risk, negative_mean, item = min(trials)
        chosen.append(item)
        print("step", step+1, "choose", item, "risk", round(risk, 6))
    assert chosen == ["d1", "d3"]
    assert isclose(cvar([1., 0.], [.1, .9], .2), .5)
    print("atom_boundary: exact_CVaR=0.5; whole_atom_tail_mean=0.1")
    # Version-specific check of a generic submodularity assertion.
    # V_c(S)=sum relevance/2, target=.5, equiprobable intents, beta=.5.
    docs = {"A": (1., 0.), "B": (0., 1.)}
    def risk_s(items):
        values = [sum(docs[d][c] for d in items)/2 for c in range(2)]
        return cvar([max(0., .5-v) for v in values], [.5, .5], .5)
    empty = risk_s([])
    phi = {name: empty-risk_s(items) for name, items in
           [("empty", []), ("A", ["A"]), ("B", ["B"]), ("AB", ["A", "B"]) ]}
    assert phi == {"empty": 0., "A": 0., "B": 0., "AB": .5}
    assert phi["A"]+phi["B"] < phi["AB"]+phi["empty"]
    print("submodularity_check", phi)
    print("All teaching checks passed.")
