import inspect
import numpy as np
from typing import Optional, Dict, Any, Callable
from .eval import _cvar_one
from tqdm.auto import tqdm
import pulp
def tie_break_by_mean_score(is_min: np.ndarray, mean_scores: np.ndarray, **kwargs: Dict[str, Any]) -> int:
    """
    Tie-break by selecting the candidate with the highest mean score.
    This is the original method.
    """
    tied_scores = np.where(is_min, mean_scores, -np.inf)
    return np.argmax(tied_scores)
def tie_break_randomly(is_min: np.ndarray, **kwargs: Dict[str, Any]) -> int:
    """
    Tie-break by selecting a random candidate from the tied set.
    """
    tied_indices = np.where(is_min)[0]
    return np.random.choice(tied_indices)

def _rel_2d(rels: np.ndarray) -> np.ndarray:
    """Vectorized mean relevance for a 2D array."""
    if rels.shape[1] == 0:
        return np.zeros(rels.shape[0])
    return rels.mean(axis=1)
def _sumrel_2d(rels: np.ndarray) -> np.ndarray:
    """Vectorized sum of relevance for a 2D array."""
    return rels.sum(axis=1)
def _prec_2d(rels: np.ndarray) -> np.ndarray:
    """Vectorized Precision@k for a 2D array."""
    if rels.shape[1] == 0:
        return np.zeros(rels.shape[0])
    return (rels > 0).mean(axis=1)
def _mrr_2d(rels: np.ndarray) -> np.ndarray:
    """Vectorized Mean Reciprocal Rank for a 2D array."""
    bin_rel = rels >= 0.5
    # Find the index of the first relevant document for each row (intent)
    ranks = np.argmax(bin_rel, axis=1)
    # If no relevant doc is found for a row, argmax returns 0.
    # We need to check if a relevant doc actually exists at that position.
    has_rel = bin_rel[np.arange(len(ranks)), ranks]
    # Calculate reciprocal rank, which is 0 if no relevant doc was found.
    reciprocal_ranks = has_rel / (ranks + 1.0)
    return reciprocal_ranks
def _err_2d(rels: np.ndarray, max_rels: np.ndarray) -> np.ndarray:
    """Vectorized Expected Reciprocal Rank for a 2D array of rankings."""
    if rels.shape[1] == 0:
        return np.zeros(rels.shape[0])
    # max_rels should be (C, 1) to broadcast correctly
    prob_stop = (np.power(2.0, rels) - 1.0) / (2.0 ** max_rels)
    prob_stop = np.clip(prob_stop, 0, 1)
    prob_continue_all = np.cumprod(1 - prob_stop, axis=1)
    prob_continue = np.insert(prob_continue_all[:, :-1], 0, 1.0, axis=1)

    ranks = np.arange(1, rels.shape[1] + 1)
    err = (prob_continue * prob_stop / ranks).sum(axis=1)
    return err
def _rbp_2d(rels: np.ndarray, p: float, max_rels: np.ndarray) -> np.ndarray:
    """Vectorized Rank-Biased Precision for a 2D array."""
    if rels.shape[1] == 0:
        return np.zeros(rels.shape[0])
    gains = np.divide(rels, max_rels, out=np.zeros_like(rels, dtype=float), where=max_rels!=0)
    weights = (1 - p) * (p ** np.arange(rels.shape[1]))
    return (gains * weights).sum(axis=1)
def _dcg_2d(rels: np.ndarray, disc: np.ndarray) -> np.ndarray:
    """Vectorized DCG for a 2D array."""
    k = rels.shape[1]
    return (rels * disc[:k]).sum(axis=1)
def _dcg_vec(rels: np.ndarray, disc: np.ndarray, **kwargs) -> float:
    """Linear DCG. rels length <= len(disc)"""
    return float((rels * disc[: len(rels)]).sum())
def _edcg_2d(rels: np.ndarray, disc: np.ndarray) -> np.ndarray:
    """Vectorized Exponential DCG for a 2D array."""
    k = rels.shape[1]
    exp_gains = np.power(2.0, rels) - 1.0
    return (exp_gains * disc[:k]).sum(axis=1)
def _ndcg_2d(rels: np.ndarray, disc: np.ndarray, idcgs: np.ndarray) -> np.ndarray:
    """Vectorized nDCG. Takes a vector of pre-computed IDCGs."""
    dcgs = _dcg_2d(rels, disc)
    return np.divide(dcgs, idcgs, out=np.zeros_like(dcgs), where=idcgs!=0)
def _endcg_2d(rels: np.ndarray, disc: np.ndarray, eidcgs: np.ndarray) -> np.ndarray:
    """Vectorized eNDCG. Takes a vector of pre-computed eIDCGs."""
    edcgs = _edcg_2d(rels, disc)
    return np.divide(edcgs, eidcgs, out=np.zeros_like(edcgs), where=eidcgs!=0)
def _cvar_one(loss: np.ndarray, w: np.ndarray, beta: float) -> float:
    """Helper to calculate CVaR for one set of losses."""
    if beta >= 1.0: return float(np.average(loss, weights=w))
    if beta <= 0.0: return float(loss.max())

    q = np.quantile(loss, 1 - beta)
    tail_losses = loss[loss >= q]
    tail_weights = w[loss >= q]

    if tail_weights.sum() == 0: return q
    return np.average(tail_losses, weights=tail_weights)
def _map_2d(rels: np.ndarray) -> np.ndarray:
    """
    Vectorized Mean Average Precision for binary relevance.

    Assumes rels are already binary (0 or 1).
    """
    # No normalization needed - already binary
    bin_rel = rels.astype(bool)
    num_rel = bin_rel.sum(axis=1)

    csum = np.cumsum(bin_rel, axis=1)
    ranks = np.arange(1, rels.shape[1] + 1)
    prec = csum / ranks

    ap = (prec * bin_rel).sum(axis=1)
    return np.divide(ap, num_rel, out=np.zeros_like(ap, dtype=float), where=num_rel!=0)
def _oracle_score_intent(
    rel_row: np.ndarray, metric: str, k: int, disc: np.ndarray, p: float = 0.8
) -> float:
    """
    Best possible score for one intent, top-k docs.

    For MAP and Precision, assumes rel_row is already binary.
    """
    if rel_row.size < k: k = rel_row.size
    top_k_indices = np.argpartition(-rel_row, k - 1)[:k] if k > 0 else []
    rels = rel_row[top_k_indices]
    rels_sorted = np.sort(rels)[::-1]

    rels_2d = rels_sorted[None, :]
    if metric == "map":
        return _map_2d(rels_2d)[0]
    if metric == "prec":
        # Simplified: no min/max needed for binary relevance
        return _prec_2d(rels_2d)[0]

    # Other metrics remain the same
    max_rel_metric = rel_row.max()
    if max_rel_metric == 0: max_rel_metric = 4.0
    max_rels_2d = np.array([[max_rel_metric]])

    if metric == "rel": return _rel_2d(rels_2d)[0]
    if metric == "sumrel": return _sumrel_2d(rels_2d)[0]
    if metric == "mrr": return _mrr_2d(rels_2d)[0]
    if metric == "dcg": return _dcg_2d(rels_2d, disc)[0]
    if metric == "ndcg": return 1.0 if _dcg_2d(rels_2d, disc)[0] > 0 else 0.0
    if metric == "endcg": return 1.0 if _edcg_2d(rels_2d, disc)[0] > 0 else 0.0
    if metric == "err": return _err_2d(rels_2d, max_rels_2d)[0]
    if metric == "rbp": return _rbp_2d(rels_2d, p, max_rels_2d)[0]
    return 0.0
def ours(
    cprob: np.ndarray,
    qrels: np.ndarray,
    *,
    metric: str = "rel",
    k: int,
    beta: float = 0.1,
    p: float = 0.8,
    baseline_rnk: Optional[np.ndarray] = None,
    tgt_lvl: Optional[float] = None,
    filter_docs: bool = False,
    tie_breaker: Callable[..., int] = tie_break_by_mean_score,
    **kwargs,
) -> np.ndarray:
    """
    Greedy MINIMISER of CVaR of the loss L(c) = [M0(c) − M(rank | c)]_+

    Now accepts a `tie_breaker` function to resolve ties when multiple
    documents yield the same minimum CVaR.

    For MAP and Precision, assumes qrels are already binary.
    """
    # Robustness Fix: Check for and correct qrels dimension order
    if qrels.ndim == 3 and cprob.ndim == 2 and qrels.shape[0] == cprob.shape[0] and qrels.shape[2] == cprob.shape[1]:
        qrels = qrels.transpose(0, 2, 1)
    if beta is None:
        beta = 0.1
    T, C, D = qrels.shape
    disc = 1.0 / np.log2(np.arange(2, k + 2))
    ranking = -np.ones((T, k), dtype=np.int32)
    # Process each query
    for t in tqdm(range(T), desc=f"Ours (Vectorized CVaR, {metric})"):
        w_c = cprob[t] / cprob[t].sum() if cprob[t].sum() > 0 else np.full(C, 1.0 / C)
        r_tc = qrels[t]  # Shape: (C, D)
        if filter_docs:
            # Filter out non-relevant documents
            non_zero_mask = np.any(r_tc > 0, axis=0)  # Check along intent axis
            valid_docs = np.where(non_zero_mask)[0]

            if len(valid_docs) == 0:
                ranking[t, :] = np.arange(min(k, D))
                continue
        else:
            valid_docs = np.arange(D)

        n_valid = len(valid_docs)
        r_tc_filtered = r_tc[:, valid_docs]  # Shape: (C, n_valid)
        # Pre-computation for M0 (Target Score)
        M0 = np.empty(C, dtype=np.float32)
        max_rels_t = r_tc.max(axis=1, keepdims=True)
        max_rels_t[max_rels_t.squeeze() == 0] = 4.0
        # NDCG: Match the first version exactly - use full sort on unfiltered r_tc
        if metric == 'ndcg':
            idcgs_t = np.ones(C, dtype=np.float32)  # Default to 1 to avoid division by zero
            for c in range(C):
                ideal_oracle_rels = np.sort(r_tc[c])[::-1][:k]
                idcgs_t[c] = _dcg_vec(ideal_oracle_rels, disc)
        elif metric == 'endcg':
            top_k_rels = np.partition(r_tc, -min(k, r_tc.shape[1]), axis=1)[:, -min(k, r_tc.shape[1]):]
            eidcgs_t = _edcg_2d(np.sort(top_k_rels, axis=1)[:, ::-1], disc)

        # M0 calculation
        if baseline_rnk is not None:
            rels_b = r_tc[:, baseline_rnk[t, :k]]
            if metric == 'ndcg': M0 = _ndcg_2d(rels_b, disc, idcgs_t)
            elif metric == 'endcg': M0 = _endcg_2d(rels_b, disc, eidcgs_t)
            elif metric == 'map':
                M0 = _map_2d(rels_b)
            elif metric == 'prec':
                # Simplified: no normalization needed for binary qrels
                M0 = _prec_2d(rels_b)
            else: M0 = globals()[f"_{metric}_2d"](rels_b, p=p, max_rels=max_rels_t, disc=disc) if metric in ['rbp','err','dcg','edcg'] else globals()[f"_{metric}_2d"](rels_b)
        else:
            for c in range(C):
                M0[c] = _oracle_score_intent(r_tc[c], metric, k, disc, p)
            if tgt_lvl is not None and 0 < tgt_lvl <= 1.0: M0 *= tgt_lvl
        # Ranking State Initialization
        available = np.ones(n_valid, dtype=bool)
        current_scores_c = np.zeros(C, dtype=np.float32)

        # Metric-specific state
        if metric in ['rel', 'sumrel']:
            state = {'sum': np.zeros(C, dtype=np.float32)}
        elif metric == 'prec':
            state = {'count': np.zeros(C, dtype=np.float32)}
        elif metric == 'err':
            state = {'prob_continue': np.ones(C, dtype=np.float32)}
        elif metric == 'map':
            num_rel = r_tc_filtered.sum(axis=1)  # Already binary
            state = {
                'csum_rel': np.zeros(C),
                'ap_sum': np.zeros(C),
                'num_rel': num_rel
            }
        else:
            state = {}
        # Greedy Selection Loop
        for pos in range(min(k, n_valid)):
            candidate_indices = np.where(available)[0]
            candidate_rels = r_tc_filtered[:, candidate_indices] # Shape: (C, num_candidates)
            n_candidates = len(candidate_indices)
            # Vectorized score calculation for all candidates
            if metric in ['dcg', 'edcg', 'ndcg', 'endcg']:
                if metric == 'dcg': delta = candidate_rels * disc[pos]
                elif metric == 'edcg': delta = (np.power(2.0, candidate_rels) - 1.0) * disc[pos]
                elif metric == 'ndcg': delta = np.divide(candidate_rels * disc[pos], idcgs_t[:, np.newaxis], out=np.zeros_like(candidate_rels), where=idcgs_t[:, np.newaxis]!=0)
                else: delta = np.divide((np.power(2.0, candidate_rels) - 1.0) * disc[pos], eidcgs_t[:, np.newaxis], out=np.zeros_like(candidate_rels), where=eidcgs_t[:, np.newaxis]!=0)
                trial_scores_all = current_scores_c[:, np.newaxis] + delta

            elif metric == 'rbp':
                gain = np.divide(candidate_rels, max_rels_t, out=np.zeros_like(candidate_rels), where=max_rels_t!=0)
                delta = (1 - p) * gain * (p ** pos)
                trial_scores_all = current_scores_c[:, np.newaxis] + delta

            elif metric == 'err':
                prob_stop_d = np.divide(np.power(2.0, candidate_rels) - 1.0, np.power(2.0, max_rels_t) - 1.0, out=np.zeros_like(candidate_rels), where=max_rels_t!=0)
                prob_stop_d = np.clip(prob_stop_d, 0, 1)
                delta = (state['prob_continue'][:, np.newaxis] * prob_stop_d) / (pos + 1.0)
                trial_scores_all = current_scores_c[:, np.newaxis] + delta
            elif metric == 'rel':
                trial_scores_all = (state['sum'][:, np.newaxis] + candidate_rels) / (pos + 1.0)
            elif metric == 'sumrel':
                trial_scores_all = state['sum'][:, np.newaxis] + candidate_rels
            elif metric == 'prec':
                # Simplified: qrels are already binary, so `> 0` is not needed.
                trial_scores_all = (state['count'][:, np.newaxis] + candidate_rels.astype(bool)) / (pos + 1.0)

            elif metric == 'mrr':
                is_rel_all = (candidate_rels > 0)
                trial_scores_all = np.where(current_scores_c[:, np.newaxis] > 0, current_scores_c[:, np.newaxis], is_rel_all / (pos + 1.0))
            elif metric == 'map':
                is_rel_all = candidate_rels.astype(bool)
                trial_csum_rel = state['csum_rel'][:, np.newaxis] + is_rel_all
                prec_at_pos = trial_csum_rel / (pos + 1.0)
                delta_ap_sum = prec_at_pos * is_rel_all
                trial_ap_sum = state['ap_sum'][:, np.newaxis] + delta_ap_sum
                trial_scores_all = np.divide(trial_ap_sum, state['num_rel'][:, np.newaxis], out=np.zeros_like(trial_ap_sum), where=state['num_rel'][:, np.newaxis]!=0)
            # Vectorized CVaR computation
            loss_all = np.maximum(0, M0[:, np.newaxis] - trial_scores_all)  # Shape: (C, n_candidates)

            # Vectorized CVaR computation for all candidates at once
            if beta >= 1.0:
                risks = np.average(loss_all, weights=w_c, axis=0)
            elif beta <= 0.0:
                risks = loss_all.max(axis=0)
            else:
                threshold = 1.0 - beta
                w_c_expanded = w_c[:, np.newaxis]

                sort_indices = np.argsort(loss_all, axis=0)
                sorted_losses = np.take_along_axis(loss_all, sort_indices, axis=0)
                sorted_weights = np.take_along_axis(np.broadcast_to(w_c_expanded, (C, n_candidates)), sort_indices, axis=0)

                cumsum_weights = np.cumsum(sorted_weights, axis=0)
                threshold_idx = np.argmax(cumsum_weights >= threshold, axis=0)
                quantiles = sorted_losses[threshold_idx, np.arange(n_candidates)]

                tail_masks = loss_all >= quantiles
                numerator = np.sum(loss_all * tail_masks * w_c_expanded, axis=0)
                denominator = np.sum(tail_masks * w_c_expanded, axis=0)
                risks = np.where(denominator > 0, numerator / denominator, quantiles)

            mean_scores = np.sum(w_c[:, np.newaxis] * trial_scores_all, axis=0)
            # --- Selection ---
            min_risk = np.min(risks)
            tolerance = 1e-9 * np.abs(min_risk) if min_risk != 0 else 1e-9
            is_min = np.abs(risks - min_risk) < tolerance

            best_local_idx_in_candidates = tie_breaker(
                is_min=is_min,
                mean_scores=mean_scores
            )

            best_doc_local_idx = candidate_indices[best_local_idx_in_candidates]

            # Update State with Best Document
            available[best_doc_local_idx] = False
            ranking[t, pos] = valid_docs[best_doc_local_idx]
            current_scores_c = trial_scores_all[:, best_local_idx_in_candidates]

            best_rels_d = r_tc_filtered[:, best_doc_local_idx]
            if metric in ['rel', 'sumrel']:
                state['sum'] += best_rels_d
            elif metric == 'prec':
                # Simplified: qrels are already binary
                state['count'] += best_rels_d.astype(bool)
            elif metric == 'err':
                prob_stop_d = np.divide(np.power(2.0, best_rels_d) - 1.0, np.power(2.0, max_rels_t.squeeze()) - 1.0, out=np.zeros(C), where=max_rels_t.squeeze()!=0)
                state['prob_continue'] *= (1.0 - np.clip(prob_stop_d, 0, 1))
            elif metric == 'map':
                is_rel_d = best_rels_d.astype(bool)
                state['csum_rel'] += is_rel_d
                prec_at_pos = state['csum_rel'] / (pos + 1.0)
                state['ap_sum'] += (prec_at_pos * is_rel_d)
        # Fill remaining ranks if not enough valid docs were found
        if filter_docs and n_valid < k:
            non_zero_mask = np.any(r_tc > 0, axis=0)
            zero_docs = np.where(~non_zero_mask)[0]
            ranking[t, n_valid:] = zero_docs[:k - n_valid]
    return ranking.astype(np.int32)

