"""Toy su pham doc lap; khong phai code hoac reproduction cua tac gia."""
from itertools import combinations

items = {"A": (0.95, False), "B": (0.93, False),
         "C": (0.88, True), "D": (0.80, True)}

def objective(chosen, weight):
    score = sum(items[i][0] for i in chosen)
    share = sum(items[i][1] for i in chosen) / len(chosen)
    penalty = abs(share - 0.5)
    return (1 - weight) * score - weight * penalty

if __name__ == "__main__":
    for weight in (0.01, 0.1):
        candidates = list(combinations(items, 2))
        best = max(candidates, key=lambda c: objective(c, weight))
        print(f"lambda={weight:.2f}")
        for chosen in candidates:
            print(" ", "".join(chosen), f"objective={objective(chosen, weight):.4f}")
        print("best:", ",".join(best))
        assert best == (("A", "B") if weight == 0.01 else ("A", "C"))
    truth = [-1, -1, 1, 1, -1, 1, -1, 1]
    prediction = [-1, -1, 1, 1, -1, 1, 1, 1]
    fidelity = sum(a == b for a, b in zip(truth, prediction)) / len(truth)
    print(f"illustrative_fidelity={fidelity:.3f}")
    assert fidelity == 0.875
