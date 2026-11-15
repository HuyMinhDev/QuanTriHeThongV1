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
