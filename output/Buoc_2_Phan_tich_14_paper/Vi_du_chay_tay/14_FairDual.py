"""Ví dụ Jensen và weighted loss tự xây dựng, KHÔNG phải FairDual đầy đủ."""
from math import log

batches = [[4.0, 0.0], [0.0, 4.0]]
mean = [sum(row[g] for row in batches)/2 for g in range(2)]
square_of_mean = sum(x*x for x in mean)
mean_of_squares = sum(sum(x*x for x in row) for row in batches)/2
global_worst = max(mean)
local_worst = sum(max(row) for row in batches)/2
print('mean group loss=', mean)
print('f(mean)=%.6f mean(f)=%.6f Jensen gap=%.6f' % (square_of_mean, mean_of_squares, mean_of_squares-square_of_mean))
print('max(mean)=%.6f mean(max)=%.6f' % (global_worst,local_worst))
adjacency = [[1,0],[0,1],[0.5,0.5]]
mu = [-0.2, 0.1]
weights = [1-sum(a*m for a,m in zip(row,mu)) for row in adjacency]
probabilities = [0.5,0.8,0.6]
losses = [-log(x) for x in probabilities]
weighted = sum(w*l for w,l in zip(weights,losses))
print('weights=',[round(x,6) for x in weights])
print('losses=',[round(x,6) for x in losses])
print('unweighted=%.6f weighted=%.6f' % (sum(losses),weighted))
eta, H = 1/10, 1.0
print('bound-audit B=100 eta=.1 H/eta=%.6f' % (H/eta))
print('bound-audit B=400 eta=.05 H/eta=%.6f' % (H/0.05))
assert weights == [1.2,0.9,1.05]
