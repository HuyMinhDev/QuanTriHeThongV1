# Ghi chú workflow, tự biên soạn

Nguồn README: https://github.com/theresiavr/DPFR-recsys-evaluation

Tải datasets theo hướng dẫn repo, preprocessing ở preproc_data; tuning scripts và hyperchoice của fork RecBole; reranking/rerank_subset.py; eval/base_eval.py; pareto/generate_pareto.py và pareto/estimate_pareto.py; cuối cùng notebook experiments/02_pareto_pair_plot.ipynb cho DPFR.

Đây là pipeline phụ thuộc artifact, không phải một command chạy được từ bất kỳ working directory. Có placeholder newest_file trong notebook đã đọc. Chưa xác minh package lock hoặc full installation. Khi tái lập, cần giữ test oracle ở evaluator, không dùng oracle labels để tune deployed reranker.
