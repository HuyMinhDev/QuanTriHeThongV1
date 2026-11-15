# Nguồn mã đã đối chiếu: SCRUF-D RecSys 2025

Ngày: 15/11/2026. Repo: https://github.com/that-recsys-lab/individual_fair_recsys2025.

Artifact ở đây là ghi chú và trích lệnh README qua web; **không phải clone, không phải snapshot repo, chưa chạy training/evaluation chính thức**. Nội dung đầy đủ entry và các lớp agent không truy cập được do web cache miss; vì vậy không có bản audit source hoàn chỉnh hay commit SHA xác minh.

README và cấu trúc đã đọc tại https://github.com/that-recsys-lab/individual_fair_recsys2025#readme. Entry do README nêu: scruf_d/__main__recsys_25.py. Configurations chọn least_fair/product_lottery/weighted_product_allocation; choice weighted_scoring/RuleBorda/RuleCopeland. Post-processing có metrics.c và run_movie_experiments.py.

README yêu cầu Python<=3.9 vì tương thích Whalrus. Xem README_DA_KIEM_TRA.md cho trích lệnh. Dataset phải được chuẩn bị riêng; không nói thư mục này chứa toàn bộ code/dữ liệu tác giả. Toy Borda và metric tự biên soạn ở ../../Vi_du_chay_tay/09_SCRUF_D.py.
