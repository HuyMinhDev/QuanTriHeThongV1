"""Ví dụ sư phạm tự xây dựng; KHÔNG phải mã huấn luyện chính thức PFA."""
from math import atan, log, log2, pi

def kl(p, q):
    return sum(x * log(x / y) for x, y in zip(p, q) if x > 0)

scores = [[0.90, 0.85, 0.70, 0.65], [0.88, 0.82, 0.78, 0.73]]
delta = [-0.16, -0.16, 0.00, 0.04]
providers = [0, 0, 1, 2]
positives = [{0, 1}, {0, 2}]
discounts = [1 / log2(k + 2) for k in range(2)]

def evaluate(lists):
    exposure = [0.0] * 3
    ndcg = []
    for u, ids in enumerate(lists):
        ndcg.append(sum(discounts[k] for k, i in enumerate(ids) if i in positives[u]) / sum(discounts))
        for k, i in enumerate(ids):
            exposure[providers[i]] += discounts[k]
    return [x / sum(exposure) for x in exposure], sum(ndcg) / len(ndcg)

base = [sorted(range(4), key=lambda i: (-row[i], i))[:2] for row in scores]
adjusted = [sorted(range(4), key=lambda i: (-(row[i] + delta[i]), i))[:2] for row in scores]
p, ndcg = evaluate(adjusted)
pb, ndcgb = evaluate(base)
pg = [p[0], p[1] + p[2]]
within = [p[1] / pg[1], p[2] / pg[1]]
inter = kl(pg, [0.5, 0.5])
intra = pg[1] * kl(within, [0.5, 0.5])
calibration = sum(x * log(a / b) for x, a, b in zip(pg, [0.5, 0.5], [1 / 3, 2 / 3]))
global_kl = kl(p, [1 / 3] * 3)
print('base top2:', base, 'NDCG=%.6f' % ndcgb)
print('adjusted top2:', adjusted, 'NDCG=%.6f' % ndcg)
print('provider shares:', [round(x, 6) for x in p])
print('KL base=%.6f adjusted=%.6f' % (kl(pb, [1 / 3] * 3), global_kl))
print('inter=%.6f intra=%.6f calibration=%.6f sum=%.6f' % (inter, intra, calibration, inter + intra + calibration))
assert abs(global_kl - inter - intra - calibration) < 1e-12
a = atan(10 * (0.6 - 0.8)) / pi + 0.5
print('soft swap alpha=%.6f outputs=(%.6f, %.6f)' % (a, (1-a)*0.8+a*0.6, a*0.8+(1-a)*0.6))
