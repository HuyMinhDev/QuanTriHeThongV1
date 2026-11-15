"""Original teaching example for single-item SMMR sampling, no PyTorch."""
from math import exp, isclose, log, ceil


def softmax(scores, temperature):
    assert temperature > 0
    maximum = max(scores)
    weights = [exp((s-maximum)/temperature) for s in scores]
    return [w/sum(weights) for w in weights]


def draw(items, probabilities, uniform):
    cumulative = 0.
    for item, probability in zip(items, probabilities):
        cumulative += probability
        if uniform < cumulative:
            return item
    return items[-1]


if __name__ == "__main__":
    relevance = {"A": .95, "B": .9, "C": .8, "D": .7}
    genre = {"A": 0, "B": 0, "C": 1, "D": 1}
    chosen = ["A"]
    for step, uniform in enumerate([.9, .2], 2):
        items = [i for i in relevance if i not in chosen]
        scores = [.5*relevance[i]-.5*max(float(genre[i] == genre[j])
                                             for j in chosen) for i in items]
        probabilities = softmax(scores, .1)
        item = draw(items, probabilities, uniform)
        print("step", step, "candidates", items,
              "scores", [round(x, 6) for x in scores],
              "probabilities", [round(x, 6) for x in probabilities],
              "uniform", uniform, "chosen", item)
        chosen.append(item)
    assert chosen == ["A", "D", "B"]
    assert isclose(sum(softmax([1000., 999.], .1)), 1)
    print("ranking", chosen, "mean_relevance", sum(relevance[i] for i in chosen)/3)
    batches, selected, round_index = [], 0, 0
    while selected < 20:
        batch = min(2**round_index, 20-selected)
        batches.append(batch)
        selected += batch
        round_index += 1
    assert batches == [1, 2, 4, 8, 5]
    print("paper_batch_sizes_K20_s2", batches)
    assert ceil(log(1+(2-1)*20, 2)) == len(batches)
    print("All teaching checks passed.")
