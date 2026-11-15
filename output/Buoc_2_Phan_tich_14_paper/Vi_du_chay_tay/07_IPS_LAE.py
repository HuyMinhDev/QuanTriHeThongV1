"""Original numerical derivation; no dataset download or official training."""
import numpy as np

def main():
    X = np.array([[1., 1., 0.], [1., 0., 1.], [1., 0., 0.], [0., 1., 0.]])
    ridge = 1.0
    G = X.T @ X + ridge * np.eye(3)
    P = np.linalg.inv(G)
    B = -P / np.diag(P)
    np.fill_diagonal(B, 0)
    counts = X.sum(axis=0)
    logs = np.log1p(counts)
    alpha = -(logs.min() + logs.max()) / 2  # beta = 1
    propensity = 1 / (1 + np.exp(-(alpha + logs)))
    weights = 1 / propensity
    weighted = B * weights
    independently_solved = np.zeros_like(B)
    for j in range(3):
        free = [i for i in range(3) if i != j]
        independently_solved[free, j] = np.linalg.solve(
            G[np.ix_(free, free)], (X.T @ X[:, j] * weights[j])[free])
    assert np.allclose(weighted, independently_solved)
    original_scores = np.array([1., 0., 0.]) @ B
    adjusted_scores = original_scores * weights
    np.set_printoptions(precision=6, suppress=True)
    print("counts", counts)
    print(f"alpha={alpha:.6f}")
    print("propensity", propensity)
    print("weights", weights)
    print("scores", original_scores)
    print("weighted_scores", adjusted_scores)
    print("unseen_order: B,C -> C,B")
    print("closed_form_matches_constrained_solve=True")

if __name__ == "__main__":
    main()
