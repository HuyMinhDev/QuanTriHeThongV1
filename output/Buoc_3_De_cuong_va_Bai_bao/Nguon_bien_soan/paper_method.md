# 3. Foundations and problem formulation

## 3.1. Scope, definitions, and notation

A recommender first learns a scorer and retrieves candidates; re-ranking then changes their final order. We study one offline batch of B users, with exactly K displayed items per user. Exposure means a prescribed position-weighted opportunity to be seen [25]; it is a proxy rather than an observed causal attention probability. Category diversity means the number of distinct metadata categories in a list. A popularity-head item belongs to the highest-frequency part of the training catalog. These three quantities represent different stakeholders and should not be merged into a single fairness claim [4,13,15].

| Symbol | Definition and domain |
|---|---|
| u, i, r, s | User, item, position, and scenario indices |
| C_u; M | Fixed candidate set for u; maximum candidate-set size |
| G; G_i | Nonempty category universe; set of categories attached to item i |
| s_ui | Bounded predicted relevance score in [0,1]; no probability interpretation assumed |
| w_r; W; D | Positive nonincreasing position weights; W=Σ_r w_r; D=BW |
| x_uir; z_ug | Binary assignment and binary category-presence variables |
| ε; d_u | Allowed relative predicted-score loss in [0,1]; minimum category count |
| h_is | Binary head membership of item i in scenario s |
| S; α; β | Number of equal-probability scenarios; confidence in [0,1); upper-tail mass β=1−α |
| θ; λ | Risk budget in [0,1]; nonnegative diversity objective weight |
| P; S(P); F(P) | Fixed slot assignments; structural completions; completions satisfying every constraint |
| ρ; Q_α | Scenario mixture; CVaR risk envelope |
| η; v_s | CVaR threshold and nonnegative excess variables |

Every user has at least K candidates. Repetition within a user's list is forbidden; the same item may be recommended to several users. There is no shared item capacity, no additional slot-specific eligibility constraint, and no adaptive choice of ranking after the scenario is observed. These assumptions are essential to the sorting certificate below. G_i may have several categories. The prototype stores these as a dictionary of item-to-category tuples.

For each user, π_u^base sorts candidates by s_ui, using deterministic item-ID tie breaking. By the rearrangement inequality, this maximizes the weighted predicted score because w_r is nonincreasing. Define U_u^base from this list. If U_u^base=0, its relative floor is zero and the retained-score ratio is reported as undefined. Raw learned logits are mapped through a fixed monotone sigmoid for this definition; the transformation is recorded because it changes relative-loss budgets. It is not a calibration claim.

## 3.2. Popularity scenarios and empirical tail risk

For the planned real-data study, divide training interactions into time blocks, resample blocks with replacement, recompute item counts, and label a fixed number of top-count items as head in each scenario. Use the train-observed catalog and a deterministic tie rule; repeat the entire resampling operation S times. Head labels within a scenario are dependent: exactly a fixed number of catalog items can be head. Scenarios are independent draws conditional on the observed training blocks and the stated bootstrap law. This is uncertainty about a train-popularity proxy, not about protected attributes or all future preference distributions [16–18].

For a fixed ranking x, the head-exposure share in scenario s is

```math
H_s(x) = (1/D) Σ_u Σ_i∈C_u Σ_r w_r h_is x_uir.                 (1)
```

The denominator D is the full batch exposure and never changes with a prefix. Thus 0≤H_s≤1. Following the established CVaR construction [30,31], define

```math
R_α(x) = min_η∈[0,1] { η + [1/(βS)] Σ_s max(H_s(x)−η, 0) }.
β = 1−α.                                                       (2)
```

For example, with four exposures (1,0.2,0,0) and α=0.5, the worst half averages to R_α=0.6. A budget θ=0.6 therefore permits the scenario with exposure 1. CVaR control is not a per-scenario maximum guarantee, except in the finite-sample special case α≥1−1/S. When βS is not integral, the last tail observation contributes a fractional mass; rounding the number of tail scenarios changes the risk definition.

**Proposition 1 (finite risk envelope; standard CVaR identity).** Let

```math
Q_α = {ρ: Σ_s ρ_s=1, 0≤ρ_s≤1/(βS)}.
Then R_α(x) = max_ρ∈Q_α Σ_s ρ_s H_s(x).                         (3)
```

**Proof.** First allow η to be free and introduce v_s≥H_s−η and v_s≥0 in (2). The Lagrangian multipliers ρ_s for the first inequalities give coefficients 1−Σ_sρ_s for η and 1/(βS)−ρ_s for v_s. A finite lower infimum requires Σ_sρ_s=1 and 0≤ρ_s≤1/(βS). The remaining dual objective is Σ_sρ_sH_s. The primal is a feasible bounded linear program, so strong LP duality gives (3). For losses in [0,1], an optimizer η can be chosen in [0,1], leaving the value unchanged. To maximize the dual, allocate mass at the cap to the largest H_s, then allocate the residual mass to the next observation. This exchange argument also proves the fractional-tail rule. If βS≤1, all mass may be placed on one maximum observation, giving R_α=max_sH_s. ∎

This identity is prior theory, not a claimed contribution. The confidence convention α used here must be converted explicitly when a baseline parameter instead denotes tail mass.

## 3.3. Hard constraints and optimization objective

Let q_ui=Σ_r x_uir and A_ug=Σ_i:g∈G_i q_ui. The constraints are

```math
Σ_i∈C_u x_uir = 1                         for every u,r;       (4)
Σ_r x_uir ≤ 1                             for every u,i;       (5)
U_u(x)=Σ_i,r w_r s_ui x_uir ≥ (1−ε)U_u^base for every u;        (6)
z_ug ≤ A_ug ≤ min(K, |{i∈C_u:g∈G_i}|) z_ug for every u,g;      (7)
Σ_g z_ug ≥ d_u                            for every u;         (8)
v_s ≥ H_s(x)−η, v_s≥0; 0≤η≤1;
η + [1/(βS)]Σ_s v_s ≤ θ; x_uir,z_ug∈{0,1}.                    (9)
```

When no candidate has category g, (7) forces z_ug=0. Both directions of (7) matter. Keeping only A_ug≤Kz_ug would allow a solver to set a category variable to one without selecting that category. Missing categories are represented by an explicit “unknown” category, with sensitivity analyses that exclude it from coverage; missing values are never silently counted as several new genres.

**Proposition 2 (exact encoding).** Under (4)–(5), binary z satisfying (7) are exactly the indicators that at least one selected item has category g. Constraints (4)–(9) are therefore equivalent to a valid ranking with all three stated floors/budgets.

**Proof.** If A_ug=0, z_ug≤A_ug implies z_ug=0. If A_ug≥1, the upper inequality implies z_ug=1 since z is binary. Conversely, the true indicator satisfies both inequalities, because no more than min(K,|C_ug|) category-g candidates can be selected. Equation (8) is exactly union coverage. Proposition 1 and the excess-variable epigraph show equivalence of (9) to R_α≤θ. The remaining equations directly encode slot occupancy, no repetition, and the score floors. ∎

Within this feasible set, the intended objective is

```math
maximize J(x) = [Σ_u U_u(x)]/D + λ [Σ_u Σ_g z_ug]/(B|G|).       (10)
```

Both components lie in [0,1] before multiplying the second by λ. Varying ε,d,θ generates trade-off curves instead of treating a single λ as a complete policy. A score floor protects the scorer's output. It does not prove a retained NDCG, click-through rate, satisfaction level, or protected-group fairness guarantee on held-out data. Those require separate measurements.

**Proposition 3 (hardness).** Deciding feasibility of the model is NP-hard for arbitrary multilabel categories, even with one user and without active score/risk constraints.

**Proof.** Reduce Set Cover with universe G, subsets T_1,…,T_m and cardinality bound 1≤k≤m, which suffices for its NP-hard restriction. Create one candidate per subset with G_i=T_i and k additional empty-category dummy candidates. Set B=1,K=k,d_1=|G|, all scores zero, arbitrary valid head coefficients, ε=1,θ=1, and positive weights. A cover with at most k subsets can be padded by distinct dummies to exactly k selected items and ordered arbitrarily. Conversely any feasible length-k list covers G by its nondummy subsets and yields a cover of size at most k. Since k≤m, construction size is polynomial even when k is encoded in binary. Thus a general polynomial-time exact feasibility claim would solve Set Cover. ∎

# 4. Scenario-coupled residual certificate

## 4.1. Componentwise relaxation

A prefix P is any consistent assignment of some user-position slots. S(P) contains completions satisfying only (4)–(5) and P. F(P) additionally enforces (6)–(9). If S(P) is empty, P is structurally impossible. Otherwise define b_s(P)=min_x∈S(P)H_s(x). Dropping score and category floors deliberately enlarges the residual feasible set. The simple necessary bound is LB_sep(P)=CVaR_α(b_1,…,b_S). It can be weak because a different ranking may attain each b_s.

For binary coefficients, b_s can also be understood as forced head exposure. For a user with L unfilled slots and t available tail candidates, at least max(0,L−t) head candidates must be selected. Put those candidates in the lowest remaining weight positions, add already fixed head exposure, and divide by D. This computes a per-scenario minimum but forgets which item choices conflict across scenarios.

## 4.2. Coupled mixture bound and closed form

For a fixed ρ∈Q_α, let a_i(ρ)=Σ_sρ_sh_is and define

```math
L_P(ρ) = min_x∈S(P) Σ_s ρ_s H_s(x).
LB_mix(P) = max_ρ∈Q_0(P) L_P(ρ),                              (11)
```

where Q_0(P) is a finite subset of Q_α. In the prototype it contains the uniform mixture, the tail-maximizing mixture ρ^sep for b(P), and two scenario-index cyclic envelope points (duplicate points are harmless). Each cyclic point fills successive scenario weights up to the cap 1/(βS) until their sum is one. These two extra points are heuristic screening choices, not learned parameters or claims of an optimal envelope search. Their usefulness is an ablation question.

**Proposition 4 (closed-form residual minimization).** Let R_u be the unfilled slots, L_u=|R_u|, and I_u the unused candidates for user u. Sort the remaining weights as ω_u1≥…≥ω_uL_u and the L_u smallest coefficients in I_u as a_u(1)≤…≤a_u(L_u). Then

```math
L_P(ρ) = {Σ_(u,r,i)∈P w_r a_i(ρ)
          + Σ_u Σ_j=1..L_u ω_uj a_u(j)} / D.                  (12)
```

**Proof.** For a fixed user, replacing a selected item by an unused smaller-coefficient item cannot increase cost because all weights are positive. Hence an optimum uses the L_u smallest coefficients. If two selected coefficients a≤b are paired with weights p≥q, putting a on p costs pa+qb, whereas the opposite costs pb+qa; their difference is (p−q)(a−b)≤0. Repeated swaps give the pairing in (12). Users optimize independently because items have no shared capacity. Fixed assignments contribute a constant. Summing and normalizing proves the formula. ∎

**Theorem 1 (validity and dominance).** If Q_0(P) includes a maximizer ρ^sep of ρ·b(P), then

```math
LB_sep(P) ≤ LB_mix(P) ≤ min_x∈F(P) R_α(x),                    (13)
```

using +∞ for an empty F(P). In fact LB_mix also bounds min_x∈S(P)R_α(x). Therefore LB_mix(P)>θ proves P cannot have a feasible completion. The reverse implication does not hold.

**Proof.** For every structural x and every nonnegative ρ, H_s(x)≥b_s, so ρ·H(x)≥ρ·b. Minimizing gives L_P(ρ^sep)≥ρ^sep·b=LB_sep. Maximizing over Q_0 preserves this inequality. For any fixed structural x, Proposition 1 implies R_α(x)≥ρ·H(x)≥L_P(ρ) for every ρ∈Q_0. Maximizing on the right and then minimizing over x proves the second bound for S(P). Since F(P)⊆S(P), the same lower bound applies to F(P). A completion satisfying R_α≤θ would contradict a strictly larger lower bound. ∎

This is weak duality plus a ranking-specific sorting relaxation. We do not present it as a new general duality theorem. Its candidate research value is the computational behavior of inexpensive scenario coupling during residual ranking checks.

**Example 1 (strict improvement and a remaining integrality gap).** One user has K=1 and candidates A,B. There are two scenarios with H(A)=(1,0), H(B)=(0,1), and α=0.5. Componentwise b=(0,0), giving LB_sep=0. The uniform mixture gives a_A=a_B=0.5 and L=0.5, so LB_mix=0.5. Both integer choices have CVaR=1. With θ=0.4, the mixture rejects while the componentwise bound does not. With θ=0.75, the mixture passes although no ranking is feasible. Even maximizing L over all of Q_α yields only 0.5: for ρ=(t,1−t), L=min(t,1−t)≤0.5. One must not interchange min over integer rankings and max over mixtures as an equality.

The prefix-specific LP-CVaR relaxation LP(P) of (4)–(9), with every fixed assignment in P imposed, x,z relaxed into [0,1] and the risk budget omitted when minimizing risk, is an essential additional bound. It includes the score and coverage relaxations. For any ρ, a fractional structural assignment is a convex combination of per-user assignment vertices; minimizing its linear mixture cost has the same structural value (12). Thus the optimal LP(P) minimum risk is at least LB_mix(P), and at most the prefix-specific integer minimum risk with score/category floors. Comparing a root LP to a nonempty-prefix certificate would not give this ordering. A timed-out LP primal value is not a certified lower bound; use a valid solver dual bound or obtain optimality. LP screening may be substantially stronger and more expensive; empirical comparisons must include both bound strength and total cost.

## 4.3. Certificate cost

With T=|Q_0|, a direct implementation forms mixture coefficients in O(TSBM), sorts candidates in O(TBM log M), and sorts scenario minima in O(S log S). Coefficients for shared items can be cached, making this a conservative bound. Storage for coefficients and scenario labels is O(SBM) in an uncached representation, plus candidate/order workspaces. With fixed T=4 the certificate is polynomial, but the whole constrained ranking problem remains NP-hard. Extra shared capacities or position eligibility would require a different residual assignment solver; formula (12) cannot simply be reused.

# 5. Witness-preserving construction and worked examples

## 5.1. Algorithm and oracle contract

A completion oracle receives a prefix and returns FEASIBLE with a complete ranking, INFEASIBLE with an exact-search/solver conclusion, or UNKNOWN when its budget ends without either conclusion. Every purported feasible ranking is independently checked against the original coefficients, no repeats, floors, risk, and the entire prefix. A solver limit with a verified feasible incumbent can return FEASIBLE; without an incumbent it returns UNKNOWN. The Python implementation supplies exhaustive enumeration for tiny cases and SciPy/HiGHS MILP for larger ones. Solver “infeasible” status is numerical solver evidence, not a separately machine-checked UNSAT proof.

```text
Algorithm 1: WCR(instance, completion_oracle, Qmax)
  if structural impossibility or LBmix(empty) > θ: return INFEASIBLE
  result ← completion_oracle(empty)
  if result has no verified feasible ranking: return its status
  W ← verified complete ranking; P ← empty; checks ← 0
  for u = 1,…,B and r = 1,…,K in this fixed order:
      chosen ← none
      order unused candidates by marginal J gain, then item ID
      for i in this order while checks < Qmax:
          P' ← P plus (u,r)↦i; checks ← checks+1
          if LBmix(P') > θ or P' is structurally impossible: continue
          result ← completion_oracle(P')
          if result has a verified feasible ranking W':
              W ← W'; chosen ← i; break
          # UNKNOWN provides no infeasibility certificate
      if chosen is none: chosen ← W[u,r]
      P ← P plus (u,r)↦chosen
  independently verify the completed P; return FEASIBLE, P
```

The priority is w_rs_ui/D plus λ times newly covered categories divided by B|G|. It is a heuristic for (10). A feasible completion may have a smaller overall J than the previous witness; the current prototype does not promise monotone objective improvement. Qmax is a global candidate-check budget, not a per-slot bound. Enumeration's state_limit and MILP's time_limit control individual oracle effort; wall-clock scheduling across calls is a planned engineering extension. Once a verified initial witness exists, exhausted improvement budgets cause witness fallback rather than an unchecked greedy decision. If initial feasibility is UNKNOWN, the method abstains and reports UNKNOWN. Any operational return of the original list must be separately labeled uncertified for these constraints.

**Theorem 2 (conditional feasibility preservation).** In exact arithmetic, suppose the initial witness is feasible and every subsequently accepted completion is feasible and agrees with the proposed prefix. Algorithm 1 outputs a feasible ranking after BK slot steps, regardless of how many later oracle calls return UNKNOWN.

**Proof.** Invariant: at the start of each slot, W is feasible and agrees with P. It holds at initialization. When a new completion is accepted, it is verified feasible and agrees with P plus the new choice, preserving the invariant. If none is accepted, selecting W[u,r] extends P by a value already present in its feasible witness, also preserving the invariant. Every step fills one previously empty slot, so after BK steps P fills every slot and equals W. Feasibility of W gives feasibility of the output. ∎

This theorem is conditional on obtaining a witness. It does not establish that a witness will be found within any deadline, optimality of J, a Pareto optimum, or a submodular 1−1/e approximation. Completion-aware scheduling and feasibility look-ahead have prior antecedents [20]. The formal invariant mainly prevents an incorrect claim that a cheap necessary test alone guarantees a full ranking.

## 5.2. Example 2: a partial budget check can become blocked

Let B=2,K=1,w_1=1. User 1 has A with score 0.9 and B with score 0.8. User 2 has only A with score 1.0. A is head in every scenario and B is tail. Every item has category g; d_1=d_2=1. Set ε=0.2 and θ=0.5, with any valid α. Baseline utilities are (0.9,1.0), so floors are (0.72,0.8).

Step 1: local greedy picks A for user 1. Using the correct full denominator D=2, the partial head exposure is 1/2 and seems within budget. Step 2: user 2 must also receive A; final exposure becomes 1 and violates θ. Normalizing the partial list by its own current exposure would create a different, equally inappropriate partial check.

WCR instead obtains witness (B,A), with scores (0.8,1.0) and risk 0.5. For trial prefix user1↦A, the residual structural minimum includes the forced A for user 2, so LB_mix=1>θ and the trial is rejected. The next trial user1↦B admits completion (B,A). User2↦A finishes the batch. Both score floors and genre floors hold. The supplied run trace records one bound rejection and a verified final ranking. The example is constructed here for explanation; it is not copied from a source paper.

## 5.3. Example 3: equal counts can hide different exposure

One user, K=2, w=(2,1). A is always head, score 1.0, category a; B is always tail, score 0.9, category b. Require d=2, ε=0.1, θ=1/3. The baseline order (A,B) has U^base=2.9, so the floor is 2.61. Its head exposure is 2/3 and violates θ. Order (B,A) has utility 2×0.9+1=2.8≥2.61, covers two categories, and has head exposure 1/3. WCR's first trial A at position 1 is rejected by LB_mix=2/3; B at position 1 has a feasible completion. Both lists contain one head item, demonstrating why head-item counts cannot replace position-weighted exposure. The code evaluates the numerical values shown here.

## 5.4. Total complexity and numerical implementation

Let C_LB be certificate cost and C_F the cost of one completion call including verification. Without an explicit check budget, WCR checks at most BKM candidate prefixes and makes at most 1+BKM oracle calls. A conservative total bound is O(BKM(C_LB+C_F+log M)); prefix priority sorting and initial feasibility are included up to constants. With global Qmax, substitute min(BKM,Qmax) for the candidate-check term, retaining O(BKM log M) priority sorting overhead. An exhaustive oracle may examine up to ∏_u M_u!/(M_u−K)! rankings, each requiring exposure, coverage, and score evaluation. MILP also has exponential worst-case complexity. Reporting only the sorting cost as the algorithm's running time would be incorrect.

The reference verifier uses tolerance 10^−8 for real-valued constraints; study comparisons use 10^−7. Strict certificate rejection is implemented as LB_mix>θ+tolerance. These are numerical acceptance rules, not an exact-arithmetic proof assistant. Recompute primal metrics from returned item IDs, preserve solver statuses, gaps and bounds, and do not translate UNKNOWN into INFEASIBLE. Formal Theorems 1–2 state exact-arithmetic properties; the numerical checks below provide finite implementation evidence.

## 5.5. Independent audit statement and its limits

The training-scenario constraint alone does not certify risk under unseen scenario distributions. A limited statistical diagnostic is possible if the ranking x and threshold η are fixed before drawing N fresh independent scenarios from the same conditional bootstrap law. Let Z_j=max(H_j(x)−η,0). Since 0≤Z_j≤1, Hoeffding's inequality [37] and (2) give, with probability at least 1−δ,

```math
CVaR_α,pop(H(x)) ≤ η + {mean_j Z_j
                     + sqrt[log(1/δ)/(2N)]}/(1−α).             (14)
```

**Proof.** For fixed x,η, Hoeffding bounds E[Z] by its independent sample mean plus the displayed deviation. Population CVaR is the infimum over thresholds, hence is at most the objective at this fixed η. Substitute the mean bound and divide by positive 1−α. ∎

The confidence term grows as α approaches one and can make (14) vacuous; cap the bound at 1 when presenting it. Selecting x or η using these same audit samples invalidates the fixed-choice argument. Use separate tuning/audit splits or a justified simultaneous correction. This is a statement about the specified conditional bootstrap distribution, not a guarantee of future platform exposure, demographic fairness, or a causal mitigation of popularity feedback. It is a supplementary diagnostic, not the central contribution.
