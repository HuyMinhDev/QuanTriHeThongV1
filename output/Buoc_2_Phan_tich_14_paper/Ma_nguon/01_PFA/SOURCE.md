# Nguồn mã đã đối chiếu: PFA

Ngày kiểm tra: 15/11/2026. Kho gốc: https://github.com/Tam-JQK/Post-train.

Thư mục này là ghi chú đối chiếu qua web cùng trích đoạn rất ngắn; **không phải bản clone, không phải snapshot đầy đủ, không có checkpoint/dataset được xác minh và chưa chạy training chính thức**. Không có commit SHA được xác minh trong lần truy cập, nên chỉ có thể ghi branch main và ngày truy cập.

Nguồn đã đọc:

- README: https://github.com/Tam-JQK/Post-train#readme.
- Adapter: https://github.com/Tam-JQK/Post-train/blob/main/base_model/post_train.py.
- Training và grouping: https://github.com/Tam-JQK/Post-train/blob/main/trainer.py.

Đối chiếu: Post.forward tạo MLP correction; CombinedModel.forward cộng dot-product score với correction rồi sigmoid. RecTrainer.train đóng băng backbone và chỉ tối ưu post model. setup_supplier_groups dùng phân vị số item; generate_pid2group có logic train counts riêng. Cần audit đường gọi trước khi gắn implementation với grouping theo training exposure như bài.

README công bố Python>=3.8, PyTorch>=1.10. Lệnh được kiểm tra: pip install torch numpy pandas scipy scikit-learn tqdm pyyaml; python main.py. Cần tự chuẩn bị interaction splits, iid2pid.json và cấu hình tương ứng. Đây là lệnh tham khảo, không phải biên bản đã chạy thành công.

Repo hiển thị MIT license. Lấy đầy đủ repo và LICENSE từ nguồn tác giả trước khi tái sử dụng. Toy được biên soạn độc lập ở ../../Vi_du_chay_tay/01_PFA.py.
