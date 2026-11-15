"""Original pipeline/metric illustration, not FairDiverse implementation."""
from collections import Counter
from math import log

ITEMS = ("A", "B", "C", "D")
GROUP = {"A": "head", "B": "head", "C": "tail", "D": "tail"}
SCORES = [dict(A=.95, B=.90, C=.80, D=.20),
          dict(A=.93, B=.88, C=.40, D=.84),
          dict(A=.92, B=.87, C=.86, D=.10)]

def summary(lists):
    e = Counter(i for row in lists for i in row)
    counts = [e[i] for i in ITEMS]
    total = sum(counts)
    gini = sum(abs(a-b) for a in counts for b in counts) / (2*len(ITEMS)*total)
    group_counts = Counter()
    for i, c in e.items():
        group_counts[GROUP[i]] += c
    entropy = -sum((c/total)*log(c/total) for c in group_counts.values())
    utility = sum(SCORES[u][i] for u, row in enumerate(lists) for i in row)
    return utility, len(e)/len(ITEMS), gini, entropy

def main():
    baseline = [["A", "B"] for _ in range(3)]
    reranked = [["A", "C"], ["A", "D"], ["A", "C"]]
    for name, lists in [("baseline", baseline), ("reranked", reranked)]:
        utility, coverage, gini, entropy = summary(lists)
        print(name, f"utility={utility:.6f} coverage={coverage:.6f} gini={gini:.6f} group_entropy={entropy:.6f}")
    print("score_retention=", f"{summary(reranked)[0]/summary(baseline)[0]:.6f}", sep="")
    defaults = {"topk": [10], "model": "BPR"}
    model_config = {"model": "CPFair", "topk": [20]}
    user_config = {"topk": [2]}
    merged = defaults | model_config | user_config
    assert merged["topk"] == [2]
    print("config_precedence: topk=[2]")

if __name__ == "__main__":
    main()
