"""Toy ADF: entropy, quota va counterexample rounding; no official training."""
from math import log2

def entropy(p):
    return -sum(x * log2(x) for x in p if x > 0) / log2(len(p))

if __name__ == "__main__":
    original = [0.6, 0.3, 0.1]
    mix = 0.3  # Chon de tinh tay; khong phai ket qua grid search cua paper.
    target = [(1 - mix) * x + mix / len(original) for x in original]
    quotas = [round(10 * x) for x in target]
    candidates = {
        "A": [0.99, 0.97, 0.95, 0.94, 0.92, 0.90],
        "B": [0.89, 0.87, 0.85, 0.80],
        "C": [0.83, 0.79, 0.70],
    }
    selected_score = sum(sum(scores[:n]) for scores, n in zip(candidates.values(), quotas))
    baseline_score = sum(sorted([s for group in candidates.values() for s in group], reverse=True)[:10])
    achieved = [q / sum(quotas) for q in quotas]
    print("P=", original)
    print("P_target=", [round(x, 4) for x in target])
    print(f"H(P)={entropy(original):.6f}; H(target)={entropy(target):.6f}")
    print("quotas=", quotas, "length=", sum(quotas))
    print("Q=", achieved, f"H(Q)={entropy(achieved):.6f}")
    print(f"score_selected={selected_score:.2f}; score_top10={baseline_score:.2f}")
    bad = [round(2 * x) for x in (0.5, 0.25, 0.25)]
    print("rounding_counterexample K=2:", bad, "length=", sum(bad))
    assert quotas == [5, 3, 2]
    assert abs(selected_score - 9.00) < 1e-10
    assert abs(baseline_score - 9.11) < 1e-10
    assert sum(bad) == 1
    desired = entropy(original) ** (1 - 0.4)
    grid = [(t / 20, [(1 - t / 20) * x + (t / 20) / 3 for x in original]) for t in range(21)]
    best_mix, best_p = min(grid, key=lambda row: abs(entropy(row[1]) - desired))
    grid_quotas = [round(10 * x) for x in best_p]
    print(f"alpha=0.4 beta=0; H_target={desired:.6f}; grid_mix={best_mix:.2f}")
    print("grid_P_target=", [round(x, 6) for x in best_p], "grid_quotas=", grid_quotas,
          "length=", sum(grid_quotas))
    assert best_mix == 0.2 and sum(grid_quotas) == 9
