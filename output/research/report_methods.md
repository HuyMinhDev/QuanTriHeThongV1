<pagebreak>

# 4. Tổng hợp khoảng trống và tài liệu cần đối chiếu thêm

## 4.1. Những gì đã có và khoảng trống còn kiểm chứng

| Ý định đề xuất | Tiền lệ gần nhất | Phần cần chứng minh thêm |
|---|---|---|
| Fairness hậu xử lý không retrain backbone | ElasticRank [10], PFA [1] | Khác biệt thuật toán, constraint và độ tin cậy dưới drift. |
| Phối hợp fairness cá thể và nhóm | SCRUF-D [9] | Tác dụng thêm của diversity/uncertainty; không chỉ thêm một agent. |
| Diversity có điều chỉnh trade-off | SMMR [11], CatDive [6], ADF [3] | Cơ chế thích nghi có lợi ở cùng tuning budget, đặc biệt cold users. |
| Diversity bảo vệ nhóm intent kém nhất | VRisker [5] | Relevance dự báo, uncertainty được hiệu chuẩn và exposure toàn hệ thống. |
| Công bằng bằng dual optimization | FairDual [14], FairSync [16] | Tính khả thi trong candidate pool và realized exposure của batch. |
| Đánh giá Pareto | DPFR [13], mở rộng [19] | Ba mục tiêu và frontier khả đạt trong cùng candidates, CI, độ bền thứ hạng. |
| Tăng accuracy–coverage bằng popularity correction | IPS-LAE [7] | Tăng ILD/exposure còn bao nhiêu sau baseline khử bias mạnh. |

**Kết luận có điều kiện:** có cơ sở nghiên cứu reranking dưới bất định và ràng buộc exposure, nhưng chưa có cơ sở nói “chưa ai đồng thời xét accuracy, diversity và fairness”. InFoDance [17] còn công bố đúng ba thành phần này ở khâu tăng cường dữ liệu. Tính mới cần dựa trên phát biểu hẹp, đối sánh cơ chế và thực nghiệm, không dựa vào việc đổi tên một tổng trọng số.

## 4.2. Tài liệu bổ trợ trực tiếp, không tính vào 14 bài mới

**TaxRank — “A Taxation Perspective for Fair Re-ranking”, SIGIR 2024 [15].** Thuế hóa utility và optimal transport để phân bổ item; code Python/CVXPY/OT tại [Tax-rank](https://github.com/XuChen0427/Tax-rank). Thử trên Yelp/iPinYou với BPR; so FairRec/+, P-MMF, Welf; đo eCN/eCPM/Gini/POT và latency. Bài cho đường trade-off, không có diversity constraint của đề tài. Hữu ích làm baseline OT nếu tài nguyên cho phép. DOI đúng: **10.1145/3626772.3657766**; README có thông tin citation không khớp bài gốc, nên dùng publisher/PDF.

**FairSync — “Ensuring Amortized Group Exposure in Distributed Recommendation Retrieval”, WWW 2024 [16].** Xử lý exposure ngay khâu retrieval bằng dual vector giữa shards; thử AmazonBook/Taobao, so regularized-fair, IPW, K-neighbor, Uncalibrated. Đo Recall/NDCG/HR và tỷ lệ nhóm đủ exposure tối thiểu (ESP). Code [FairSync](https://github.com/XuChen0427/FairSync) phụ thuộc TensorFlow GPU 1.x/Faiss GPU. Ý nghĩa cho luận văn: reranker không thể đưa lên item/nhóm chưa vào candidates; fairness retrieval chưa tự bảo đảm fairness ở danh sách hiển thị cuối.

**InFoDance, ACM TKDD 2025 [17].** Metadata và [repo](https://github.com/TYtianyang/infodance) đã xác minh; phương pháp dùng influence function để chọn dữ liệu ảo nhằm accuracy–fairness–diversity. Chưa phân tích đủ phương pháp thực nghiệm để thay một hồ sơ chính; giữ làm prior art bắt buộc đọc trước khi tuyên bố tính mới ba mục tiêu. Không ghi nhầm venue thành ACM TORS.

**UGAD/RUGAD, Expert Systems with Applications, online 2026 [18].** Kết hợp subprofiles của user với global item clusters, không cần metadata khi reranking. Preview cho biết có CiaoDVD, Amazon Beauty/Health, Steam, ML1M, Yelp và temporal splitting. Chưa có đủ full text/bảng kết quả hoặc code đã xác minh nên không suy ra baseline, ngôn ngữ hay mức tăng cụ thể. Bản issue có thể mang năm khác online; DOI là căn cứ nhận diện.

**DPFR mở rộng, tháng 10/2026 [19].** Tác giả ghi accepted ACM TORS, chưa xác minh DOI publisher riêng. Đọc để cập nhật robustness của Pareto evaluation; không đếm lặp với [13].

<pagebreak>

# 5. Thiết kế thực nghiệm đề nghị cho luận văn

Phần này là **đề xuất của báo cáo**, chưa phải một thực nghiệm đã chạy. Các ngưỡng, ngân sách và tham số bên dưới là lựa chọn nghiên cứu cần chốt trước khi mở test.

## 5.1. Dữ liệu, ngôn ngữ và lưu trữ

| Vai trò | Dữ liệu / nguồn | Xử lý và giới hạn |
|---|---|---|
| Kiểm tra pipeline | MovieLens 100K [24] | Dùng toy/debug; không xem đây là dữ liệu ngoài miền so với ML1M. |
| Benchmark chính 1 | MovieLens 1M [24] | Rating, timestamp, multi-label genres; rating≥4 là positive; không có giao dịch mua. |
| Benchmark chính 2 | Amazon Reviews 2018, Musical Instruments 5-core [25] | Nguồn ghi 231.392 reviews trước xử lý; ghép metadata category/brand, deduplicate user–item; số cuối do manifest ghi. |
| Stress / mở rộng | Amazon Reviews 2023 [26] hoặc time windows của hai tập chính | Chọn subset có đủ history và metadata; không tải toàn bộ 571 triệu reviews lên máy 16 GB. |

Chọn Python cho pipeline thống nhất: NumPy/pandas/SciPy cho dữ liệu/metrics; RecBole/PyTorch cho BPR/LightGCN; scikit-learn cho similarity và phân tích; PuLP/CBC hoặc OR-Tools cho oracle nhỏ. Đây là stack đề nghị, không phải khẳng định mọi repo trong khảo sát dùng cùng stack. Tách môi trường repo gốc Python 3.9 với môi trường benchmark chính; pin phiên bản thực sự đã cài chạy và commit SHA.

**“Cơ sở dữ liệu” thực nghiệm là benchmark dataset**, không bắt buộc MySQL/PostgreSQL. Lưu raw JSON/CSV ở chế độ chỉ đọc, processed interactions/candidates dạng Parquet/NumPy, configs YAML và metrics CSV. SQLite/DuckDB có thể dùng truy vấn kết quả, nhưng không tạo ra đóng góp thuật toán. Không cần dựng hệ quản trị cơ sở dữ liệu nặng chỉ để chạy MovieLens.

Với Amazon, dùng category ở một mức cây đã định trước và giữ multi-label nhất quán. Brand bị thiếu/không nhất quán phải có báo cáo tỷ lệ; không suy brand là merchant/seller. Fairness chính vẫn là item/popularity-group. Chỉ làm provider fairness khi có ánh xạ provider hợp lệ. Popularity là số tương tác **trong train**, không tính toàn bộ dữ liệu rồi chia nhóm.

Manifest cần có: dataset_name, release, source_url, download_date, license/terms_url, sha256, schema, counts trước/sau lọc, tỷ lệ thiếu metadata, positive rule, split boundaries, catalog eligibility và commit xử lý. Đọc điều kiện phân phối dữ liệu; công bố downloader và checksum thay vì mặc định đóng gói raw dataset vào repo.

## 5.2. Chia dữ liệu và tránh nhìn tương lai

**Giao thức chính:** global temporal split bằng hai mốc t1<t2, khoảng 70/10/20 theo timeline. Train chỉ chứa t≤t1; validation t1<t≤t2; test t>t2. Mọi statistics, eligibility, scaler, embeddings và popularity bins cho một giai đoạn chỉ dùng dữ liệu trước cutoff. Mốc thời gian được công bố trong manifest, không chỉ ghi tỷ lệ.

Chọn hyperparameters bằng validation; sau đó có thể fit lại train+validation ở cutoff t2 bằng cấu hình đã chốt, tính lại popularity theo dữ liệu trước t2 và đánh giá test đúng một lần. Nếu dùng refit, mọi baseline đều dùng cùng refit policy. Không dùng score/metric test để chọn θ, τ, λ, candidate size hoặc seed.

Protocol phụ để so với đề cương là per-user temporal 70/10/20, nhưng phải công bố rằng user-specific cutoffs có thể trộn tương lai của user này vào quá khứ của user khác. Kết luận robustness dựa thêm protocol global; không gọi per-user split là bảo đảm tuyệt đối không temporal leakage.

Main task là warm-start: user có đủ history, item đã có trước cutoff; loại mọi item user đã tương tác khỏi candidates. Cold users ở đây là **ít lịch sử đã biết**, không phải user mới hoàn toàn chưa có embedding. Nhóm 1–5, 6–20, >20 positive interactions hoặc quantile được chốt từ train, ghi số user thực. New-user/new-item hoàn toàn là kịch bản riêng với fallback/metadata model, không lẫn vào BPR warm-start rồi xóa âm thầm các ca thất bại.

Giữ riêng toàn bộ lịch sử tương tác trước cutoff, kể cả rating<4, để loại item đã thấy khỏi candidates; ngưỡng rating≥4 chỉ tạo nhãn positive cho huấn luyện/đánh giá. Deduplicate theo từng cutoff/window bằng một quy tắc đã chốt; không chọn bản ghi mới nhất trên toàn lịch sử rồi mới split, vì bản ghi tương lai có thể thay/xóa tương tác train. Nếu test là repeated interaction của item đã thấy thì không đưa vào main task gợi ý item mới và phải báo số ca bị loại.

Không dùng test để xây k-core lặp rồi cho rằng dữ liệu hoàn toàn không nhìn tương lai. Nếu dùng bản 5-core công bố sẵn, nêu rõ nó đã chọn theo toàn lịch sử; bổ sung sensitivity với lọc từ train/raw subset khi khả thi. Dùng rolling-origin 2–3 windows cho drift nếu số lượng tương tác cho phép.

## 5.3. Candidate pool và hai tầng đánh giá

Mỗi backbone sinh top-M từ **eligible catalog chưa tương tác**, mặc định M=100; sensitivity M=50/100/300/500, K=5/10/20. Không chèn test positive vào candidates. Tính full-catalog accuracy bằng chấm điểm theo block; không cần giữ ma trận user×item dày trong RAM.

Trong thí nghiệm reranking, tất cả policies trên cùng backbone dùng đúng candidate cache, score và metadata. Báo **candidate recall**, tỷ lệ item/nhóm có mặt trong candidates và tỷ lệ user có đủ diversity khả thi. Kết quả kém do retrieval khác kết quả kém do reranker; một quota không thể đạt không được ghi thành “thuật toán hội tụ chậm”.

Nếu nghiên cứu candidate enrichment, mở một track end-to-end riêng: so cả reranker và no-rerank trên cùng pool mở rộng, cùng tổng M và thời gian. Track shared-pool giữ nguyên để tách lợi ích do candidate recall tăng. Đánh giá fairness trên cả toàn eligible catalog lẫn union candidates; ghi rõ mẫu số, không loại item exposure=0 để làm đẹp Gini.

## 5.4. Baselines cần triển khai

| Tầng | Baseline | Mục đích / mức ưu tiên |
|---|---|---|
| Retrieval/relevance | MostPopular; ItemKNN | Sanity check và kiểm tra personalization; bắt buộc. |
| Retrieval/relevance | BPR-MF [20] | Backbone chính, phù hợp CPU/máy 16 GB. |
| Retrieval/relevance | LightGCN [21] | Kiểm chứng lợi ích không phụ thuộc backbone; cấu hình nhỏ hoặc GPU khi có. |
| Re-ranking | No-rerank | Mốc utility/exposure ban đầu. |
| Re-ranking | MMR [23]; xQuAD | Baseline diversity kinh điển; cùng similarity/category. |
| Re-ranking | Popularity penalty | Kiểm tra cơ chế mới có hơn một penalty đơn giản. |
| Re-ranking mới | SMMR [11]; ElasticRank [10] | Hai baseline gần nhất cần ưu tiên. |
| Re-ranking mới | VRisker [5] | Bảo vệ intent thiểu số; ước lượng intent từ train thay oracle ratings. |
| Mở rộng | SCRUF-D [9] hoặc PFA [1] | So cơ chế phối hợp fairness hoặc adaptation; ghi rõ có học thêm adapter. |
| Nhánh bổ sung | IPS-LAE [7]; CatDive [6] | IPS-LAE cho popularity; CatDive nếu nghiên cứu thêm SASRec/sequential. |

Để vừa tài nguyên, vòng đầu dùng BPR với no-rerank, MMR, popularity penalty, SMMR, ElasticRank, VRisker và proposed. Sau khi chốt pipeline mới mở LightGCN và một baseline nâng cao. Không phải tất cả 14 bài trong khảo sát đều là baseline có cùng nhiệm vụ: bài metric/toolkit không cần “huấn luyện” để đưa vào bảng thắng thua.

Cho mỗi baseline cùng số validation trials hoặc cùng ngân sách thời gian đã định, cùng số seeds và cùng candidate sizes. Với CatDive/PFA/FairDual, tách chi phí train/adapter khỏi inference. Nếu tái hiện thuật toán từ công thức thay code gốc, ghi “reimplementation” và kiểm tra toy/đối chiếu kết quả gốc ở phạm vi khả thi.

<pagebreak>

# 6. Các phép đo và cách báo cáo

## 6.1. Độ chính xác

Với Lᵤ là top-K, Tᵤ là positive items hợp lệ trong test, relᵤ,r∈{0,1} và wᵣ=1/log₂(r+1), r bắt đầu từ 1:

**Precision@K = |Lᵤ∩Tᵤ|/K; Recall@K = |Lᵤ∩Tᵤ|/|Tᵤ|.** Lấy macro-average theo user có |Tᵤ|>0 và báo số user bị loại do không có positive hợp lệ.

**DCG@K = Σᵣ₌₁ᴷ wᵣ·relᵤ,r; NDCG@K = DCG@K/IDCG@K**, IDCG lấy min(K,|Tᵤ|) positives. Nếu dùng graded relevance thì thay gain và giải thích; không trộn với score-retention NDCG của ElasticRank.

**MAP@K:** trung bình APᵤ@K = Σᵣ Precision@r·relᵤ,r / min(K,|Tᵤ|). Công bố mẫu số vì thư viện có thể dùng convention khác. HR hữu ích khi chỉ có một test positive, nhưng không thay Recall nếu test có nhiều positives.

**Relative NDCG loss = 1 − meanNDCG(proposed)/meanNDCG(base)**, nếu mẫu số >0. Báo thêm chênh lệch tuyệt đối. Đây là loss của hai macro-means, khác trung bình phần trăm loss từng user; phải nêu cách tính.

## 6.2. Đa dạng và độ phủ

**ILD@K = 2/[K(K−1)] · Σᵢ<ⱼ [1−sim(i,j)]**, với K≥2. Main similarity là Jaccard trên multi-label genre/category; có thể bổ sung cosine embeddings như sensitivity. Xử lý category rỗng theo một quy tắc đã chốt và báo tỷ lệ, không mặc định xem hai item thiếu metadata là cực kỳ khác nhau.

**Genre/category coverage@K** là số category khác nhau trong danh sách chia số category đủ điều kiện của dataset; báo thêm số category thô. Multi-label item được tính cho các category của nó trong phép đo này. **Catalog coverage@K** là |unionᵤ Lᵤ|/|I_eligible|; hai độ phủ có mẫu số khác nhau.

**Category entropy:** phân phối khối lượng 1/|genres(i)| cho mỗi nhãn của item rồi chuẩn hóa tổng khối lượng trong danh sách; entropy chia log|G| nếu |G|>1. **Inter-list diversity** có thể báo thêm 1−Jaccard giữa cặp danh sách user, cùng cách lấy mẫu cặp; không thay ILD.

Novelty/self-information hoặc average recommendation popularity là metrics phụ, tính từ train và có smoothing cho count=0. Thêm chỉ số này không tự chứng minh người dùng thật nhận được khám phá có ích.

## 6.3. Exposure và mục tiêu fairness

**Exposure item eᵢ = Σᵤ Σᵣ wᵣ·1[πᵤ(r)=i].** Đây là proxy attention theo vị trí, không phải số lượt xem đo thực tế. Kiểm tra sensitivity với wᵣ=1 và một discount khác; không tự tuyên bố discount là xác suất click đã hiệu chuẩn.

**Gini exposure = ΣᵢΣⱼ|eᵢ−eⱼ| / [2·n·Σᵢeᵢ]**, n=|I_eligible|, tổng exposure>0. Giữ item không xuất hiện với eᵢ=0; dùng công thức từ exposure đã sort để tránh O(n²). Gini thấp biểu thị ít tập trung hơn, chưa xác định một chính sách công bằng đúng về mặt chuẩn tắc.

**Head exposure share = Σᵢ∈Head eᵢ / Σᵢeᵢ**, Head là top 10% item theo train counts, có tie-breaking cố định. Báo head/mid/tail theo **số item** và quy tắc phân nhóm; không đổi qua các thuật toán. Đây là fairness theo popularity, không phải theo nhóm xã hội.

Nếu target t_g≥0, Σ_g t_g=1, đặt p_g=E_g/Σ_hE_h và **exposure gap = ½Σ_g|p_g−t_g|**. Target có thể equal-per-item, equal-per-group hoặc proportional-to-merit; phải chọn và biện minh trước. Với category chồng lấp, phân bổ exposure theo fractional membership để không đếm trùng. Target từ popularity lịch sử có thể bảo tồn bias, nên cần sensitivity với target khác.

**Violation** đối với upper budget θ: max(0, head_share−θ); đối với diversity minimum τᵤ: max(0,τᵤ−Dᵤ). Báo mean/max, tỷ lệ user/batch vi phạm, tỷ lệ bài toán vô nghiệm và slack cần thiết. Một penalty mềm hoặc dual update không bảo đảm hard quota sau mỗi batch.

## 6.4. Pareto, subgroup và tài nguyên

Giữ riêng ba trục: NDCG↑, ILD↑ và exposure gap/Gini↓. Một nghiệm Pareto không bị nghiệm khác tốt hơn hoặc bằng trên mọi trục và tốt hơn ít nhất một trục. Vẽ scatter/frontier tại các settings đã chốt; nếu dùng hypervolume, chuẩn hóa và reference point cố định **trước** khi so thuật toán. Chọn điểm vận hành trên validation, không chọn điểm đẹp nhất từ test.

DPFR [13] là phép đánh giá hai mục tiêu; không tự gọi một phép ghép ba metric là “DPFR ba chiều đã được chứng minh”. Oracle dựa test chỉ làm upper bound hậu kiểm. Oracle giới hạn cùng candidates giúp phân biệt retrieval bottleneck với chất lượng reranker.

Đo latency rerank p50/p95/p99 theo ms/user, throughput users/s, thời gian huấn luyện, thời gian tạo candidates, peak RAM và kích thước cache. Chỉ báo p99 khi đủ lượt đo; warm-up riêng, cùng phần cứng và thread count. Không đặt latency M2 một luồng từ VRisker cạnh latency GPU của bài khác để suy thuật toán nhanh hơn.

Cold-user subgroup, head/tail items và missing-metadata subgroup phải có số mẫu, accuracy và fairness/diversity cùng nhau. Coverage/Gini là **metric toàn tập**, không tạo “per-user Gini” rồi xem như cùng đại lượng.

## 6.5. Thống kê và bảng kết quả

Dùng seeds 1001–1010 khi khả thi, lưu kết quả cả 10, không chọn seed đẹp. Báo mean±SD qua training seeds. Với accuracy theo user, paired bootstrap user IDs cho chênh lệch proposed−baseline; cùng bộ user resamples cho hai thuật toán. Không gộp 10 lần dự đoán của cùng user thành 10 quan sát độc lập.

Với exposure quota liên kết users trong batch, bootstrap các unit độc lập đã định trước như batch/time window, hoặc chạy lại policy cho từng resample. Bootstrap cố định predictions chỉ phản ánh bất định đánh giá có điều kiện, không toàn bộ độ ngẫu nhiên của huấn luyện/policy. Dùng hierarchical bootstrap khi đủ số seed/window; nếu không đủ, mô tả giới hạn CI thay vì báo một CI giả chính xác.

Chốt primary endpoints, RQs và cách điều chỉnh nhiều so sánh (ví dụ Holm cho một họ giả thuyết). Báo effect size và CI, không chỉ p-value. Non-inferiority accuracy budget 3% là **ngưỡng đề nghị** cần đăng ký trước: kết luận giữ accuracy chỉ khi CI của relative loss đáp ứng margin; không suy từ “p>0,05” thành tương đương.

| Bảng/hình cần có | Nội dung |
|---|---|
| Dataset card | Counts, sparsity, time boundaries, metadata, eligibility, license, checksum. |
| Kết quả chính | Mean±SD, CI chênh lệch, NDCG/Recall/ILD/coverage/Gini/gap, latency/RAM. |
| Ablation | Bỏ uncertainty, diversity, exposure, adaptation, candidate enrichment. |
| Subgroup | Cold/warm users, head/tail items, missing metadata; số mẫu và CI. |
| Trade-off | Frontier, accuracy budget, sensitivity K/M/θ/τ, runtime. |
| Failure cases | Infeasible quotas, relevance loss lớn, user-order effects, drift. |
