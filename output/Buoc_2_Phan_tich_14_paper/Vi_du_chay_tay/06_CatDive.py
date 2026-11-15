"""Pedagogical coverage-first with ONE shared histogram; not repo exact code."""
from collections import Counter
from itertools import combinations
from math import log, log2

items = [("A", 1, .95), ("B", 1, .93), ("C", 1, .90),
         ("D", 2, .88), ("E", 2, .86), ("F", 3, .80)]

def metrics(chosen, target):
    pairs = list(combinations(chosen, 2))
    ild = sum(a[1] != b[1] for a, b in pairs) / len(pairs)
    cov = len({x[1] for x in chosen}) / 3
    ids = [x[0] for x in chosen]
    hit = int(target in ids)
    ndcg = 1 / log2(ids.index(target) + 2) if hit else 0
    return hit, ndcg, ild, cov

if __name__ == "__main__":
    pref, conf = [.4, .4, .1, .1], [.5, .1, .3, .1]
    weights = [p + .5 * c for p, c in zip(pref, conf)]
    probs = [x / sum(weights) for x in weights]
    print("negative_sampling_probabilities=", [round(x, 6) for x in probs])
    k, coverage_weight, penalty_weight = 3, .4, .4
    freq = Counter(x[1] for x in items)
    rare = sorted(freq, key=lambda c: (freq[c], c))[:int(k * coverage_weight)]
    chosen = [max((x for x in items if x[1] == c), key=lambda x: x[2]) for c in rare]
    histogram = Counter(x[1] for x in chosen)
    print("coverage_first=", [x[0] for x in chosen])
    while len(chosen) < k:
        remaining = [x for x in items if x not in chosen]
        scores = {x[0]: x[2] - penalty_weight * log(1 + histogram[x[1]]) for x in remaining}
        best = max(remaining, key=lambda x: scores[x[0]])
        print("adjusted=", {a: round(b, 6) for a, b in scores.items()}, "choose=", best[0])
        chosen.append(best)
        histogram[best[1]] += 1
    chosen.sort(key=lambda x: x[2], reverse=True)
    print("final=", [x[0] for x in chosen], "score=", round(sum(x[2] for x in chosen), 2))
    for name, ranking in [("baseline", items[:3]), ("pedagogical_rerank", chosen)]:
        print(name, "HR,NDCG,ILD,category_cov=", tuple(round(x, 6) for x in metrics(ranking, "D")))
    assert [x[0] for x in chosen] == ["A", "D", "F"]
    assert metrics(chosen, "D")[2:] == (1.0, 1.0)
