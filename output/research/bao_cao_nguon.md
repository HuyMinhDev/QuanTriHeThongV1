# 1. Kết luận định hướng cho đề tài

Đề tài trong PDF là **“Hệ gợi ý thương mại điện tử đa mục tiêu cân bằng độ chính xác, đa dạng và công bằng hiển thị sản phẩm”**, với trọng tâm **reranking sau mô hình relevance**, không phải xây một mô hình dự báo điểm mới từ đầu. Đầu ra nghiên cứu cần là đánh đổi có thể kiểm chứng giữa accuracy, diversity và exposure, cùng chi phí tính toán và mức tác động tới người dùng ít lịch sử.

Báo cáo lựa chọn **14 công trình trọng tâm có bản công bố năm 2025–2026**, gồm 6 bài năm 2026 và 8 bài năm 2025 theo metadata bản công bố được dùng. Mỗi bài có đường dẫn bài gốc/toàn văn, mã nguồn chính thức, thiết lập thực nghiệm, kết quả, hạn chế và đề xuất phát triển. Riêng bài LLM [8] có tiền ấn phẩm từ 2024; năm bản publisher không có nghĩa ý tưởng xuất hiện lần đầu năm 2025. Các nguồn nền tảng 2009–2024 được tách ở phần bổ trợ, không dùng để đủ số lượng bài mới.

**Hướng nên ưu tiên cho máy 16 GB:** đóng băng BPR-MF, xây reranker có kiểm tra tính khả thi, diversity theo user và exposure theo batch, rồi nghiên cứu độ bất định của popularity dưới temporal drift. So trực tiếp với MMR, SMMR [11], ElasticRank [10] và VRisker [5]; thêm PFA [1] hoặc SCRUF-D [9] khi đã tái lập được. RecBole và FairDiverse [12] hỗ trợ dùng chung pipeline, nhưng cần kiểm tra lại split và định nghĩa metrics.

**Tính mới hiện chưa được xác lập.** Adaptive weights, tối ưu đối ngẫu, fair reranking, Pareto evaluation và phối hợp nhiều mục tiêu đều đã có tiền lệ. Hướng luận văn cần thu hẹp thành một cơ chế mới có đối sánh gần nhất, hoặc một phát hiện thực nghiệm đủ mạnh và tái lập được. Việc cộng thêm λ·diversity−μ·popularity vào điểm BPR, tự nó, khó tạo đóng góp mới.

## 1.1. Lộ trình đọc ưu tiên

| Ưu tiên | Tài liệu | Mục đích khi đọc |
|---|---|---|
| 1 | ElasticRank [10], PFA [1] | Xác định fair reranking/adaptation gần nhất; tránh đề xuất lại cơ chế đã có. |
| 2 | SMMR [11], VRisker [5] | Có baseline diversity/risk mới, tương đối phù hợp tài nguyên nhỏ. |
| 3 | DPFR [13], fairness metrics [4] | Chọn metric và tránh kết luận sai từ một điểm tổng hợp. |
| 4 | SCRUF-D [9], CatDive [6] | Đối chiếu phối hợp fairness agents, category diversity và cá nhân hóa. |
| 5 | FairDiverse [12], IPS-LAE [7] | Chuẩn hóa benchmark; có baseline khử thiên lệch popularity. |
| 6 | FairDual [14], ADF [3], LLM [8], giải thích [2] | Mở rộng lý thuyết/ứng dụng sau khi pipeline chính ổn định. |

## 1.2. Cách đọc kết quả trong báo cáo

- **Kết quả đã công bố** là trị số của tác giả trên thiết lập của bài đó; báo cáo này chưa chạy tái lập mã nguồn.
- **Hạn chế do tác giả nêu** được ghi rõ. Các mục “nhận xét đối với đề tài” là phân tích của báo cáo, không gán thành lời tác giả.
- **Hướng cải tiến** là giả thuyết cần kiểm chứng; không phải kết quả đạt được hoặc bảo đảm được nhận đăng.
- Số liệu giữa các bài có dataset, split, candidate pool hoặc gain khác nhau **không được xếp hạng trực tiếp**. Dấu phẩy thập phân được dùng trong phần diễn giải tiếng Việt.

<pagebreak>

# 2. Phạm vi và phương pháp tìm tài liệu

## 2.1. Phát biểu phạm vi từ PDF

Đầu vào gồm lịch sử tương tác, điểm relevance s(u,i), metadata category/genre và popularity tính trên train. Từ top-M candidates, tạo top-K cho mỗi user, vừa giữ relevance vừa tăng diversity và kiểm soát tập trung exposure trên toàn user/batch. PDF yêu cầu MovieLens 100K/1M, temporal split, MostPopular/ItemKNN/BPR/LightGCN, MMR/popularity penalty, K=5/10/20, seeds 1001–1010, ablation và CI.

Phạm vi fairness được chốt là **cơ hội xuất hiện của item/nhóm item**, không suy thành demographic fairness. MovieLens là benchmark phương pháp; muốn kết luận cho thương mại điện tử cần thêm dữ liệu sản phẩm. Interaction/rating là tín hiệu quan sát, không phải xác suất hài lòng hoặc mua hàng đã được xác định nhân quả.

## 2.2. Tìm kiếm và sàng lọc

Ngày rà soát: **15/11/2026**. Đây là khảo sát có mục tiêu dựa trên nguồn truy cập được, không phải systematic review bao phủ toàn bộ cơ sở dữ liệu và không khẳng định đã tìm hết mọi bài mới nhất trên thế giới.

Các truy vấn đã dùng gồm: “recommendation reranking accuracy diversity exposure fairness 2025 2026 SIGIR code”; “2026 recommender reranking diversity fairness exposure paper code”; “2025 2026 recommendation uncertainty popularity re-ranking”; “FairDiverse toolkit paper”; “Joint Fairness Relevance recommender”; cùng tìm tên chính xác/DOI và trang hội nghị của các ứng viên.

Nguồn ưu tiên là ACM/ICLR/PLOS, PDF tác giả, kho đại học, arXiv của đúng công trình, tài liệu dataset gốc và GitHub của tác giả. ArXiv chỉ cung cấp toàn văn/phiên bản; **bằng chứng bình duyệt lấy từ bản công bố hoặc proceedings**, không từ việc có mặt trên arXiv. Không dùng bài tóm tắt tự động làm căn cứ số liệu.

Tiêu chí chọn: liên quan trực tiếp ít nhất một khâu của cân bằng relevance–diversity–exposure hoặc đánh giá đánh đổi; ưu tiên 2025–2026; có nguồn công bố xác minh được; đủ phương pháp/thực nghiệm để phân tích; ưu tiên code chính thức. Toolkit và bài metric được giữ vì cần thiết cho thiết kế benchmark, nhưng ghi đúng vai trò. “Uy tín” được xét theo nguồn xuất bản và khả năng kiểm tra, không tự gán Q1/Q2, CORE hay số trích dẫn chưa xác minh.

## 2.3. Mức độ kiểm tra và giới hạn bằng chứng

Đã đọc/đối chiếu các phần abstract, phương pháp, thực nghiệm và hạn chế từ toàn văn hoặc phần nội dung publisher truy cập được, cùng README của repo. Khi không xác minh được split, phiên bản thư viện hoặc code bao phủ đầy đủ thí nghiệm, báo cáo ghi rõ. Repo tồn tại không đồng nghĩa cài chạy thành công; chưa huấn luyện lại mô hình nào trong phạm vi tài liệu này.

Những trường hợp thiếu toàn văn được để ở nhóm đọc tiếp: UGAD/RUGAD [18] có preview nhưng chưa đủ bảng kết quả; InFoDance [17] đã xác minh metadata và repo nhưng chưa phân tích đủ thực nghiệm. Bản mở rộng DPFR tháng 10/2026 [19] được gộp dòng nghiên cứu. PreferRec arXiv:2603.22073 và một số tiền ấn phẩm 2026 chưa xác minh venue nên không tính vào 14 bài chính.

## 2.4. Năm khái niệm cần tách rõ

| Khái niệm | Đối tượng đo | Không đủ để kết luận |
|---|---|---|
| Held-out accuracy | Item positive trong tập kiểm thử | Không đo trực tiếp doanh thu/hài lòng thực. |
| Intra-list diversity | Mức khác nhau giữa item trong cùng một danh sách | Không chứng minh exposure toàn catalog cân bằng. |
| Inter-list diversity | Mức khác nhau giữa danh sách của các users | Không thay thế ILD hoặc cá nhân hóa tốt. |
| Catalog coverage | Số item được xuất hiện ít nhất một lần | Không xét đủ số lần/vị trí; coverage cao vẫn có thể tập trung mạnh. |
| Exposure fairness | Phân bố chú ý theo item/nhóm, đối chiếu target | Target phải minh bạch; bình đẳng và proportional-to-merit là hai lựa chọn khác nhau. |

<pagebreak>

# 3. Danh sách 14 công trình trọng tâm

Các số [1]–[14] dùng thống nhất cho hồ sơ chi tiết và danh mục tài liệu tham khảo. Bài được sắp theo nhóm thời gian và vai trò, không theo thứ hạng chất lượng thuật toán.

| Mã | Năm / nơi công bố | Công trình / phương pháp | Vai trò sát đề tài |
|---|---|---|---|
| [1] | 2026 / SIGIR | PFA–HEFA | Provider exposure; adapter sau huấn luyện. |
| [2] | 2026 / UMAP | Behind the Re-Rank | Giải thích tác động của fair reranking. |
| [3] | 2026 / ACM TORS | ADF | Relevance–diversity–user calibration; khác provider fairness. |
| [4] | 2026 / ACM TORS | Relevance-aware item fairness measures | Tính hợp lệ và giới hạn của metric. |
| [5] | 2026 / WSDM | VRisk / VRisker | Diversity theo rủi ro của intent thiểu số. |
| [6] | 2026 / PLOS ONE | CatDive | Category diversity; sequential recommendation. |
| [7] | 2025 / SIGIR-AP | IPS-LAE | Accuracy–coverage; popularity correction. |
| [8] | 2025 / ACM TORS | LLM diversity reranking | So prompt-based reranking với greedy. |
| [9] | 2025 / RecSys | SCRUF-D / social choice | Kết hợp individual và group fairness. |
| [10] | 2025 / SIGIR | ElasticRank | Relevance-score retention–group fairness. |
| [11] | 2025 / SIGIR | SMMR | Sampling MMR; coverage và inter-list diversity. |
| [12] | 2025 / SIGIR | FairDiverse | Toolkit và benchmark fairness/diversity. |
| [13] | 2025 / WWW | DPFR / Oracle2Fair | Đánh giá frontier relevance–fairness. |
| [14] | 2025 / ICLR | FairDual | Max-min fairness và Jensen gap khi training. |

Tất cả 14 hồ sơ đều có link mã nguồn do tác giả/nhóm công bố. Mức hoàn chỉnh khác nhau: FairDual mới công bố một nhánh chính; một số repo phụ thuộc môi trường cũ, solver hoặc GPU. Điều này được ghi tại từng hồ sơ để lên kế hoạch tái lập phù hợp.


<pagebreak>

## 3.1. [1] PFA / HEFA

**Post-hoc Provider Fairness Adaptation via Hierarchical Exposure Alignment**

Jingzhi Li; Zhiyong Cheng; Richang Hong; Meng Wang

ACM SIGIR 2026

[Bài/toàn văn](https://arxiv.org/html/2605.01524v1) | [Code](https://github.com/Tam-JQK/Post-train)

**Bài toán và phương pháp:** Điều chỉnh công bằng nhà cung cấp mà không huấn luyện lại backbone. PFA học adapter trên điểm của mô hình đóng băng; HEFA phối hợp cân bằng giữa nhóm và trong nhóm với mục tiêu relevance khả vi.

**Dữ liệu và protocol:** Amazon Beauty, Amazon Movies & TV, RateBeer; provider là brand/brewer. Lọc 5-core; random split theo user 70/10/20; 3 lần chạy; K=20.

**Baselines:** BPRMF, LightGCN, SGL; SDRO, Multi-FR, Ada2Fair, FairDual, FairRec, CPFair, TaxRank, ElasticRank.

**Phép đo:** NDCG/HR/MRR; provider Gini/Entropy/CV.

**Kết quả đã công bố:** Bảng 2, Beauty+BPR: NDCG/Gini 0,1000/0,7260 → 0,0943/0,6282. Bảng 3, Beauty+LightGCN: 0,1254/0,7102 → 0,1204/0,6428. Cải thiện cân bằng exposure đi kèm giảm NDCG trong hai cấu hình này.

**Ngôn ngữ, code và môi trường:** Python/PyTorch; bài dùng RTX 4080, embedding 32, batch 256. Đã xác minh repo; chưa chạy tái lập.

**Hạn chế và phạm vi kết luận:** Nhận xét đối với đề tài: chưa có mục tiêu ILD trực tiếp; random split chưa kiểm chứng dịch chuyển theo thời gian. Adapter linh hoạt đã có tiền lệ, nên không đủ làm tuyên bố mới riêng.

**Hướng cải tiến đề xuất:** Thử adapter/reranker có ràng buộc diversity và exposure dưới temporal drift; đối sánh cùng backbone, candidate pool và ngân sách tuning. Bác bỏ hướng này nếu lợi ích biến mất khi đổi random split sang temporal split.

**Điểm cần kiểm tra khi tái lập:** Paper chia nhóm theo training exposure; README mô tả theo item count. Đây là khác biệt tài liệu cần kiểm tra ở implementation, chưa phải bằng chứng code sai.

<pagebreak>

## 3.2. [2] Behind the Re-Rank

**Behind the Re-Rank: Explaining Fairness in Top-N Recommendations**

Raciel Yera; Luis Martínez

ACM UMAP 2026, tr. 21–29

[Bài/toàn văn](https://ruja.ujaen.es/server/api/core/bitstreams/78628cee-deca-474f-9dad-ca0bd6fc0e8c/content) | [Code](https://github.com/ryera/fairness-explanation-topn)

**Bài toán và phương pháp:** Giải thích item/thể loại nào được nâng hoặc hạ khi áp ràng buộc fairness. Dùng tối ưu reranking và cây quyết định suy ra quy tắc, sau đó đánh giá cách diễn đạt giải thích.

**Dữ liệu và protocol:** MovieLens 1M, HetRec2011, Yelp Philadelphia; hold-out 80/20 cho recommendation. Riêng kiểm tra khả năng khái quát quy tắc: user discovery/validation 60/40. User study N=54.

**Baselines:** MF và VAECF trong Cornac; fairness Sym/Cal/Exp; giải thích generic, granular demotion, side-effect promotion; top-50 → top-5/10.

**Phép đo:** NDCG utility loss, fidelity, thuộc tính bị hy sinh; thang đo cảm nhận trong user study.

**Kết quả đã công bố:** Bảng 1: ML1M, MF@10, Action, λ=0,8: utility loss +11,0%, fidelity 0,779. Cách mô tả trực tiếp item bị hạ có thể giảm hài lòng; framing khám phá/đa dạng giảm tác động này.

**Ngôn ngữ, code và môi trường:** Python 3, Cornac, pandas, NumPy, PuLP/CBC, scikit-learn. Repo có script, bảng kết quả, tài liệu khảo sát và MIT license; chưa chạy lại.

**Hạn chế và phạm vi kết luận:** Tác giả: user study chỉ ở miền nhà hàng, cỡ mẫu vừa và ngắn hạn. Nhận xét: đây là đóng góp giải thích, không phải bằng chứng một thuật toán tối ưu ba mục tiêu mới.

**Hướng cải tiến đề xuất:** Sau khi có reranker ổn định, khảo sát giải thích đánh đổi exposure bằng tiếng Việt. Đo fidelity, mức hiểu đúng và hài lòng riêng; không diễn đạt gây hiểu lầm rằng mọi thay đổi fairness đều tăng lợi ích cá nhân.

**Điểm cần kiểm tra khi tái lập:** PDF tác giả còn DOI placeholder; DOI hoàn chỉnh lấy từ repo và đối chiếu chương trình UMAP 2026. Không dùng placeholder làm trích dẫn.

<pagebreak>

## 3.3. [3] ADF

**Shift your Focus for the Greater Good: Improving Fairness at no cost for Accuracy and Diversity in News Recommender Systems**

Célina Treuillier; Sylvain Castagnos; Evan Dufraisse; Özlem Özgöbek; Armelle Brun

ACM Transactions on Recommender Systems 4(3), Article 44, 1–36; online 05/03/2026

[Bài/toàn văn](https://doi.org/10.1145/3790097) | [Code](https://github.com/celinatreuillier/ADF_framework)

**Bài toán và phương pháp:** Điều chỉnh phân bố khía cạnh/chủ đề đề xuất theo sở thích của user, kết hợp relevance và diversity. Fairness ở đây là tương thích với người dùng, không phải phân phối exposure sản phẩm toàn hệ thống.

**Dữ liệu và protocol:** MIND, Adressa; chia theo thời gian bằng NewsRecLib; lọc user test có ít nhất 5 tương tác. Adressa dùng 5 ngày đầu train; ngày cuối chia validation/test; sampled negatives 20/click.

**Baselines:** CentroidVector, LSTUR, NAML, NPA, NRMS; greedy diversification và calibrated recommendation.

**Phép đo:** Precision@20, content ILD, topic SRecall, CH/Hellinger calibration.

**Kết quả đã công bố:** §5.3.2, Hình 7–8: MIND+NAML Precision@20 khoảng 0,100 → 0,092 tại α=0,4; Adressa+NAML 0,081 → 0,105 tại α=0,6. Tiêu đề ‘no cost’ không có nghĩa accuracy luôn được giữ ở mọi cấu hình.

**Ngôn ngữ, code và môi trường:** Python, ClayRS/NewsRecLib, spaCy, tomotopy; LDA cho MIND và bge-m3 cho Adressa. Link code tác giả đã kiểm tra; chưa tái lập.

**Hạn chế và phạm vi kết luận:** Tác giả: dữ liệu lịch sử, đánh giá offline, metric còn hẹp; cần user study. Nhận xét: không suy từ calibration tốt sang exposure fairness hay hiệu quả thương mại điện tử.

**Hướng cải tiến đề xuất:** Giữ calibration theo user nhưng thêm exposure budget theo item/nhóm phổ biến trên toàn batch. Thực nghiệm xem hai mục tiêu hỗ trợ hay xung đột ở cold users; luôn báo cả calibration gap và exposure gap.

**Điểm cần kiểm tra khi tái lập:** Không chuyển nhãn ‘fairness’ trong bài thành fairness nhà cung cấp. Các trị số đọc từ hình được ghi ‘khoảng’; không coi là số đo có thêm độ chính xác.

<pagebreak>

## 3.4. [4] Relevance-aware fairness metrics

**Relevance-aware Individual Item Fairness Measures for Recommender Systems: Limitations and Usage Guidelines**

Theresia Veronika Rampisela; Maria Maistro; Tuukka Ruotsalo; Falk Scholer; Christina Lioma

ACM Transactions on Recommender Systems 4(3), Article 37, 45 trang; online 05/03/2026

[Bài/toàn văn](https://doi.org/10.1145/3765624) | [Code](https://github.com/theresiavr/relevance-aware-item-fairness-measures-recsys)

**Bài toán và phương pháp:** Phân tích các metric fairness item có điều kiện relevance; chỉ ra non-realisability, non-localisation, undefinedness, zero-exposure và top-k-insensitivity; hiệu chỉnh những trường hợp có thể sửa.

**Dữ liệu và protocol:** Lastfm, Amazon Luxury Beauty, QK-video, MovieLens 10M và dữ liệu tổng hợp. Chọn mô hình bằng NDCG@10 validation; chưa xác minh đầy đủ split cho mọi dataset từ nguồn đã truy cập.

**Baselines:** ItemKNN, BPR, MultiVAE, NCL, COMBMNZ; so metric gốc với metric hiệu chỉnh, relevance-only và exposure-only metrics.

**Phép đo:** Các joint relevance–fairness measures và phản ứng trước biến đổi ranking/zero exposure.

**Kết quả đã công bố:** §6.3: trong phép thử được thiết kế, các bản sửa đạt điểm fairness tối ưu lý thuyết 0, trong khi một số bản gốc không đạt. Đây là kết quả về tính chất metric, không phải mức tăng accuracy của recommender.

**Ngôn ngữ, code và môi trường:** Python/notebook, RecBole; repo chính thức cung cấp mã đánh giá. Bản tác giả có trong luận án Rampisela, Chương 4; chưa chạy lại.

**Hạn chế và phạm vi kết luận:** Phạm vi chủ yếu là binary relevance và single-round/deterministic rankings. Nhận xét: không đại diện mọi định nghĩa fairness nhóm, multi-round hay cảm nhận công bằng của người dùng.

**Hướng cải tiến đề xuất:** Làm robustness study khi nhãn bị thiếu, thay đổi head/tail và popularity drift. Kiểm tra liệu thứ hạng thuật toán theo metric có đảo chiều; đối chiếu với NDCG, ILD và exposure thay vì gộp thành một điểm tùy ý.

**Điểm cần kiểm tra khi tái lập:** Là bản mở rộng dòng SIGIR 2024 ‘Can We Trust Recommender System Fairness Evaluation?’. Báo cáo không đếm bản 2024 thành một công trình độc lập nữa.

<pagebreak>

## 3.5. [5] VRisk / VRisker

**Diversification as Risk Minimization**

Rikiya Takehi; Fernando Diaz; Tetsuya Sakai

ACM WSDM 2026, tr. 618–628

[Bài/toàn văn](https://arxiv.org/html/2510.22681v1) | [Code](https://github.com/RikiyaT/VRisk)

**Bài toán và phương pháp:** Tối ưu relevance trung bình có thể bỏ qua ý định thiểu số. VRisk dùng CVaR của phần intent được phục vụ kém nhất; VRisker dùng greedy để giảm rủi ro.

**Dữ liệu và protocol:** NTCIR INTENT-2, TREC Web 2012, MovieLens 32M. MovieLens: 42.902 users, 71.933 items; user có >200 ratings; genre là intent. Chỉ đánh giá reranking trên ratings, không huấn luyện recommender hoặc temporal split.

**Baselines:** Naive, IW-Greedy, xQuAD, MMR, IA-SELECT, FA*IR, Calibrated Recommendations.

**Phép đo:** VRisk, AvgRel, DCG/nDCG/ERR/RBP/Precision; mặc định K=10, worst-intent fraction β=0,10; CI 95%.

**Kết quả đã công bố:** Hình 9, MovieLens: VRisk 0,77, utility 0,94 với Naive=1. Hình 8: 7,84 ms/query trên M2, RAM 16 GB. Con số 33% giảm risk/2% mất utility trong abstract thuộc INTENT-2, không gán cho MovieLens.

**Ngôn ngữ, code và môi trường:** Code Python, NumPy/BLAS một luồng; đo trên MacBook Pro M2 (2022), 16 GB. Có PDF tác giả https://841.io/doc/vrisker.pdf; chưa chạy lại.

**Hạn chế và phạm vi kết luận:** Intent cần được ước lượng; giả định intent loại trừ nhau. Nhận xét: oracle-like relevance từ ratings chưa chứng minh hiệu quả với điểm dự báo; chưa có exposure constraint toàn hệ thống.

**Hướng cải tiến đề xuất:** Chạy VRisker trên điểm BPR với temporal split và nhóm user ít lịch sử. Bổ sung exposure budget rồi so với VRisker nguyên bản; phân biệt bất định relevance, bất định intent và bất định popularity.

**Điểm cần kiểm tra khi tái lập:** Bảo đảm greedy phụ thuộc loại utility và giả định trong định lý; không ghi bảo đảm 1−1/e cho mọi biến thể nDCG hoặc mọi ràng buộc thêm vào.

<pagebreak>

## 3.6. [6] CatDive

**CatDive: A simple yet effective method for maximizing category diversity in sequential recommendation**

Jaeri Lee; Jongjin Kim; U Kang

PLOS ONE 21(1), e0341419; 30/01/2026

[Bài/toàn văn](https://journals.plos.org/plosone/article?id=10.1371/journal.pone.0341419) | [Code](https://github.com/snudatalab/CatDive)

**Bài toán và phương pháp:** Cân bằng accuracy–category diversity bằng embedding category, category-weighted negative sampling và reranking ưu tiên độ phủ rồi điền các item phù hợp.

**Dữ liệu và protocol:** Amazon Books, Kindle Store, Goodreads Romance; last-timestamp leave-one-out; K=10/20. Books: 8.685 users, 9.053 items, 26 categories; Kindle 17 và Romance 44 categories.

**Baselines:** SASRec backbone; GRU4Rec, SASRec, MCPRN, MMR, ComiRec.

**Phép đo:** HR, nDCG, ILD, category coverage.

**Kết quả đã công bố:** Bài báo nêu các điểm Pareto tốt hơn, không phải một cấu hình tăng mọi metric. Demo Books trong README: NDCG@10/ILD/coverage 0,1066/0,5947/0,1213 → 0,1041/0,6839/0,1562 với λ=0,1; accuracy có giảm.

**Ngôn ngữ, code và môi trường:** Python 3.8+, PyTorch; repo có dữ liệu/hướng dẫn/pretrained demo. Trị số demo lấy từ README, không phải kết quả chạy mới của báo cáo.

**Hạn chế và phạm vi kết luận:** Chưa ràng buộc exposure sản phẩm toàn catalog. Tham số diversity dùng chung chưa tự động cá nhân hóa; bản đầy đủ gồm cả thay đổi training nên không quy hết lợi ích cho reranking.

**Hướng cải tiến đề xuất:** Tách ablation training và reranking; thử tham số phụ thuộc độ bất định lịch sử user, kết hợp exposure toàn batch. So trên cùng SASRec checkpoint trước, sau đó mới so khác backbone.

**Điểm cần kiểm tra khi tái lập:** Category coverage của một danh sách khác catalog coverage toàn hệ thống; phải giữ nguyên mẫu số và đơn vị trong bảng kết quả.

<pagebreak>

## 3.7. [7] IPS-LAE

**Accurate and Diverse Recommendations via Propensity-Weighted Linear Autoencoders**

Kazuma Onishi; Katsuhiko Hayashi; Hidetaka Kamigaito

ACM SIGIR-AP 2025; công bố 06/12/2025

[Bài/toàn văn](https://arxiv.org/html/2512.20896v1) | [Code](https://github.com/cars1015/IPS-LAE)

**Bài toán và phương pháp:** Tăng coverage bằng inverse propensity weights cho đầu ra linear autoencoder. Propensity là hàm tần suất tương tác; nghiệm trọng số có thể cập nhật hậu xử lý.

**Dữ liệu và protocol:** MovieLens 20M, Netflix, Million Song Dataset; user-disjoint train/validation/test theo protocol strong generalization của MultVAE; không tương đương temporal split theo user.

**Baselines:** EASE, EDLAE, RDLAE, SANSA với nhiều mật độ ma trận.

**Phép đo:** Recall@20/50, NDCG@100, Coverage@100.

**Kết quả đã công bố:** Bảng 1, ML20M–EASE: NDCG@100 0,4203 → 0,4217; coverage 0,2134 → 0,7133. EDLAE: 0,4240/0,2152 → 0,4253/0,7585. Không suy từ coverage sang exposure fairness.

**Ngôn ngữ, code và môi trường:** Python, NumPy/SciPy, môi trường conda; Apache-2.0. Mã chính thức hỗ trợ weighted/unweighted variants; chưa tái lập.

**Hạn chế và phạm vi kết luận:** Nhận xét: frequency-based propensity không tự xác định được xác suất exposure nhân quả; không tối ưu ILD hay quota. Ma trận item×item dày gây giới hạn bộ nhớ khi catalog lớn.

**Hướng cải tiến đề xuất:** Dùng IPS-LAE làm baseline popularity correction, sau đó thêm exposure budget/ILD để kiểm tra phần tăng thêm. Chạy ML1M hoặc sparse SANSA; đo peak RAM và độ nhạy của trọng số với dữ liệu thiếu.

**Điểm cần kiểm tra khi tái lập:** Các con số bảng gốc thuộc strong generalization; phải huấn luyện lại cùng split luận văn trước khi so số tuyệt đối với BPR/LightGCN.

<pagebreak>

## 3.8. [8] LLM diversity reranking

**Enhancing Recommendation Diversity by Re-ranking with Large Language Models**

Diego Carraro; Derek Bridge

ACM Transactions on Recommender Systems 4(2), Article 18, 1–40; trang publisher hiển thị 22/11/2025

[Bài/toàn văn](https://arxiv.org/html/2401.11506v2) | [Code](https://github.com/cdiego89phd/chat-reranking)

**Bài toán và phương pháp:** Zero-shot prompt LLM tái xếp hạng top-40/50 thành top-10 để tăng diversity. Tám template thay đổi chỉ dẫn, genre và mô tả item.

**Dữ liệu và protocol:** Anime, Goodreads; random 80/20 user-based theo mô tả bài, lấy thêm validation từ train; đánh giá 500 test users. Không mô tả thành temporal split.

**Baselines:** MF/RankSys; MMR, xQuAD, RxQuAD, Random; ChatGPT, InstructGPT, Llama2-Chat 7B/13B.

**Phép đo:** NDCG@10, α-NDCG, ILD, EILD, SRecall/rSRecall, CI 95%, chi phí gọi mô hình.

**Kết quả đã công bố:** Bảng 3/Phụ lục B, Anime: MF NDCG/ILD 0,316/0,776; MMR 0,299/0,874; ChatGPT T8 0,307/0,806. LLM không thắng greedy trên mọi metric.

**Ngôn ngữ, code và môi trường:** Java RankSys cho MF; Python cho LLM reranking. Bài dùng hai GPU A40 48 GB cho Llama; bản đầy đủ không phù hợp máy 16 GB. Repo đã kiểm tra, chưa chạy lại.

**Hạn chế và phạm vi kết luận:** Tác giả/phân tích: item ngoài candidates, output không hợp lệ và random fill làm giảm accuracy; model snapshot cũ, offline evaluation. Năm nghiên cứu ban đầu là 2024, dù bản publisher ghi 2025.

**Hướng cải tiến đề xuất:** Nếu còn tài nguyên, thử constrained item-ID generation và đo invalid rate, latency, chi phí. Đối sánh với greedy exposure-aware; chỉ dùng LLM khi có lợi ích vượt baseline mạnh ở cùng ngân sách.

**Điểm cần kiểm tra khi tái lập:** Đây là một dòng nghiên cứu từ tiền ấn phẩm 2024; không quảng bá như thuật toán vừa xuất hiện lần đầu năm 2025.

<pagebreak>

## 3.9. [9] SCRUF-D / social choice

**Integrating Individual and Group Fairness for Recommender Systems through Social Choice**

Amanda Aird; Elena Štefancová; Anas Buhayh; Cassidy All; Martin Homola; Nicholas Mattei; Robin Burke

ACM RecSys 2025, tr. 177–186; 07/09/2025

[Bài/toàn văn](https://doi.org/10.1145/3705328.3748087) | [Code](https://github.com/that-recsys-lab/individual_fair_recsys2025)

**Bài toán và phương pháp:** SCRUF-D phối hợp các fairness agents theo cơ chế phân bổ và bỏ phiếu; cân bằng item coverage với group exposure thay vì chọn một định nghĩa fairness duy nhất.

**Dữ liệu và protocol:** MovieLens 1M bổ sung The Movies Dataset; AMBAR music. ML: 5 random partitions 80/20; BPR-MF/RecBole; top-50 → top-10.

**Baselines:** No-rerank BPR; group-only, individual-only và kết hợp; LeastFair/Lottery/Weighted × Borda/Copeland/Rescoring.

**Phép đo:** NDCG@10, target-normalized coverage, group exposure, L1/2 norm, RBO, NLIP.

**Kết quả đã công bố:** Bảng 3, ML, Both Lottery+Borda: NDCG 0,085±0,008 so với base 0,073±0,002; normalized coverage 0,728±0,053 so với 0,661±0,056. Bảng 2 music cho thấy lợi ích không đồng đều; NDCG 0,101 so với base 0,103.

**Ngôn ngữ, code và môi trường:** Python; README yêu cầu ≤3.9 do Whalrus; có C metrics biên dịch bằng clang, cấu hình TOML/YAML. Chưa chạy tái lập.

**Hạn chế và phạm vi kết luận:** Tác giả: kết quả phụ thuộc miền, coverage chưa xét vị trí, targets mang tính minh họa. Nhận xét: kết hợp nhiều agents đã có; cần chứng minh cơ chế mới tốt hơn chính tổ hợp này.

**Hướng cải tiến đề xuất:** Thêm agent diversity và thay coverage bằng exposure có trọng số vị trí; đánh giá temporal split và độ nhạy thứ tự user. Ablation từng agent và cơ chế social choice để xác định nguồn lợi ích.

**Điểm cần kiểm tra khi tái lập:** Coverage được chuẩn hóa theo mục tiêu của bài; không so trực tiếp số 0,728 với catalog coverage thô. ± trong kết quả ML là CI theo 5 partitions, không ghi thành SD.

<pagebreak>

## 3.10. [10] ElasticRank

**Understanding Accuracy-Fairness Trade-offs in Re-ranking through Elasticity in Economics**

Chen Xu; Jujia Zhao; Wenjie Wang; Liang Pang; Jun Xu; Tat-Seng Chua; Maarten de Rijke

ACM SIGIR 2025, tr. 539–548

[Bài/toàn văn](https://arxiv.org/html/2504.14991v1) | [Code](https://github.com/XuChen0427/ElasticRank)

**Bài toán và phương pháp:** Mô hình hóa đánh đổi accuracy–fairness bằng elasticity; EF-Curve/EF metric và ElasticRank điều chỉnh điểm trong không gian utility.

**Dữ liệu và protocol:** Steam, Amazon Digital Music, Yelp; nhóm publisher/category, gộp nhóm <10 items. Global chronology 80% train MF, 20% cho reranking evaluation.

**Baselines:** FairRec/FairRec+, Welf, CPFair, P-MMF, min-regularizer, TaxRank.

**Phép đo:** Score-based NDCG@5/10/20, Loss, EF, inference time.

**Kết quả đã công bố:** Bảng 2, Steam@10: ElasticRank NDCG 0,9948, EF −0,8283; P-MMF 0,9890/−0,9228. Yelp@10: ElasticRank 0,9918/−0,4211; P-MMF 0,9923/−0,4379. NDCG này dùng điểm MF làm gain, không phải binary test relevance.

**Ngôn ngữ, code và môi trường:** Python 3.9; repo có main.py, cũng tích hợp qua FairDiverse. Đã xác minh liên kết chính thức, chưa chạy lại.

**Hạn chế và phạm vi kết luận:** Nhận xét đối với đề tài: chưa có ràng buộc diversity trong từng danh sách; ý nghĩa group utility phụ thuộc scorer và grouping. Giữ gần điểm gốc chưa đồng nghĩa giữ accuracy thực.

**Hướng cải tiến đề xuất:** Bổ sung ILD tối thiểu và position-weighted exposure budget, sau đó đánh giá held-out NDCG cùng scorer-retention. Dùng cùng candidates và ngân sách tuning để tránh lợi ích do protocol khác nhau.

**Điểm cần kiểm tra khi tái lập:** Không đặt NDCG≈0,99 của bài cạnh held-out NDCG≈0,10 ở PFA rồi kết luận ElasticRank chính xác hơn. Hai đại lượng có gain khác nhau.

<pagebreak>

## 3.11. [11] SMMR

**SMMR: Sampling-Based MMR Reranking for Faster, More Diverse, and Balanced Recommendations and Retrieval**

Kiryl Liakhnovich; Oleg Lashinin; Andrei Babkin; Michael Pechatov; Marina Ananyeva

ACM SIGIR 2025, short paper, tr. 2754–2758

[Bài/toàn văn](https://www.hse.ru/data/2025/07/04/1995597406/%D0%90%D0%BD%D0%B0%D0%BD%D1%8C%D0%B5%D0%B2%D0%B0_%D1%81%D1%82%D0%B0%D1%82%D1%8C%D1%8F%2012.pdf) | [Code](https://github.com/kliakhnovich/smmr)

**Bài toán và phương pháp:** Thay lựa chọn MMR hoàn toàn quyết định bằng softmax sampling và batch tăng dần, nhằm tăng inter-list diversity và giảm số vòng chọn.

**Dữ liệu và protocol:** MovieLens 10M, Dunnhumby, MIND; temporal train/test 80/20; top-1.000 candidates; BPR, LightGCN, SASRec. Validation split chưa được mô tả đủ trong nguồn kiểm tra.

**Baselines:** MMR, FastMAP-DPP, SSD và no-rerank; similarity từ embeddings nội bộ.

**Phép đo:** Recall, ItemCoverage, ILAD (inter-list Jaccard diversity), mean runtime.

**Kết quả đã công bố:** Bảng 2, MIND+BPR@100, λ=0,9: MMR Recall/coverage/ILAD 0,11/0,37/0,89; SMMR 0,11/0,400/0,92. Ở λ=0,95, SMMR Recall 0,13 so với MMR 0,15: không luôn giữ accuracy.

**Ngôn ngữ, code và môi trường:** Python 3.11 theo README hiện hành; RecBole/PyTorch, NumPy. Repo có nhánh paper_reproducibility và production_ready; chưa chạy tái lập.

**Hạn chế và phạm vi kết luận:** Nhận xét: chưa có hard exposure target; kết quả phụ thuộc temperature và seed. ‘Logarithmic’ là số vòng sampling; chi phí dựng similarity vẫn cần tính theo số candidates.

**Hướng cải tiến đề xuất:** Thêm exposure dual penalty và thử temperature phụ thuộc độ bất định; so với cả MMR và SMMR nguyên bản ở cùng latency. Báo CI của metric toàn batch vì stochastic sampling ảnh hưởng phân bố exposure.

**Điểm cần kiểm tra khi tái lập:** ILAD là độ khác nhau giữa các danh sách; không đổi tên thành ILD trong từng danh sách. Không tự gán kết quả K=100 sang NDCG@10 của luận văn.

<pagebreak>

## 3.12. [12] FairDiverse

**FairDiverse: A Comprehensive Toolkit for Fairness- and Diversity-aware Information Retrieval**

Chen Xu; Zhirui Deng; Clara Rus; Xiaopeng Ye; Yuanna Liu; Jun Xu; Zhicheng Dou; Ji-Rong Wen; Maarten de Rijke

ACM SIGIR 2025, resource paper, tr. 3540–3550

[Bài/toàn văn](https://pure.uva.nl/ws/files/304772377/3726302.3730280.pdf) | [Code](https://github.com/XuChen0427/FairDiverse)

**Bài toán và phương pháp:** Chuẩn hóa dữ liệu, pre/in/post-processing và evaluation cho fairness/diversity; hỗ trợ search và recommendation với 28 thuật toán trên 16 base models.

**Dữ liệu và protocol:** Benchmark recommendation minh họa trên Steam: BPR cho in-processing, DMF cho reranking. Split cụ thể chưa được xác minh đủ từ config; không mặc định dùng split của luận văn.

**Baselines:** Có FairRec/+, CPFair, P-MMF, TaxRank, ElasticRank, FairSync, RAIF, FairDual và các phương pháp khác.

**Phép đo:** NDCG/HR/MRR, MMF/Gini/Entropy, utility loss; tùy tác vụ.

**Kết quả đã công bố:** Bảng 3, default Steam+BPR: FairDual NDCG@10/Gini 0,3204/0,7123; FairNeg 0,2964/0,6671. Đây là minh họa trade-off trong toolkit, không phải bảng xếp hạng sau tuning công bằng đầy đủ.

**Ngôn ngữ, code và môi trường:** Python/PyTorch, NumPy/Pandas/SciPy/CVXPY. Docs: https://xuchen0427.github.io/FairDiverse/ . RAIF có phụ thuộc Gurobi/license; chưa cài hoặc chạy lại.

**Hạn chế và phạm vi kết luận:** Nhận xét: default settings chưa đủ kết luận thuật toán tốt nhất; group fairness metrics không thay thế ILD. Một số thuật toán được tái hiện trong toolkit, cần đối chiếu với code gốc.

**Hướng cải tiến đề xuất:** Dùng làm benchmark harness, thêm temporal split, cùng candidate cache và metrics thống nhất. Đóng góp cần nằm ở thuật toán hoặc bằng chứng nghiên cứu, không chỉ ghép các API đã có.

**Điểm cần kiểm tra khi tái lập:** ArXiv v1 có caption Bảng 4 ghi ClueWeb trong khi mô tả nói Steam+DMF; báo cáo tránh trích số bảng này và cung cấp link final published PDF.

<pagebreak>

## 3.13. [13] DPFR / Oracle2Fair

**Joint Evaluation of Fairness and Relevance in Recommender Systems with Pareto Frontier**

Theresia Veronika Rampisela; Tuukka Ruotsalo; Maria Maistro; Christina Lioma

ACM The Web Conference 2025, tr. 1548–1566

[Bài/toàn văn](https://arxiv.org/html/2502.11921v1) | [Code](https://github.com/theresiavr/DPFR-recsys-evaluation)

**Bài toán và phương pháp:** DPFR đo khoảng cách tới điểm tham chiếu trên frontier relevance–fairness do Oracle2Fair dựng, thay vì ghép hai metric theo trọng số thiếu căn cứ.

**Dữ liệu và protocol:** Lastfm, Amazon-lb, QK-video, Jester, ML10M, ML20M. Amazon/MovieLens global temporal 60/20/20; dữ liệu thiếu timestamp chia global random cùng tỷ lệ; top-25 → top-10.

**Baselines:** ItemKNN, BPR, MultiVAE, NCL; GS, COMBMNZ, BordaCount; đối chiếu DPFR với Jain/QF/Gini/FSat/Entropy, IBO/MME/IAA/II-F/AI-F.

**Phép đo:** Relevance–fairness pairs, DPFR và độ nhất quán thứ hạng thuật toán.

**Kết quả đã công bố:** Bảng 3, ML20M: frontier đầy đủ mất 75,77 phút; xấp xỉ 12 điểm mất 2,60 phút, Kendall τ tối thiểu 0,97. Kết quả đánh giá không đồng nghĩa mọi hệ thống mới đều đạt frontier đó.

**Ngôn ngữ, code và môi trường:** Python/RecBole, notebooks và code Oracle2Fair. Repo chính thức đã xác minh; chưa chạy tái lập.

**Hạn chế và phạm vi kết luận:** Nhận xét: hai mục tiêu; oracle sử dụng nhãn evaluation và có thể vượt candidate pool thực. Không dùng test oracle để chọn tham số hoặc coi oracle là thuật toán có thể triển khai.

**Hướng cải tiến đề xuất:** Đánh giá frontier ba trục accuracy–diversity–exposure và thêm frontier bị giới hạn cùng candidate pool; kèm CI. So với DPFR và các metric tách biệt để kiểm tra độ ổn định kết luận.

**Điểm cần kiểm tra khi tái lập:** Bản mở rộng arXiv:2610.27850 ngày 20/10/2026 được tác giả ghi accepted ACM TORS; chưa xác minh DOI riêng. Gộp vào dòng DPFR, không đếm thêm một bài độc lập.

<pagebreak>

## 3.14. [14] FairDual

**Bridging Jensen Gap for Max-Min Group Fairness Optimization in Recommendation**

Chen Xu; Yuxin Li; Wenjie Wang; Liang Pang; Jun Xu; Tat-Seng Chua

ICLR 2025, conference paper

[Bài/toàn văn](https://proceedings.iclr.cc/paper_files/paper/2025/hash/184a03a3ad07e8897c62461c02634b02-Abstract-Conference.html) | [Code](https://github.com/XuChen0427/FairDual)

**Bài toán và phương pháp:** Max-min fairness phi tuyến tạo Jensen gap khi tối ưu bằng minibatch. FairDual dùng group-weighted objective và dual mirror optimization để giảm khoảng cách này.

**Dữ liệu và protocol:** MIND, Amazon-Book, Amazon-Electronic; chronology 80/10/10; 3 lần chạy. Backbone chính NRMS, RecFormer, BigRec; phụ lục có BPR/GRU4Rec/SASRec.

**Baselines:** UNI, DRO, S-DRO, Prop, IFairLRS, Maxmin Sample.

**Phép đo:** NDCG/MRR/MMF@5/10/20; MMF tổng hợp utility của 20% nhóm kém nhất.

**Kết quả đã công bố:** Bảng 1, BigRec–MIND@10: FairDual NDCG/MRR/MMF 1,69%/1,11%/2,99%; UNI 1,50%/0,98%/2,33%. Đây là phần trăm, không phải trị số thập phân 1,69.

**Ngôn ngữ, code và môi trường:** Python 3.9, PyTorch 2.0.1+cu117, CVXPY; Ubuntu 18.04, GPU A5000. Repo MIT hiện công bố chủ yếu Llama2–MIND dựa trên BigRec, chưa đủ toàn bộ backbones; chưa chạy lại.

**Hạn chế và phạm vi kết luận:** Nhận xét: in-processing, không phải reranker thuần; chưa trực tiếp tối ưu ILD; tái lập nhánh LLM tốn tài nguyên hơn máy 16 GB. Lý thuyết Jensen gap không tự bảo đảm quota thực tế của mỗi batch.

**Hướng cải tiến đề xuất:** Thử cơ chế kế toán nhóm/dual trên BPR đóng băng, thêm diversity và kiểm tra batch size, thứ tự user, drift. So với FairDual gốc nếu tài nguyên cho phép; ghi rõ khác biệt giữa train-time và post-processing.

**Điểm cần kiểm tra khi tái lập:** ICLR có trang proceedings chính thức; không bịa DOI ACM. NDCG, MMF trong bài có thang đo khác nhau giữa bảng nên phải đọc header trước khi trích.

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


<pagebreak>

# 9. Danh mục tài liệu tham khảo

Các mục [1]–[14] là 14 công trình chính. Link code đi kèm từng hồ sơ ở Mục 3; link dưới đây dẫn tới publisher/proceedings hoặc toàn văn. Các nguồn web và repo được rà soát ngày 15/11/2026. Với metadata không xác minh đủ số trang, báo cáo giữ DOI thay vì điền số trang suy đoán.

## 9.1. Công trình chính 2025–2026

[1] Jingzhi Li; Zhiyong Cheng; Richang Hong; Meng Wang. Post-hoc Provider Fairness Adaptation via Hierarchical Exposure Alignment. ACM SIGIR 2026. DOI: 10.1145/3805712.3809597. [Bài](https://arxiv.org/html/2605.01524v1). [Code](https://github.com/Tam-JQK/Post-train).

[2] Raciel Yera; Luis Martínez. Behind the Re-Rank: Explaining Fairness in Top-N Recommendations. ACM UMAP 2026, tr. 21–29. DOI: 10.1145/3774935.3806165. [Bài](https://ruja.ujaen.es/server/api/core/bitstreams/78628cee-deca-474f-9dad-ca0bd6fc0e8c/content). [Code](https://github.com/ryera/fairness-explanation-topn).

[3] Célina Treuillier; Sylvain Castagnos; Evan Dufraisse; Özlem Özgöbek; Armelle Brun. Shift your Focus for the Greater Good: Improving Fairness at no cost for Accuracy and Diversity in News Recommender Systems. ACM Transactions on Recommender Systems 4(3), Article 44, 1–36; online 05/03/2026. DOI: 10.1145/3790097. [Bài](https://doi.org/10.1145/3790097). [Code](https://github.com/celinatreuillier/ADF_framework).

[4] Theresia Veronika Rampisela; Maria Maistro; Tuukka Ruotsalo; Falk Scholer; Christina Lioma. Relevance-aware Individual Item Fairness Measures for Recommender Systems: Limitations and Usage Guidelines. ACM Transactions on Recommender Systems 4(3), Article 37, 45 trang; online 05/03/2026. DOI: 10.1145/3765624. [Bài](https://doi.org/10.1145/3765624). [Code](https://github.com/theresiavr/relevance-aware-item-fairness-measures-recsys).

[5] Rikiya Takehi; Fernando Diaz; Tetsuya Sakai. Diversification as Risk Minimization. ACM WSDM 2026, tr. 618–628. DOI: 10.1145/3773966.3777985. [Bài](https://arxiv.org/html/2510.22681v1). [Code](https://github.com/RikiyaT/VRisk).

[6] Jaeri Lee; Jongjin Kim; U Kang. CatDive: A simple yet effective method for maximizing category diversity in sequential recommendation. PLOS ONE 21(1), e0341419; 30/01/2026. DOI: 10.1371/journal.pone.0341419. [Bài](https://journals.plos.org/plosone/article?id=10.1371/journal.pone.0341419). [Code](https://github.com/snudatalab/CatDive).

[7] Kazuma Onishi; Katsuhiko Hayashi; Hidetaka Kamigaito. Accurate and Diverse Recommendations via Propensity-Weighted Linear Autoencoders. ACM SIGIR-AP 2025; công bố 06/12/2025. DOI: 10.1145/3767695.3769512. [Bài](https://arxiv.org/html/2512.20896v1). [Code](https://github.com/cars1015/IPS-LAE).

[8] Diego Carraro; Derek Bridge. Enhancing Recommendation Diversity by Re-ranking with Large Language Models. ACM Transactions on Recommender Systems 4(2), Article 18, 1–40; trang publisher hiển thị 22/11/2025. DOI: 10.1145/3700604. [Bài](https://arxiv.org/html/2401.11506v2). [Code](https://github.com/cdiego89phd/chat-reranking).

[9] Amanda Aird; Elena Štefancová; Anas Buhayh; Cassidy All; Martin Homola; Nicholas Mattei; Robin Burke. Integrating Individual and Group Fairness for Recommender Systems through Social Choice. ACM RecSys 2025, tr. 177–186; 07/09/2025. DOI: 10.1145/3705328.3748087. [Bài](https://doi.org/10.1145/3705328.3748087). [Code](https://github.com/that-recsys-lab/individual_fair_recsys2025).

[10] Chen Xu; Jujia Zhao; Wenjie Wang; Liang Pang; Jun Xu; Tat-Seng Chua; Maarten de Rijke. Understanding Accuracy-Fairness Trade-offs in Re-ranking through Elasticity in Economics. ACM SIGIR 2025, tr. 539–548. DOI: 10.1145/3726302.3730106. [Bài](https://arxiv.org/html/2504.14991v1). [Code](https://github.com/XuChen0427/ElasticRank).

[11] Kiryl Liakhnovich; Oleg Lashinin; Andrei Babkin; Michael Pechatov; Marina Ananyeva. SMMR: Sampling-Based MMR Reranking for Faster, More Diverse, and Balanced Recommendations and Retrieval. ACM SIGIR 2025, short paper, tr. 2754–2758. DOI: 10.1145/3726302.3730250. [Bài](https://www.hse.ru/data/2025/07/04/1995597406/%D0%90%D0%BD%D0%B0%D0%BD%D1%8C%D0%B5%D0%B2%D0%B0_%D1%81%D1%82%D0%B0%D1%82%D1%8C%D1%8F%2012.pdf). [Code](https://github.com/kliakhnovich/smmr).

[12] Chen Xu; Zhirui Deng; Clara Rus; Xiaopeng Ye; Yuanna Liu; Jun Xu; Zhicheng Dou; Ji-Rong Wen; Maarten de Rijke. FairDiverse: A Comprehensive Toolkit for Fairness- and Diversity-aware Information Retrieval. ACM SIGIR 2025, resource paper, tr. 3540–3550. DOI: 10.1145/3726302.3730280. [Bài](https://pure.uva.nl/ws/files/304772377/3726302.3730280.pdf). [Code](https://github.com/XuChen0427/FairDiverse).

[13] Theresia Veronika Rampisela; Tuukka Ruotsalo; Maria Maistro; Christina Lioma. Joint Evaluation of Fairness and Relevance in Recommender Systems with Pareto Frontier. ACM The Web Conference 2025, tr. 1548–1566. DOI: 10.1145/3696410.3714589. [Bài](https://arxiv.org/html/2502.11921v1). [Code](https://github.com/theresiavr/DPFR-recsys-evaluation).

[14] Chen Xu; Yuxin Li; Wenjie Wang; Liang Pang; Jun Xu; Tat-Seng Chua. Bridging Jensen Gap for Max-Min Group Fairness Optimization in Recommendation. ICLR 2025, conference paper. DOI: không gán DOI. [Bài](https://proceedings.iclr.cc/paper_files/paper/2025/hash/184a03a3ad07e8897c62461c02634b02-Abstract-Conference.html). [Code](https://github.com/XuChen0427/FairDual).

## 9.2. Prior art trực tiếp và cập nhật mới

[15] C. Xu, X. Ye, W. Wang, L. Pang, J. Xu và T.-S. Chua, “A Taxation Perspective for Fair Re-ranking,” SIGIR, 2024, tr. 1494–1503. DOI: [10.1145/3626772.3657766](https://doi.org/10.1145/3626772.3657766). [Toàn văn tác giả](https://arxiv.org/html/2404.17826v1). [Code](https://github.com/XuChen0427/Tax-rank).

[16] C. Xu, J. Xu, Y. Ding, X. Zhang và Q. Qi, “FairSync: Ensuring Amortized Group Exposure in Distributed Recommendation Retrieval,” The Web Conference, 2024. DOI: [10.1145/3589334.3645413](https://doi.org/10.1145/3589334.3645413). [Toàn văn](https://arxiv.org/html/2402.10628v1). [Code](https://github.com/XuChen0427/FairSync).

[17] T. Xie, Y. Ge và S. Guo, “Accuracy, Fairness, Diversity All at Once: An Influence-Function-Guided Data Enhancement Approach for Recommender System,” ACM Transactions on Knowledge Discovery from Data, 19(9), Article 171, 2025. DOI: [10.1145/3768316](https://doi.org/10.1145/3768316). [Metadata đại học tác giả](https://experts.arizona.edu/en/publications/accuracy-fairness-diversity-all-at-once-an-influence-function-gui/). [Code](https://github.com/TYtianyang/infodance).

[18] K. Kim, “Recommendation diversification via user-centric subprofiles and global item clusters,” Expert Systems with Applications, online 2026, Article 133766. DOI: [10.1016/j.eswa.2026.133766](https://doi.org/10.1016/j.eswa.2026.133766). [Preview publisher](https://www.sciencedirect.com/science/article/pii/S0957417426026746). Chưa đủ toàn văn cho hồ sơ thực nghiệm đầy đủ; chưa xác minh code.

[19] T. V. Rampisela, M. Maistro, T. Ruotsalo và C. Lioma, “Robustness Analysis of Pareto-based Joint Evaluation of Fairness and Relevance in Recommender Systems,” arXiv:2610.27850, 20/10/2026; tác giả thông báo accepted ACM TORS, chưa xác minh DOI publisher riêng. [Bản tác giả](https://arxiv.org/abs/2610.27850). [Code bản mở rộng](https://github.com/theresiavr/robustness-DPFR-recsys-evaluation). Gộp cùng dòng DPFR [13].

## 9.3. Nền tảng thuật toán và framework

[20] S. Rendle, C. Freudenthaler, Z. Gantner và L. Schmidt-Thieme, “BPR: Bayesian Personalized Ranking from Implicit Feedback,” UAI, 2009, tr. 460–469. [PMLR R7 và PDF](https://proceedings.mlr.press/r7/rendle09a.html). Implementation baseline có trong [RecBole](https://github.com/RUCAIBox/RecBole); không mô tả implementation này là code gốc của bài 2009.

[21] X. He, K. Deng, X. Wang, Y. Li, Y. Zhang và M. Wang, “LightGCN: Simplifying and Powering Graph Convolution Network for Recommendation,” SIGIR, 2020, tr. 639–648. DOI: [10.1145/3397271.3401063](https://doi.org/10.1145/3397271.3401063). [PDF tác giả](https://hexiangnan.github.io/papers/sigir20-LightGCN.pdf). [Code TensorFlow gốc](https://github.com/kuandeng/LightGCN); [bản PyTorch được repo gốc dẫn](https://github.com/gusye1234/LightGCN-PyTorch).

[22] W. X. Zhao và cộng sự, “RecBole: Towards a Unified, Comprehensive and Efficient Framework for Recommendation Algorithms,” CIKM, 2021. DOI: [10.1145/3459637.3482016](https://doi.org/10.1145/3459637.3482016). [Code và tài liệu](https://github.com/RUCAIBox/RecBole).

[23] J. Carbonell và J. Goldstein, “The Use of MMR, Diversity-Based Reranking for Reordering Documents and Producing Summaries,” SIGIR, 1998, tr. 335–336. DOI: [10.1145/290941.291025](https://doi.org/10.1145/290941.291025). MMR là baseline được tái sử dụng trong các bài reranking; có implementation đối chiếu trong [SMMR](https://github.com/kliakhnovich/smmr).

## 9.4. Dữ liệu và nguồn đặc tả

[24] GroupLens Research, MovieLens datasets. [Trang tổng](https://grouplens.org/datasets/movielens/); [100K](https://grouplens.org/datasets/movielens/100k/); [1M](https://grouplens.org/datasets/movielens/1m/). Dùng README/terms tại đúng bản tải để xác nhận schema và quyền sử dụng.

[25] J. Ni, J. Li và J. McAuley, “Justifying Recommendations using Distantly-Labeled Reviews and Fine-Grained Aspects,” EMNLP-IJCNLP, 2019; nguồn Amazon Review Data 2018. [Dataset, metadata, 5-core và citation](https://cseweb.ucsd.edu/~jmcauley/datasets/amazon_v2/). Phần đề xuất chọn Musical Instruments 5-core, không tải toàn bộ Amazon.

[26] Y. Hou, J. Li, Z. He, A. Yan, X. Chen và J. McAuley, “Bridging Language and Items for Retrieval and Recommendation,” 2024; nguồn mô tả Amazon Reviews 2023. [Trang dataset chính thức](https://amazon-reviews-2023.github.io/). Đây là nguồn dữ liệu bổ trợ, không được tính vào 14 bài phương pháp chính.

[27] “CSE631 — Đề tài 07: Hệ gợi ý thương mại điện tử đa mục tiêu cân bằng độ chính xác, đa dạng và công bằng hiển thị sản phẩm,” tài liệu đề tài do người học cung cấp, GVHD: TS. Nguyễn Khắc Chiến; tệp CSE631_DeTai_07_MultiObjective_Recsys.pdf, 11 trang. Căn cứ phạm vi, tài nguyên và tiêu chí nghiệm thu của báo cáo.

<pagebreak>

# Phụ lục. Các điểm phải kiểm tra khi bắt đầu tái lập

| Điểm kiểm tra | Cách xử lý trong nghiên cứu |
|---|---|
| PFA: group definition giữa paper và README chưa khớp | Đọc code đường tạo nhóm, pin commit và ghi lựa chọn. |
| ElasticRank: NDCG dùng gain từ score gốc | Tính thêm held-out NDCG, đặt tên metric khác nhau. |
| SMMR: ILAD là inter-list; độ phức tạp similarity | Tính riêng ILD và ILAD; đo toàn pipeline, không chỉ vòng sampling. |
| SCRUF-D: coverage được target-normalized | Báo lại raw catalog coverage và giải thích normalized metric của bài gốc. |
| VRisker: MovieLens là evaluation-only | Dựng input từ BPR train-only; không cho oracle ratings vào policy triển khai. |
| FairDual: repo chỉ bao phủ một nhánh chính | Không ghi “tái lập toàn bài” khi chỉ chạy BigRec–MIND hoặc bản tự viết BPR. |
| FairDiverse: mặc định/split/caption bản cũ | Kiểm tra config và bản final; cùng tuning budget trong benchmark mới. |
| TaxRank: citation repo không khớp bài | Dùng DOI và tác giả từ publisher/PDF đã đối chiếu. |
| LLМ models và API snapshots đã thay đổi | Ghi model/version/date; thay model là thí nghiệm mới, không bản tái lập nguyên trạng. |
| DPFR và bản mở rộng | Không đếm lặp; test oracle chỉ để hậu kiểm, không tune. |

Tài liệu này cung cấp khảo sát và thiết kế thí nghiệm, chưa cung cấp một hệ thống gợi ý đã triển khai hoặc kết quả thực nghiệm mới. Các hướng đóng góp cần tiếp tục rà soát 20–30 bài sát cơ chế đã chọn, tái lập baseline và kiểm chứng trước khi chốt tuyên bố novelty trong luận văn/paper.
