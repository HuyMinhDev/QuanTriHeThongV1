# Nguồn mã đã đối chiếu: FairDual

Ngày: 15/11/2026. Repo https://github.com/XuChen0427/FairDual; branch master; chưa xác minh commit SHA.

**Thư mục này là ghi chú đọc web và đoạn nhận diện đường gọi; không phải clone/snapshot đầy đủ; không có Llama weights, không có báo cáo training đã chạy.**

Nguồn README https://github.com/XuChen0427/FairDual#readme; source đã đọc https://github.com/XuChen0427/FairDual/blob/master/train.py. README phát hành đường Llama2/MIND dựa trên BigRec và chỉ dẫn sh train.sh. Môi trường tham khảo từ bài: Python3.9, PyTorch2.0.1+cu117, cvxpy, Ubuntu18.04, A5000.

Đã xác minh FairTrainer.compute_loss, FairTrainer.get_item_emb, WeightLabelSmoother; import Dual_Sampler từ sample_utils.Dual_sample; luồng dot-product ranking_scores→torch.topk→update_weight→weighted token loss. Chưa đọc được đầy đủ sample_utils/Dual_sample.py; không khẳng định đã audit projection.

Code lấy embedding có giả định về token xuống dòng và cấu trúc prompt. Cần kiểm tra lại nếu đổi tokenizer/template. Repository hiển thị MIT; lấy đầy đủ LICENSE và dependencies từ repo trước khi tái sử dụng. Toy Jensen/weighted loss độc lập ở ../../Vi_du_chay_tay/14_FairDual.py, không hiện thực FairDual hoàn chỉnh.
