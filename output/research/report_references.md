<pagebreak>

# 9. Danh mục tài liệu tham khảo

Các mục [1]–[14] là 14 công trình chính. Link code đi kèm từng hồ sơ ở Mục 3; link dưới đây dẫn tới publisher/proceedings hoặc toàn văn. Các nguồn web và repo được rà soát ngày 15/11/2026. Với metadata không xác minh đủ số trang, báo cáo giữ DOI thay vì điền số trang suy đoán.

## 9.1. Công trình chính 2025–2026

<mainrefs>

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
