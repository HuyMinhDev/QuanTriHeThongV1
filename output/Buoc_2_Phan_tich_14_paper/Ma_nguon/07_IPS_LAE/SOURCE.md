# Nguồn mã: IPS-LAE

- Repo tác giả: https://github.com/cars1015/IPS-LAE ; branch main.
- DOI: https://doi.org/10.1145/3767695.3769512
- Truy cập web: 15/11/2026; chưa xác minh commit SHA hoặc tải git archive.
- Đã đọc main.py, run.sh, environment.yml, sansa.py trên raw.githubusercontent.com/cars1015/IPS-LAE/main/.
- main.py: CORR.compute_inv_propensity_logsigmoid, _apply_weighting, fit_model; EVAL.Recall/NDCG; run_experiment.
- run.sh: vòng lặp ease/edlae/rdlae, weighted/unweighted và parameters theo dataset.
- sansa.py: nhánh sparse dùng CHOLMOD/sansa_inv.
- License repo khai báo Apache-2.0: https://github.com/cars1015/IPS-LAE/blob/main/LICENSE
- File trích đoạn không phải bản main.py đầy đủ. File environment_review.md là ghi chú tự biên soạn từ môi trường khai báo, không phải lockfile đã cài.
- Chưa chạy code gốc hoặc dataset thật. Toy Vi_du_chay_tay/07_IPS_LAE.py là code mới của người biên soạn, đã chạy và đối chiếu nghiệm.
