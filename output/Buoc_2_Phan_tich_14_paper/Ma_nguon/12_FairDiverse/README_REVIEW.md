# Ghi chú đọc README và code

Entry points chính thức là RecTrainer.train và RecReRanker.rerank. CLI chọn task recommendation/search, stage in-processing/post-processing, dataset và train_config_file. Post-processing cần cache ranking_scores.npz tương ứng logpath.

Quan sát tĩnh cần xác minh theo commit: trainer.py đặt best_result=-1 trong vòng epoch; cần kiểm tra checkpoint behavior bằng regression trước khi tái lập. Reranker tính utility retention bằng scores mô hình gốc; không coi đó là held-out NDCG của nhãn test. Không thực hiện sửa mã hay tuyên bố đã tái hiện lỗi.

Chưa xác minh đủ YAML để chốt tỷ lệ train/validation/test của benchmark bài báo. Processor hiện đọc có timestamp slicing và sampled negatives; branch hiện hành không tự đồng nhất với artifact công bố2025.
