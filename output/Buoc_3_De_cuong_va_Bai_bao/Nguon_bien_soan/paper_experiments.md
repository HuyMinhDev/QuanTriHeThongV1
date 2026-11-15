# 6. Executed finite-instance validation

## 6.1. Apparatus, implementation, and reproducibility

The supplied prototype is written in Python 3.14.3 with NumPy 2.4.4 and SciPy 1.17.1, on macOS 26.4.1 arm64. SciPy's mixed-integer optimizer uses HiGHS. The exact CPU model, RAM size, solver thread settings and peak memory were not measured in this execution, so this draft makes no hardware-normalized speed or memory claim. A 16 GB RAM CPU workstation is a target for the later study, not a measured property of this run. No GPU is used by the finite-instance code.

`core.py` implements the model evaluator, exact fractional-tail CVaR, structural lower bounds, exhaustive completion search and WCR. `milp_backend.py` implements assignment, score, category and CVaR linear constraints, including continuous relaxation. `test_core.py` exercises thirteen distinct cases. `run_study.py` records deterministic inputs, results, source hashes, solver statuses and comparisons in JSON, with a per-instance CSV summary. The independent evaluator computes exposure and constraints directly from returned item IDs rather than trusting solver objective values. These files implement a finite re-ranking simulator; they do not implement or claim to have trained all published baselines.

The thirteen tests check fractional tails and risk endpoints; the dual envelope; blocked partial greedy; positional exposure; coupled-scenario pruning; the fact that a small bound is not positive feasibility; randomized residual inequalities; fallback without further candidate checks; initial UNKNOWN; MILP/enumeration agreement; absent-category protection; root rejection without an oracle; and marginal diversity priority. The named examples in Sections 4–5 are run by the study script as well.

## 6.2. Study design

Forty instances are generated with seed 20261115. Each has B=2, three candidates per user, K=2, S=4 and w=(2,1), with some shared items across users. Scores and binary scenario coefficients are generated synthetically. The parameter choices are ε∈{0.3,0.6}, θ∈{0.25,0.5,0.75,1}, and α∈{0,0.35,0.5,0.75,0.9}; the minimum category count is one. The script samples this finite set of settings; it is not a complete factorial experiment. Six consistent prefixes per instance, including the empty prefix, yield 240 prefix checks. Their structural completions total 2,680 enumeration visits across checks; this number counts visits and is not the number of distinct full rankings.

The d=1 floor is automatically satisfied when all selected items have a category, so the forty-instance collection does not stress difficult coverage constraints. The separate d=2 positional example and absent-category unit test cover selected cases; broader coverage-infeasible and d≥2 random instances remain necessary.

Synthetic head coefficients are not fixed-head-size train-block bootstrap samples. They stress the implementation over arbitrary binary coefficients, for which the mathematical bounds remain valid. They do not establish how the method behaves under realistic popularity drift. For each prefix, exhaustive structural search computes minimum achievable CVaR. At the root, enumeration with score/category floors but without the risk budget gives an integer minimum risk, compared with MILP and LP relaxation. WCR with unrestricted candidate checks and with zero additional candidate checks after its initial witness are compared to exact feasibility status.

## 6.3. Observed results

| Check on the recorded synthetic collection | Actual result |
|---|---|
| Instances / prefixes / structural completion visits | 40 / 240 / 2,680 |
| Strictly stronger mixture bound than componentwise bound | 74 of 240 prefixes; 21 of 40 roots |
| Prefixes rejected at their assigned θ: componentwise / mixture | 105 / 115 |
| Additional prefixes rejected by mixture | 10 |
| Roots rejected: componentwise / mixture | 13 / 15 |
| Exact feasible / infeasible instances | 23 / 17 |
| WCR status agreement with exact feasibility | 40 of 40 |
| Zero-extra-check witness-fallback status agreement | 40 of 40 |
| MILP minimum risk versus integer enumeration | 40 of 40 match; maximum absolute difference 0 |
| Root LP ordering LB_mix≤LP≤integer minimum risk | 40 of 40 satisfy within 10^−7 |
| Assertion failures in study | 0 |

The additional ten rejections are a count of bound strength, not a runtime speedup. The 23 feasible outputs were evaluated against the explicit instance constraints; infeasible outcomes include exact-search conclusions and valid root-bound rejections. The zero-extra-check configuration can simply return its initial witness, so its agreement demonstrates preservation and fallback behavior rather than improved ranking quality. Forty finite cases cannot establish general correctness of arbitrary code or distribution-wide superiority. Theorems provide the mathematical statements; tests check selected implementation consequences.

# 7. Prespecified real-data evaluation protocol — not yet executed

## 7.1. Research questions and data

RQ1 asks whether scenario-based exposure control improves independent audit tail risk over nominal and mean-only controls at matched relevance and diversity. RQ2 asks whether mixture pruning saves total computation relative to componentwise bounds, LP screening and no screening. RQ3 asks whether witnessed construction offers a useful quality/deadline trade-off against direct MILP and comparable repair. RQ4 asks how candidate coverage, training sparsity and temporal change limit feasibility. These questions are open; the tables below specify measurements rather than predicted successful values.

| Dataset and authoritative source | Planned use and feasibility condition |
|---|---|
| MovieLens 1M [32], [GroupLens download and README](https://grouplens.org/datasets/movielens/1m/) | Primary benchmark. User/item/rating/time records and movie genres support temporal scoring, popularity counts and category diversity. Record the actual postprocessing counts and file checksums after download. |
| Amazon Review Data 2018 [33], [UCSD source](https://cseweb.ucsd.edu/~jmcauley/datasets/amazon_v2/) | Musical Instruments 5-core interaction subset; the source lists 231,392 reviews. Obtain matching product metadata for category paths. File availability and metadata access must be checked before committing the second benchmark; no download is claimed here. |

For Amazon, count diversity over a predeclared informative category-path depth, removing the common root “Musical Instruments”; otherwise a one-root taxonomy makes the metric trivial. Record hierarchy depth, missingness and candidate category availability. A source-provided 5-core is a retrospective selection and can induce future activity selection bias. Prefer the ratings-only raw category file with a training-only active-user/item filter when feasible; if using the published 5-core for comparability, disclose this selection and report a raw-category sensitivity analysis. Never recompute the 5-core on the full interaction stream while calling the evaluation leakage-free. Source terms and metadata accessibility determine the usable files; a replacement dataset requires a documented protocol revision.

## 7.2. Temporal preprocessing and candidate generation

Use a primary global chronological 70%/10%/20% train/validation/test split by interaction count, respecting tied timestamps with a fixed policy and reporting actual dates and sizes. Deduplicate repeated user–item events under a declared earliest-event rule. For implicit training, use observed interactions; for held-out relevance use rating≥4, reporting the exact convention and positive counts. No test interaction influences model fitting, candidate retrieval, category-floor selection, head labels, scenario generation or θ tuning. Training-only filters define warm users and items. Report test interactions discarded by this warm-start protocol and evaluate cold-start separately if supported; do not hide them by filtering the entire future stream.

Train BPR [26] as the primary scorer and LightGCN [27] as a robustness scorer through a pinned compatible environment, optionally using RecBole [28]. Use validation-only hyperparameter tuning: embedding dimensions {32,64}, learning rates {0.001,0.005}, regularization {10^−5,10^−4}, and a recorded early-stopping rule. Software compatibility must be checked in an isolated environment; the Python 3.14 finite-instance environment is not claimed to be a working RecBole/PyTorch training environment. Report versions and commits after successful installation. Five fixed training seeds are planned, with the same trained scores reused across re-ranking methods.

Primary candidates are the top M∈{100,200} unobserved train-catalog items by the frozen scorer, excluding each user's known history up to the evaluation cutoff. Do not inject held-out positives into candidate sets. Log the fraction of held-out relevant items retrieved; re-ranking cannot recover candidates that were never retrieved. All comparable re-rankers receive identical candidates, score transformation, masks, categories and scenarios. Evaluate K∈{5,10,20}. Primary w_r=1/log2(r+1); uniform weights form a sensitivity analysis. Use small batches B∈{8,16} first and expand to {32,64} only when measured costs permit. An exact small-instance subset uses M≤20 and B≤4 for reliable MILP gaps.

## 7.3. Scenario construction, budgets and audit independence

Form calendar-week training blocks where possible; inspect block count and interaction support before choosing a wider block length. Resample the same number of whole blocks with replacement, aggregate item counts, and choose the top ceil(0.10|I_train|) items as head, with train item-ID tie breaking. Generate S∈{50,64} independent scenario draws conditional on those blocks; each draw contains dependent item memberships. Nominal head uses original train counts. Do not include validation or test events in train scenarios. When there are too few blocks for credible resampling, document this limitation and test alternative block lengths rather than asserting asymptotic validity.

Use α=0.8 as the primary confidence, meaning a 20% upper tail; α∈{0,0.5,0.9} is sensitivity analysis. Avoid interpreting α≥1−1/S as a smooth tail trade-off because it reduces to a maximum. Tune ε∈{0.05,0.10,0.20}, category floors d∈{1,2,3} and θ on validation, recording infeasible settings rather than silently lowering floors. Pick θ from a predeclared grid spanning nominal-baseline exposure and smaller budgets. Use λ∈{0,0.05,0.1,0.2}; compare full trade-off curves and at matched constraint levels, not cherry-picked single optima.

After selecting rankings and η on optimization/tuning scenarios, draw 1,024 fresh audit scenarios; use 512 as a sample-size sensitivity analysis. Use independent random seeds and never retune against the final audit. Compute audit mean, empirical CVaR, maximum, exceedance fraction and, if applicable, the conditional-bootstrap bound (14). Separately recompute head membership in chronological future windows as a drift diagnostic. A single future window provides one exposure value, not an empirical distribution of future risk. Future-window labels are evaluation-only and do not repair test rankings.

## 7.4. Baselines and fair computational comparisons

| Baseline family | Purpose and matching requirements |
|---|---|
| Frozen-score Top-K; nominal popularity penalty | Establish the original accuracy and exposure operating points. Sweep the penalty rather than choosing it from test labels. |
| MMR [29]; SMMR [11] | Relevance–diversity baselines with the same category/embedding similarity, candidate pools and tuning budget. Record randomness; avoid dense catalog-wide similarities. |
| ElasticRank [10]; FairSort [22] | Relevant utility–fairness trade-off methods. Adapt the group definition transparently; retain original algorithm behavior and measure violations of the shared constraints rather than assuming compliance. |
| Mean-risk and nominal constrained MILP | Isolate the effect of scenario CVaR from hard constraints and integer optimization. Match ε,d and score objective. |
| Direct scenario-CVaR MILP | Strong optimization baseline for exactly the same formulation. Record best incumbent, certified solver bound, gap, timeout and first-feasible time under the same total wall-clock limit. |
| WCR without screening; WCR with LB_sep | Isolate value of screening and of scenario coupling. Same initial witness, candidate priority, oracle and budgets. |
| WCR with LP-CVaR screening | Determine whether a stronger generic relaxation dominates the specialized cheap bound after accounting for cost. |
| MMR-priority with the same verified-completion contract | Separate the contribution of witness preservation from the particular objective priority. |
| PFA [1], SCRUF-D [9], VRisker [5] as extensions | Broader state-of-the-art comparisons if their objectives, required metadata and runnable code permit a meaningful common setup. Differences in fairness definitions must remain explicit. |

Include source links for the fourteen papers in Appendix A. Freeze runnable repository commits, dependencies and licenses when reproducing each baseline; the supplied Step 2 archive contains inspected code excerpts and source notes, not a claim that every full repository was cloned. No implementation should be called the “original code” unless its provenance is recorded. FairDiverse [12] is useful infrastructure but does not remove the need to audit each baseline and metric.

For screening comparisons, reuse the same initial feasible witness and oracle settings. Count bound time, oracle time, initialization, sorting, final verification and logging. Warm starts and caching must be enabled equally where applicable or reported as separate ablations. Cap total optimization time, not just each solver call. Proposed pilot limits are 10 and 60 seconds per batch; these are tunable feasibility targets, not observed latency. Any method exceeding the deadline or failing to obtain a witness returns a recorded status. Accuracy over certified outputs alone is selection-biased, so report both conditional metrics and coverage of all requested batches.

## 7.5. Metrics, estimands and statistical analysis

With binary held-out relevance rel_ur, DCG@K=Σ_r(2^rel_ur−1)/log2(r+1), and NDCG=DCG/IDCG when IDCG>0. Recall@K counts recommended held-out positives divided by the user's held-out positive count. Report the policy for users with no held-out positives and exclude them consistently from the accuracy denominator. These are held-out measures, distinct from U/U^base. For multi-positive lists, preserve identical evaluation candidate universes across methods.

| Dimension | Required measurements |
|---|---|
| Relevance | NDCG@K, Recall@K; candidate recall; predicted score retention U/U^base; worst-user and quantile score deficit |
| Diversity | Per-user union category count, category entropy, pairwise intra-list dissimilarity; catalog coverage with a stated catalog denominator |
| Exposure/risk | Train-scenario and independent-audit mean/CVaR/max head exposure, tail exposure 1−H, exceedance probability; item-exposure Gini and group shares as diagnostics |
| Constraint feasibility | FEASIBLE/INFEASIBLE/UNKNOWN fractions; maximum and mean violations of (6),(8),(9); certified-output coverage; fallback frequency |
| Optimization | J, incumbent/bound/gap on exact subset; number of candidate checks, oracle calls and bound rejects; strength/time of LB_sep, LB_mix and LP |
| Cost | End-to-end batch time median/p95, initial-witness time, certificate and oracle shares, peak RSS, scenario-construction cost |
| Joint trade-off | Matched ε,d,θ curves; DPFR [13] only with a declared relevance/fairness definition, common normalization and fixed retrospective oracle; no test oracle for tuning |

For nonnegative exposure e_i over n items in the declared evaluation catalog, including zero-exposure items, Gini=Σ_iΣ_j|e_i−e_j|/(2nΣ_ie_i). Report a zero-denominator result as undefined. It describes concentration, not automatically relevance-aware fairness [4]. For intra-list diversity, fix sim(i,j), for example Jaccard over informative category sets, and use mean(1−sim) over unordered item pairs for K≥2. Empty metadata must have a declared similarity policy. Lower head share is not proof of individual merit fairness or demographic fairness.

Users share a batch-level risk budget, so their outputs are dependent. Use paired batch-level comparisons across methods and a hierarchical/block bootstrap over chronological batches with shared training-seed replications; do not treat all user–seed observations as independent. Report effect sizes, 95% confidence intervals and all seeds; apply Holm correction to a small prespecified primary comparison family. Repeated seeds on the same data are not independent real-world datasets. For drift time series use contiguous-block resampling. Publish negative/undefined/infeasible results with denominator counts.

## 7.6. Experimental scenarios, ablations and decision criteria

The planned experiment sequence is: (i) exact tiny-instance correctness and optimality-gap studies; (ii) nominal versus mean versus CVaR controls on the same scorer; (iii) LB_sep/LB_mix/LP/no-screen ablation with matched witness/oracle; (iv) candidate size and near-boundary infeasibility stress; (v) S,α and block-length sensitivity; (vi) temporal drift and category-noise/missingness; (vii) computational scaling in B,M,K; and (viii) transfer from BPR to LightGCN. Also ablate the two cyclic mixtures, marginal-diversity priority and witness reuse.

H1 is unsupported if independent audit risk gains disappear at matched held-out accuracy/diversity or under future-window drift. H2 is unsupported if extra pruning fails to reduce total computation. H3 is unsupported if direct MILP or verified MMR consistently offers better quality and certified-output coverage under the same deadline. In those cases report a restricted contribution, negative result, or revise the method. Do not re-label an existing CVaR epigraph or a standard feasibility check as a new algorithm to compensate.

The final empirical paper should contain a dataset/split table; an accuracy–risk–diversity operating-point table; independent-audit and drift plots; solver-status and constraint-violation tables; exact-subset gap results; and cost/ablation curves. All those real-data entries are **not measured yet** in this draft. The only filled results are the finite-instance checks in Section 6.

# 8. Limitations, thesis contributions and publication development

The current evidence supports the mathematical validity of the residual relaxation and finite code consistency. It does not demonstrate useful accuracy or speed on recommendation benchmarks. Exact completion calls can dominate runtime; large-scale use may be impractical without a genuinely stronger structural result, more efficient oracle or less frequent checks. The structural bound drops score and diversity floors, which can make it too weak precisely when infeasibility comes from those floors. Extending the certificate with Lagrangian score/coverage terms is a plausible next direction, but needs an admissible efficiently solvable residual subproblem and fresh proofs. Shared provider capacities invalidate independent sorting and require a flow/assignment relaxation.

The head/tail target is a policy choice: popular items can be relevant, and tail exposure alone is not merit-based fairness. Genre metadata is an imperfect diversity proxy. Bootstrap scenarios represent resampling uncertainty conditional on observed logs, not exposure propensities, causal feedback or full distributional robustness. A train-only scorer floor can preserve model bias. The study is offline and does not claim online user benefit.

The master's thesis can contribute a complete reproducible finite-candidate audit formulation, a rigorously delimited certificate, and an honest experimental assessment of when screening is useful. A stronger paper contribution would require demonstrating a nontrivial computational advantage over direct MILP/LP and verified heuristic baselines, together with robust audit-risk findings. The main working title is the title of this manuscript. A possible later systems-focused title is “When Can Recommendation Re-ranking Meet Its Constraints? Auditing Candidate-Pool Feasibility under Popularity Drift”; it should become a separate paper only if it asks a distinct question with substantial new evidence, avoiding duplicate publication.

Potential venues include recommender-systems/information-retrieval conferences or applied intelligent-systems journals whose current scopes match the eventual contribution. Select a target after empirical results and a fresh check of scope, article type, costs and related publications. No acceptance, quartile or claim of unpublished priority is guaranteed. Before submission, rerun the related-work search, including [19,21,22,34,35], compare full methods rather than abstracts alone, freeze all artifacts and have the supervisor review the novelty statement.

# 9. Conclusion

We proposed a scenario-based constrained re-ranking study centred on residual feasibility auditing. A finite mixture certificate is valid, dominates a componentwise certificate when the prescribed envelope point is included, and admits a sorting solution under explicit structural assumptions. Maintaining a verified completion preserves feasibility after successful initialization, while UNKNOWN remains distinct from infeasibility. Executed synthetic checks illustrate stronger pruning and agree with enumeration/MILP on the tested collection. The substantive recommendation-performance and computational hypotheses remain open for the prespecified real-data study.
