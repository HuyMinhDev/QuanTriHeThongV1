<pagebreak>

# 7. Hướng cải tiến để xây đóng góp luận văn và paper

## 7.1. Hướng A — Reranking có exposure budget dưới bất định popularity

**Khuyến nghị làm hướng chính.** Câu hỏi hẹp: ước lượng độ bất định của popularity từ lịch sử có giúp giữ diversity và exposure budget ổn định hơn dưới drift, với cùng mức giảm accuracy và cùng candidate pool không? Đây là câu hỏi nghiên cứu, chưa phải kết luận thuật toán mới.

Tiền lệ phải so là ElasticRank [10], PFA [1], SMMR [11], SCRUF-D [9], VRisker [5] và FairDual [14]. Điểm dự kiến kiểm chứng là cách đưa uncertainty của **nhóm popularity** vào constraint/penalty và feasibility handling, thay vì chỉ λ thích nghi theo số lượt tương tác.

**Mô hình dự kiến:** giữ BPR đóng băng, Cᵤ là candidates và πᵤ là top-K. Cho s̄ᵤᵢ≥0 là score chuẩn hóa bằng quy tắc fit từ train/validation, Dᵤ là diversity và E_head là exposure tính trên cả batch. Tối đa predicted utility + diversity, dưới budget exposure và một sàn predicted utility:

U_s(π) = ΣᵤΣᵣ wᵣ·s̄ᵤ,πᵤ(r);  U_s(π) ≥ (1−ε_s)·U_s(π_base).

E_head(π)/E_total ≤ θ;  Dᵤ(πᵤ) ≥ τᵤ khi khả thi.

Sàn trên là **score-based guardrail**, không bảo đảm held-out NDCG. Nhãn test không có tại inference nên không thể viết “hard constraint NDCG thật không giảm quá 3%” rồi dùng test để thi hành. Budget accuracy thực được đánh giá hậu kiểm, với cấu hình đã chọn trên validation.

**Uncertainty khả thi:** bootstrap các block thời gian trong train, tính lại item counts và membership Head ở mỗi mẫu. qᵢ là tỷ lệ mẫu mà item i thuộc Head; thử penalty theo expected head exposure Σᵤ,ᵣ wᵣq_πᵤ(r), hoặc quantile budget trên các mẫu. Giữ baseline head-set cố định theo counts train để so. Không gọi phân phối bootstrap này là xác suất exposure nhân quả; nó phản ánh bất định của thống kê quan sát theo mô hình resampling đã chọn.

Nếu dùng chance constraint, phải ghi rõ nguồn ngẫu nhiên, mức δ, số mẫu, cách hiệu chuẩn trên validation và phạm vi bảo đảm dưới distribution shift. Kiểm tra quantile coverage/calibration và rate vi phạm trên windows tương lai; một posterior/quantile không được hiệu chuẩn có thể chỉ làm penalty bảo thủ hơn mà không tạo lợi ích.

**Hiện thực ban đầu:** greedy theo marginal score/diversity, thêm exposure dual price; sau đó local swaps/repair. Dual update là heuristic nếu chưa có chứng minh hội tụ và feasibility. Với quota bắt buộc, cần bước xác nhận hoặc solver trên bài toán đã định nghĩa; nếu không khả thi, trả slack tối thiểu và lý do, không lặng lẽ nới constraint.

**Đóng góp có thể chứng minh:** (i) phát biểu rõ uncertainty và constraint; (ii) thuật toán/repair với phân tích chi phí và điều kiện có nghiệm; (iii) bằng chứng robust trade-off trên hai miền và temporal windows. Bác bỏ giả thuyết nếu empirical violation/CI không tốt hơn penalty deterministic ở cùng relevance budget, hoặc lợi ích chỉ xuất hiện khi thêm candidates/tuning.

## 7.2. Hướng B — Nhận biết quota không khả thi do candidate bottleneck

Đây có thể là nhánh phụ gọn, xuất phát từ FairSync [16], TaxRank [15] và DPFR [13]. Nhiều thí nghiệm chỉ ghi fairness thấp mà không biết constraint có thể đạt từ top-M hay không.

Xây feasibility checker trên batch nhỏ: biến nhị phân xᵤᵢᵣ chỉ item được đặt ở slot r; mỗi slot một item, item không lặp, candidate membership, exposure budget và score floor. Nếu diversity là số category phủ, dùng biến zᵤg và ràng buộc liên kết để tuyến tính hóa. Nếu dùng ILD pairwise, cần biến cặp/linearization và chi phí cao hơn; không gọi nó là cùng một MILP đơn giản.

Solver tối ưu với gap=0 cho bài toán được định nghĩa là reference chính xác. Solver timeout chỉ cho upper/lower bound và gap, không phải nghiệm tối ưu đã chứng minh. Trên batch lớn dùng greedy/repair và báo khoảng cách với reference nhỏ.

Candidate enrichment chỉ được thêm như một track riêng và so ở cùng tổng M/thời gian. Đóng góp tiềm năng là phân tích quan hệ giữa candidate support, diversity threshold và exposure feasibility; **không phải** khẳng định mới về việc retrieval ảnh hưởng fairness, vì [16] đã xét điều đó.

## 7.3. Hướng C — Benchmark ba mục tiêu có frontier khả đạt và uncertainty

Phù hợp nếu muốn đóng góp thực nghiệm/tái lập. Mở rộng câu hỏi DPFR [13] và metric validity [4]: khi cùng candidate pool, cùng temporal split, thay fairness target/discount hoặc nhãn thiếu có làm đảo thứ hạng các rerankers không?

Xây một benchmark tối thiểu gồm BPR + 6–7 policies, hai dataset khác miền, rolling windows, raw predictions và thống kê tái lập. Báo frontier ba trục, bootstrap đúng unit và candidate-constrained reference. Có thể tạo phát hiện hữu ích dù phương pháp mới không thắng toàn bộ, nhưng một tập hợp bảng benchmark thông thường chưa tự đủ cho paper; cần phát hiện nhất quán, giải thích được cơ chế và phân tích độ tin cậy.

## 7.4. Hướng D — Diversity thích nghi với cold users và calibration

Gần CatDive [6], ADF [3] và VRisker [5]. Số tương tác là proxy yếu của uncertainty: user có 20 item cùng một thể loại khác user có 20 item trải đều. Có thể kết hợp history size, entropy và uncertainty của phân bố thể loại để điều chỉnh τᵤ/λᵤ; dùng shrinkage về phân bố chung cho user ít dữ liệu.

Đối sánh bắt buộc là λ cố định, λ theo history size đơn giản và λ theo entropy; thêm VRisker/calibration khi cùng input khả dụng. Ablation từng tín hiệu; không đưa test preference vào bộ điều khiển. Kết quả cần cho thấy cold users được lợi mà không dồn tổn thất sang nhóm khác, đồng thời exposure toàn batch vẫn đạt budget.

Giải thích bằng tiếng Việt [2] và LLM reranking [8] là nhánh bổ sung sau cùng. Với máy 16 GB, không nên bắt đầu bằng huấn luyện LLM để giải bài toán mà một greedy baseline chưa được tái lập.

<pagebreak>

# 8. Ma trận RQ–thí nghiệm và kế hoạch triển khai

## 8.1. RQs đề nghị chốt trong đề cương

| RQ | Dữ liệu và đối sánh | Chỉ số / bằng chứng để trả lời |
|---|---|---|
| RQ1: Có cải thiện diversity và exposure với accuracy loss trong margin đã chốt? | ML1M + Amazon Instruments; BPR; no-rerank/MMR/pop-penalty/SMMR/ElasticRank/VRisker. | NDCG loss và CI, ILD, coverage, Gini, exposure gap, frontier. Không kết luận chỉ từ một λ. |
| RQ2: Uncertainty popularity có ích hơn penalty deterministic dưới drift? | Global-time/rolling windows; fixed shared candidates; bỏ uncertainty là ablation chính. | Violation rate, constraint slack, calibration của quantile, NDCG loss, runtime. Cần cùng ngân sách tuning. |
| RQ3: Lợi ích có ổn định ở user ít lịch sử và khi thay K/M? | Nhóm history từ train; K=5/10/20; M=50/100/300/500. | Subgroup effect/CI, candidate recall, feasibility. Không xóa user khó ra khỏi đánh giá. |
| RQ4 tùy chọn: Bottleneck đến từ retrieval hay reranking? | Shared-pool track, enriched-pool track, solver reference nhỏ. | Candidate support, feasible optimum/slack, end-to-end trade-off và latency. |

## 8.2. Ablation tối thiểu

- Proposed đầy đủ; bỏ diversity; bỏ exposure; bỏ uncertainty; thay adaptive rule bằng fixed rule.
- Giữ candidate pool để so cơ chế; candidate enrichment là track tách biệt có baseline trên pool mới.
- Thay popularity head cutoff 5%/10%/20%, attention discount, category similarity và mức thiếu metadata.
- Kiểm tra thứ tự users/batches; θ/τ từ dễ đến khó, gồm trường hợp vô nghiệm được nhận diện.
- Trên tập nhỏ, so greedy/repair với solver reference; trên tập lớn, báo time/memory/feasibility.

Lưu cả cấu hình không thắng và failure cases. Không dùng ablation “bỏ một thành phần nhưng tăng mạnh tuning cho bản đầy đủ”; mỗi biến thể có ngân sách tương xứng.

## 8.3. Lộ trình 12 tuần phù hợp điều kiện đề tài

| Tuần | Công việc | Sản phẩm kiểm tra |
|---|---|---|
| 1–2 | Đọc 14 hồ sơ và 5–10 prior art sát hướng A; toy 4–10 items; định nghĩa fairness target. | Related-work matrix 20–30 công trình, RQs, ví dụ tính tay và unit checks. |
| 3 | Tải ML100K/ML1M/Amazon subset, đọc terms, dựng global-time split. | Manifest, dataset card, split hashes, kiểm tra leakage. |
| 4–5 | Tái lập MostPopular/ItemKNN/BPR; cache candidates; MMR/pop-penalty. | Benchmark chạy đầu-cuối, metrics kiểm chứng bằng toy. |
| 6 | Tái lập SMMR/ElasticRank/VRisker; audit metric definitions. | Baseline gần nhất, README/environment/commit, bảng validation. |
| 7–8 | Chốt formulation A, triển khai uncertainty/feasibility/repair; solver nhỏ. | Mã giả, complexity theo implementation, ablation hoạt động. |
| 9–10 | Hai dataset, seeds, sensitivity K/M và drift; thêm LightGCN nếu đủ thời gian. | Raw CSV, CI, frontier, subgroup, runtime/RAM. |
| 11 | Viết kết quả, hạn chế và đối chiếu gap; chọn phát hiện đáng công bố. | Draft luận văn/manuscript; kết luận theo phạm vi dữ liệu. |
| 12 | Rà soát citation/code/data, chạy lại từ README, phản biện giả lập. | Gói tái lập và bản thảo được sửa theo bằng chứng. |

Đây là kế hoạch mục tiêu, không phải cam kết thời gian huấn luyện. Bắt đầu đo runtime trên ML100K để lập ngân sách; cache scores/candidates để tránh train lại cho mỗi λ. Khi dùng 10 seeds, cost chủ yếu là số lần train backbone; reranker được đánh giá trên các cache tương ứng.

## 8.4. Bộ sản phẩm nên có khi viết luận văn/paper

Repo gồm downloader hợp lệ, preprocessing/split scripts, configs, implementation, metric definitions, toy checks, training/evaluation entry points, raw aggregate và per-user/per-batch metrics, figures và environment lock. README phải có một lệnh nhỏ để smoke test và lệnh tái tạo từng bảng chính.

Manuscript có: formalism và assumptions; đối chiếu mechanism-level với prior art; results không chọn lọc; ablation; CI đúng unit; compute budget; limitations/internal–external–construct–statistical validity. Nếu không có log randomized exposure, không tuyên bố hiệu quả nhân quả lên doanh thu, hài lòng hoặc giảm bất công xã hội.

**Tên luận văn dự kiến:** “Tái xếp hạng hệ gợi ý đa mục tiêu với ràng buộc cơ hội hiển thị dưới bất định độ phổ biến”. Tên tiếng Anh dự kiến: “Multi-Objective Recommendation Re-ranking with Exposure Constraints under Popularity Uncertainty”. Chỉ giữ cụm uncertainty trong tên nếu thí nghiệm thực sự chứng minh nó là thành phần có ích.
