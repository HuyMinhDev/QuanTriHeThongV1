"""Original teaching example; not author code or a full TORS replication."""
from itertools import permutations

ITEMS = ("A", "B", "C", "D")
RELEVANT = {"A", "B"}

def attention(rank, k, corrected):
    if rank > k:
        return 0.0
    return (k + 1 - rank) / k if corrected else (k - rank) / (k - 1)

def iaa_single(order, k, corrected):
    return sum(abs(attention(r, k, corrected) - (i in RELEVANT))
               for r, i in enumerate(order, 1)) / len(ITEMS)

def main():
    values = [iaa_single(p, 2, True) for p in permutations(ITEMS)]
    lo, hi = min(values), max(values)
    assert (lo, hi) == (0.125, 0.875)
    for order in [("A", "B", "C", "D"), ("A", "C", "B", "D"),
                  ("C", "D", "A", "B")]:
        old = iaa_single(order, 2, False)
        raw = iaa_single(order, 2, True)
        normalised = (raw - lo) / (hi - lo)
        print("".join(order), f"old={old:.6f} corrected_raw={raw:.6f} normalised={normalised:.6f}")
    print(f"enumerated=24 min={lo:.6f} max={hi:.6f}")
    try:
        attention(1, 1, False)
    except ZeroDivisionError:
        print("old_attention_k1=undefined; corrected_attention_k1=1.000000")
    assert attention(1, 1, True) == 1

if __name__ == "__main__":
    main()
