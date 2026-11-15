"""No API. Deterministic pedagogical ID repair, NOT paper's random-fill policy."""
from itertools import combinations
from math import log2

scores = dict(zip("ABCDEF", [.95, .93, .90, .88, .86, .80]))
genre = dict(zip("ABCDEF", ["Action"] * 3 + ["Romance"] * 2 + ["Documentary"]))

def ndcg(ranking, relevant):
    dcg = sum((i in relevant) / log2(r + 2) for r, i in enumerate(ranking))
    ideal = sum(1 / log2(r + 2) for r in range(min(len(relevant), len(ranking))))
    return dcg / ideal if ideal else 0

def ild(ranking):
    pairs = list(combinations(ranking, 2))
    return sum(genre[a] != genre[b] for a, b in pairs) / len(pairs)

if __name__ == "__main__":
    raw_ids, repaired, invalid = ["A", "D", "X", "A"], [], 0
    for item in raw_ids:
        if item in scores and item not in repaired:
            repaired.append(item)
        else:
            invalid += 1
    for item in sorted(scores, key=scores.get, reverse=True):
        if len(repaired) >= 3:
            break
        if item not in repaired:
            repaired.append(item)
    print("raw_ids=", raw_ids)
    print("invalid_count=", invalid, "invalid_fraction=", invalid / len(raw_ids))
    print("pedagogical_topscore_fill=", repaired)
    for ranking in [list("ABC"), repaired]:
        print("ranking=", ranking, f"score={sum(scores[x] for x in ranking):.2f}",
              f"ILD={ild(ranking):.6f}", f"NDCG(A,D)={ndcg(ranking, set('AD')):.6f}",
              f"NDCG(A,B)={ndcg(ranking, set('AB')):.6f}")
    assert repaired == ["A", "D", "B"]
    assert invalid == 2
    assert abs(ild(repaired) - 2/3) < 1e-10
    assert ndcg(repaired, set("AD")) == 1.0
