"""Own teaching code; Figure 1 coordinates cited, no Oracle2Fair replication."""
from itertools import product
from math import dist

def main():
    reference = (.766, .766)  # rounded illustration from paper Figure 1
    for name, point in [("A", (.2, .9)), ("B", (.65, .2)), ("C", (.5, .5))]:
        print(name, f"average={sum(point)/2:.6f} distance={dist(point, reference):.6f}")
    points = set()
    for chosen in product(range(3), repeat=2):
        rel = sum(i == 0 for i in chosen) / 2  # both users like A
        exposure = [chosen.count(i) for i in range(3)]
        gini = sum(abs(x-y) for x in exposure for y in exposure) / 12
        points.add((rel, 1-gini))
    frontier = [p for p in points if not any(
        q[0] >= p[0] and q[1] >= p[1] and q != p for q in points)]
    frontier.sort(reverse=True)
    for rel, fair in frontier:
        print(f"enumerated_frontier: relevance={rel:.6f} one_minus_gini={fair:.6f}")
    assert len(frontier) == 2
    assert frontier[0][0] == 1 and frontier[1][0] == .5
    print("all_assignments=9; exact_frontier_for_toy_only=True")

if __name__ == "__main__":
    main()
