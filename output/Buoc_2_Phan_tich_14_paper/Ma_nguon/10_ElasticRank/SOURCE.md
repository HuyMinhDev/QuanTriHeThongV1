# Nguồn mã đã đối chiếu: ElasticRank

Ngày: 15/11/2026. Repo: https://github.com/XuChen0427/ElasticRank; branch master. Không có commit SHA xác minh.

**Đây là một trích đoạn và ghi chú đọc web, không phải clone/snapshot đầy đủ; chưa chạy thí nghiệm chính thức.** Raw file đã đọc: https://raw.githubusercontent.com/XuChen0427/ElasticRank/master/ElasticRank.py. README: https://github.com/XuChen0427/ElasticRank#readme.

Tên lớp/hàm: ElasticRank.rerank, concave_func, distance_concave_func. Luồng xác minh: khởi tạo V_t=ones; chuẩn hóa V_t; chọn anchor theo anchor_rate; cộng correction vào ranking_score qua M; lấy top-k; cộng score gốc vào V_t. B_t lưu số item nhưng không phải trạng thái điều khiển correction.

README chỉ dẫn python main.py --train_config_file=train_Reranking.yaml và cho biết có tích hợp FairDiverse. Các dependencies và license đầy đủ chưa được audit. Trích đoạn dưới đây chỉ nhằm nhận diện phép toán, không đủ chạy mô hình. Bản toy do người biên soạn viết độc lập ở ../../Vi_du_chay_tay/10_ElasticRank.py.
