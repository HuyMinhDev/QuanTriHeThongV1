"""Tự hiện thực toy theo các phép toán đã đọc; không sao chép repo tác giả."""
from math import log2

group = [0, 0, 1, 1]
scores = [[0.90, 0.85, 0.70, 0.65], [0.89, 0.84, 0.80, 0.75]]
t, lam = 2.0, 0.2
utility = [1.0, 1.0]
selected = []
for u, row in enumerate(scores):
    q = [v / sum(utility) for v in utility]
    anchor = sorted(range(2), key=lambda g: (utility[g], g))[int(2 * 0.5)]
    d = [(q[anchor] ** (1-t) - x ** (1-t)) * (1-t) * x ** (-t) for x in q]
    adjusted = [s + lam * d[group[i]] for i, s in enumerate(row)]
    top = sorted(range(4), key=lambda i: (-adjusted[i], i))[:2]
    print('user', u, 'q=', [round(x,6) for x in q], 'anchor=', anchor)
    print('distance=', [round(x,6) for x in d], 'top2=', top)
    for i in top:
        utility[group[i]] += row[i]
    selected.append(top)
print('final smoothed utility=', [round(x,6) for x in utility])
original = [0, 1]
reranked = selected[1]
discount = [1.0, 1/log2(3)]
retention = sum(scores[1][i] * discount[k] for k,i in enumerate(reranked)) / sum(scores[1][i]*discount[k] for k,i in enumerate(original))
positives = {0, 1}
ndcg = sum(discount[k] for k,i in enumerate(reranked) if i in positives) / sum(discount)
print('second-user score retention=%.6f heldout NDCG=%.6f' % (retention, ndcg))
assert selected == [[0, 1], [2, 3]]
