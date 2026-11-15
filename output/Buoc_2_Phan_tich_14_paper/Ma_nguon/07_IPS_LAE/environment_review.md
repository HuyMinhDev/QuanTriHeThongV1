# Môi trường khai báo đã đọc, chưa cài thử

Nguồn: https://raw.githubusercontent.com/cars1015/IPS-LAE/main/environment.yml

Tên environment IPS-LAE; Python3.11.5; NumPy1.24.3; pandas2.0.3; SciPy1.11.1; bottleneck1.3.5; scikit-learn1.3.0; scikit-sparse0.4.16. README dùng conda env create và conda activate trước chạy run.sh/run_sansa.sh với tên dataset. Không suy các packages này đã cài trên máy hiện tại. scikit-sparse/CHOLMOD cần được kiểm tra theo nền tảng khi tái lập.

Trong main.py, Recall dùng min(K,số positives) ở mẫu số. Cần ghi convention nếu đối chiếu với Recall hit/số positives của evaluator luận văn.
