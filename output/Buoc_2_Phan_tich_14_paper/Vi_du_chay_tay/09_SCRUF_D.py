"""Ví dụ tự xây dựng về Borda, coverage và NLIP; không phải SCRUF-D gốc."""
from math import sqrt

items = ['A', 'B', 'C', 'D']
orders = {'user': ['A', 'B', 'C', 'D'], 'group': ['C', 'A', 'B', 'D'], 'coverage': ['D', 'C', 'B', 'A']}
weights = {'user': 2, 'group': 1, 'coverage': 1}
points = {i: 0 for i in items}
for voter, order in orders.items():
    for rank, item in enumerate(order):
        points[item] += weights[voter] * (len(items) - rank - 1)
ranking = sorted(items, key=lambda i: (-points[i], items.index(i)))
top = ranking[:2]
base = orders['user'][:2]
rbo = sum(len(set(base[:d]) & set(top[:d])) / d for d in (1, 2)) / 2
nlip = max(max(0, orders['user'].index(i) + 1 - 2) for i in top) / (4 - 2)
print('Borda scores:', points)
print('base:', base, 'rerank:', top)
print('RBO=%.6f NLIP=%.6f' % (rbo, nlip))
raw_coverage = len(set(['A', 'B'] + top)) / 4
target = 0.85
print('catalog coverage=%.6f target-normalized=%.6f' % (raw_coverage, raw_coverage / target))
fairness = [0.8, 0.2]
norm = sum(sqrt(x) for x in fairness) ** 2 / len(fairness) ** 2
print('fairness arithmetic mean=%.6f Lhalf=%.6f' % (sum(fairness)/2, norm))
print('second coverage example raw1.0 / target0.65 = %.6f' % (1/0.65))
assert top == ['A', 'C'] and abs(nlip - 0.5) < 1e-12
