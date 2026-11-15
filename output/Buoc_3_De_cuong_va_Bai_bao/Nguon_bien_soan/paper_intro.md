# Scenario-Coupled Feasibility Audits for Multi-Objective Recommendation Re-ranking under Popularity Uncertainty

**Research manuscript draft — formal development, executable finite-instance validation, and a prespecified real-data protocol.** Author order and affiliations require confirmation. Literature checked through 15 November 2026. Real-data recommendation experiments have not been executed for this draft.

## Tóm tắt tiếng Việt

Tái xếp hạng giúp điều chỉnh độ chính xác, đa dạng và cơ hội hiển thị mà không huấn luyện lại toàn bộ hệ gợi ý. Tuy nhiên, tập ứng viên hữu hạn có thể không chứa bất kỳ danh sách nào đồng thời đáp ứng các yêu cầu; bất định của thống kê độ phổ biến còn làm nhãn head/tail thay đổi tương quan giữa các sản phẩm. Bản thảo đề xuất một bài toán hữu hạn có sàn utility dự báo theo người dùng, độ phủ thể loại tối thiểu và ngân sách CVaR cho exposure nhóm phổ biến qua các kịch bản. Một cận dưới ghép kịch bản được tính bằng sắp xếp tập ứng viên còn lại, dùng để loại sớm các nhánh chắc chắn vô nghiệm. Cơ chế WCR duy trì một nghiệm hoàn tất khả thi và phân biệt nghiệm khả thi, vô nghiệm có căn cứ và chưa kết luận khi hết ngân sách. Bản thảo chứng minh tính đúng của mã hóa, cận dưới và invariant của thuật toán; các nguyên lý CVaR, weak duality và completion checking là nền tảng đã biết, không được nhận là phát minh mới. Mô phỏng nhỏ kiểm tra tính nhất quán với liệt kê đầy đủ và MILP; giao thức MovieLens/Amazon được thiết kế nhưng chưa chạy. Tính mới và hiệu quả trên dữ liệu thực vẫn là giả thuyết cần kiểm chứng.

## Abstract

Post-processing can balance recommendation utility, content diversity, and item exposure without retraining a relevance model. Its constraints may nevertheless be jointly infeasible within a finite candidate pool, while head-item membership estimated from interaction counts can vary jointly across plausible popularity scenarios. We formulate batch re-ranking with per-user predicted-utility floors, category-coverage floors, and an empirical upper-tail CVaR budget on position-weighted head exposure. We develop a residual-candidate lower bound obtained from scenario mixtures and closed-form assignment sorting. Including the risk-envelope optimizer of the componentwise bound guarantees dominance over that simpler certificate; neither bound establishes positive feasibility. A witness-preserving construction uses these bounds before completion queries and retains a verified completion when additional search is inconclusive. Its guarantee concerns feasibility of the stated finite instance, rather than held-out accuracy, future exposure, or approximation to a global optimum. The draft supplies proofs, executable counterexamples, MILP and enumeration references, and a controlled finite-instance validation. MovieLens and Amazon experiments are specified but remain unexecuted. The research claim to be tested is whether the specialized bound provides useful pruning and whether scenario-based exposure control improves independent audit risk at matched utility, diversity, and computation budgets.

**Keywords:** recommender systems; constrained re-ranking; exposure; popularity uncertainty; conditional value-at-risk; feasibility auditing.

# 1. Introduction

A recommender can accurately predict popular items and still provide repetitive lists or concentrate visibility on a small part of the catalog. Diversification and exposure control address different aspects of this problem: the first concerns variation within a user's recommendations, whereas the second concerns how attention is allocated across items or groups. Post-processing offers a modular intervention because a relevance model can remain frozen while a downstream policy changes the final lists.

The combination is not intrinsically new. User fairness, item fairness, and diversity have already been studied together [15]; FairSort provides minimum predicted-utility guarantees [22]; integer formulations allocate exposure under business constraints [19,24]; and Fair Queues checks whether a partial choice can still admit a fair completion [20]. Recent systems also validate repaired recommendations and explicitly support abstention [21]. Consequently, a contribution cannot be justified by the phrase “accuracy, diversity, and fairness together.”

We focus on a narrower setting. A batch must be served from fixed candidate sets; each returned list must satisfy a user-specific utility floor and a category-coverage floor; and the definition of a popular item is itself uncertain. Resampling training-time interaction blocks and recomputing a fixed-size head set creates correlated head memberships: items compete for the same top-decile positions. A single ranking must serve all scenarios, rather than choosing a different list after observing each scenario.

This setting creates two distinct problems. A policy can fail because it searches poorly despite the existence of an acceptable allocation, or because no acceptable allocation exists in its candidates. An independent-scenario availability bound does not fully distinguish them: each scenario may individually permit zero head exposure, while the same list cannot achieve zero exposure in all scenarios. Exact mixed-integer optimization can answer small instances but may be too expensive to query at every candidate decision.

Our proposed study therefore centres on a specialized, inexpensive infeasibility certificate and an auditable search contract. For each admissible scenario mixture, structural completion reduces to selecting low-cost residual candidates and pairing them with remaining position weights. A finite collection of such mixtures yields a lower bound on the achievable tail exposure. A witnessed completion is maintained during construction; a timeout without a witness is reported as UNKNOWN. These choices make the algorithm's finite-instance claims explicit without creating a universal guarantee of relevance or fairness.

The intended contributions are:

1. A precise finite-candidate formulation separating predicted utility, category diversity, and scenario-based exposure risk, together with an exact MILP representation and explicit policy assumptions.
2. A residual-candidate scenario-mixture certificate, a dominance result over a componentwise availability bound, and a witness-preserving construction with sound rejection and fallback semantics.
3. A reproducible evaluation design that separates certificate correctness, optimization quality, empirical audit risk, held-out recommendation accuracy, and computational cost.

The first contribution specializes existing optimization tools; the second uses established risk duality and rearrangement rather than introducing a new CVaR theory. The novelty of the complete mechanism remains conditional on the literature search and real-data results. The draft does not claim a first-ever fair, uncertain, constrained, or verified recommender.

# 2. Related work and the evidence boundary

## 2.1. The fourteen studies synthesized from the supplied analyses

All fourteen Word analyses were ingested, with file hashes and extracted text retained in the source manifest. The following table records their role in this study. Reported values belong to the original protocols and are not directly comparable across rows.

| Study | Relevant result or mechanism | Boundary for the proposed problem |
|---|---|---|
| PFA/HEFA [1] | Learns post-hoc score adapters for hierarchical provider exposure. Beauty+BPR reports NDCG/Gini 0.1000/0.7260 before and 0.0943/0.6282 after adaptation. | Does not establish the simultaneous finite-scenario, per-output coverage/utility contract studied here. Random-split evidence does not establish temporal robustness. |
| Behind the Re-Rank [2] | Explains fairness-induced semantic substitutions and studies explanation framing with 54 participants. | Explaining outcomes is complementary to, rather than a substitute for, a feasibility certificate. The user study does not validate our proposed algorithm. |
| ADF [3] | Combines diversity and user-profile compatibility in news recommendation. Benefits vary by dataset and operating point. | Its user-calibration fairness differs from batch-level item exposure. Individual profile compatibility can conflict with a global head budget. |
| Relevance-aware fairness measures [4] | Analyses attainability, undefined cases, zero exposure, locality and cutoff sensitivity. | Supports careful evaluator design; it is not a new re-ranking policy or proof that a low concentration measure is normatively fair. |
| VRisk/VRisker [5] | Uses CVaR of underserved intent utility; reports efficient greedy diversification. | Risk is over intents within a query, whereas our risk is over popularity scenarios for a batch. Its theoretical guarantees cannot be transferred to our constraints. |
| CatDive [6] | Combines category-aware representation/training with diversification and coverage-driven re-ranking. | Training and re-ranking contributions must be separated; category diversity is not a global exposure guarantee. |
| IPS-LAE [7] | Propensity-weighted linear autoencoders improve catalog coverage; ML20M–EASE coverage changes from 0.2134 to 0.7133 in the reported setup. | A popularity-frequency proxy is not identified causal exposure, and catalog coverage alone does not enforce a risk budget. |
| LLM diversity re-ranking [8] | Compares prompt-based diversification with strong greedy baselines; LLMs do not dominate every trade-off. | Adds generation and output-validation costs. A language model is unnecessary for the finite combinatorial question in this study. |
| SCRUF-D [9] | Social-choice mechanisms combine item-level and group fairness. Gains depend on domain and target normalization. | Combining agents already exists; an additional agent does not alone establish novelty or hard constraint satisfaction. |
| ElasticRank [10] | Uses economic elasticity to model utility–fairness trade-offs. | Its score-retention NDCG must be distinguished from held-out NDCG. Neither a high retention score nor a soft correction certifies our joint constraints. |
| SMMR [11] | Adds stochastic selection and growing batches; MIND+BPR@100 shows coverage 0.37 to 0.400 at the reported equal rounded recall point. | Stochastic diversity and fewer rounds do not enforce a head-risk budget; dense similarity construction still costs memory. |
| FairDiverse [12] | Provides a common toolkit for fairness/diversity algorithms and evaluation. | Useful infrastructure; defaults, masks and scoring conventions require audit. A toolkit composition alone is not a methodological contribution. |
| DPFR [13] | Evaluates relevance–fairness trade-offs against a Pareto-based reference. | A test-label oracle is suitable for retrospective evaluation, not for deployment-time feasibility or parameter tuning. |
| FairDual [14] | Addresses mini-batch optimization of max-min group fairness using dual methods. | Training-time group utility differs from guaranteed feasibility of a frozen-score batch output. |

These studies motivate a common topic, but they do not jointly prove the absence of every relevant prior method. We therefore expanded the search beyond the initial fourteen.

## 2.2. Closest prior art that restricts the novelty claim

TSFD Rank already combines user fairness, item exposure fairness and diversity through optimization and ranking decomposition [15]. Noisy-attribute fair ranking controls uncertain memberships [16], while multi-grouping robust ranking considers alternative partitions [18]. Two-stage fairness research explicitly identifies candidate pools that a subsequent ranker cannot repair [17]. Our work therefore does not introduce uncertainty about groups or the observation that candidates limit fairness.

Equity by Design studies discrete allocations, producer constraints and consumer-group CVaR under business constraints [19]. The latest author version is an ICTIR 2026 paper, not a SIGIR main-track paper. Its CVaR is over consumer utility and its discussed model assumes equal positional attention; our uncertain quantity is the head label in position-weighted batch exposure. Fair exposure allocation with integer programming and minimum guarantees is also established [24]. Upper head exposure and lower complementary tail exposure are equivalent when total attention is fixed, so reversing the inequality does not provide novelty.

Fair Queues' “can be fair” subroutine already tests whether a partial action can admit a fair completion [20]. FairSort already restricts predicted utility loss for each user [22]. FAIRGate adds runtime policy selection, validation, repair and abstention [21]. Its arXiv record reports conference acceptance, which we distinguish from independently verified publisher metadata. FARE introduces uncertainty-aware exposure adjustment in financial personalization; its arXiv version is described as an extension of a workshop paper [34]. We do not claim that a validator, a utility floor, completion look-ahead, or uncertainty-aware exposure adjustment is independently new.

Constrained multi-matchings under uncertain valuations use robust and CVaR optimization [23]. Scenario-based bounds for risk-averse mixed-integer programming predate this work [35]. Ranking under attribute constraints and position-based exposure optimization are foundational [25,36]. Our residual sorting bound is an application of a risk envelope and a structural assignment relaxation. A generic LP-CVaR relaxation is a necessary comparator because optimizing all mixtures cannot, in general, close the integral gap.

## 2.3. Conditional gap and falsifiable claims

Within the inspected sources, we did not find the exact residual-candidate certificate for correlated, resampled popularity-head scenarios under both per-user score and category floors. This is a bounded search observation, not proof of priority. The proposed method must demonstrate a useful accuracy–risk–diversity region and lower certificate cost, rather than relying on terminology.

The primary hypotheses are H1: scenario-based control improves independent audit tail exposure against nominal and mean-only controls; H2: the mixture certificate rejects more impossible prefixes per unit time than the componentwise bound; H3: the witnessed construction offers a useful quality/cost trade-off against direct MILP and repair methods under the same deadline. Each may fail. If direct MILP dominates the construction or the certificate overhead exceeds the queries it saves, the appropriate conclusion is a negative result or a revised method.
