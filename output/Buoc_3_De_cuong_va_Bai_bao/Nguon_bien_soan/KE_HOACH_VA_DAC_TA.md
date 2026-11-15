# Bước 3: đề cương theo mẫu và bản thảo nghiên cứu

Mục tiêu: hai Word độc lập; đề cương tuân thủ file mẫu 2022 do học viên gửi; bản thảo trình bày đầy đủ mô hình, chứng minh, ví dụ, mô phỏng và protocol thực nghiệm dự kiến.

## Phương án đã chọn trong phạm vi người học yêu cầu

- Tên luận văn: Tái xếp hạng gợi ý đa mục tiêu với kiểm chứng tính khả thi dưới bất định độ phổ biến.
- Hướng A (chọn): ràng buộc utility/diversity + scenario-CVaR exposure, cận dưới ghép kịch bản và cơ chế giữ witness. Có thể kiểm chứng bằng toán và bài toán nhỏ.
- Hướng B (không làm trung tâm): chỉ điều chỉnh trọng số theo user. Quá gần CatDive/ADF/VRisker và cơ chế reranking hiện có.
- Hướng C (nhánh tương lai): LLM chọn policy/giải thích. Gần FAIRGate, tốn tài nguyên, chưa cần thiết để trả lời RQ chính.

## Ký hiệu và hợp đồng thuật toán

B users, K slots, fixed candidates C_u, nonnegative predicted scores s_ui, positive nonincreasing weights w_r; unique items/user. Per-user predicted utility floor, category union minimum, finite scenario upper-tail exposure CVaR. Alpha là confidence; tail mass beta=1-alpha. Không gọi score floor là held-out NDCG guarantee.

Lower bound: risk envelope Q_alpha; cho một mixture rho, tối thiểu exposure hỗn hợp trên structural completions bằng chọn các item có coefficient thấp nhất rồi ghép với trọng số hạng giảm dần. Chọn tập mixtures gồm optimizer của cận dưới tách từng scenario để có dominance. Chỉ cận vượt threshold mới chứng nhận bất khả thi; cận thấp không chứng nhận có nghiệm.

Witness-preserving completion dùng MILP hoặc enumeration chính xác trên instance nhỏ; trạng thái FEASIBLE/INFEASIBLE/UNKNOWN. Timeout không phải vô nghiệm. Có witness thì giữ fallback đó; chưa có witness thì không tuyên bố output thỏa ràng buộc. Không có hệ số approximation phổ quát.

## Các tệp tạo mới

- Mo_phong/test_core.py: CVaR có atom, semantics constraints, counterexamples, bound dominance, exhaustive/MILP agreement, timeout fallback, infeasible/unknown.
- Mo_phong/core.py: mô hình và bộ kiểm chứng, bound, enumeration oracle, witness policy.
- Mo_phong/milp_backend.py: SciPy/HiGHS formulation, kiểm tra lại mọi incumbent.
- Mo_phong/run_study.py: các ví dụ kiểm tra và randomized finite-instance audit; xuất JSON/CSV.
- Nguon_bien_soan/de_cuong.md và bai_bao.md: nội dung và tài liệu tham khảo thống nhất.
- Nguon_bien_soan/tao_tai_lieu.py: xuất Word, font/lề/cấu trúc theo mẫu; bản thảo khác định dạng đề cương.

## Test list trước khi viết implementation

1. CVaR phân phối rời rạc: alpha0 là mean; atom cắt một phần; alpha>=1-1/S là max.
2. Hai users, K1: greedy chọn head trước vẫn thỏa budget tạm nhưng không thể hoàn thành; witness chọn tail rồi head.
3. Position-weighted quota: cùng một head item nhưng hạng khác cho exposure khác.
4. Cận tách scenario0 nhưng mixture0,5; true integer risk1. Cận không chứng minh feasible.
5. Với mọi prefix trong instance nhỏ ngẫu nhiên, LB_sep<=LB_mix<=min completion CVaR.
6. Mô hình MILP đúng coverage hai chiều và CVaR; so exact enumeration trên instance nhỏ.
7. UNKNOWN không bị đổi thành INFEASIBLE; fallback chỉ dùng witness đã xác minh.
8. Các kiểm tra toy không được ghi thành benchmark MovieLens/Amazon hoặc chứng minh tính mới.

## Thứ tự và kiểm chứng

Viết test trước; xác nhận thất bại vì hành vi chưa có; hiện thực tối thiểu; chạy lại. Rà soát chứng minh độc lập, rồi so enumeration với MILP. Tạo nội dung từ kết quả máy đã xuất; dữ liệu thực chỉ là kế hoạch. Kiểm tra XML/ZIP và chuyển text native của hai Word; đóng gói code, nguồn và nhật ký.

Mẫu yêu cầu khoảng10 trang, Times New Roman13/14, dòng1,5, lề trên3,5/dưới3/trái3,5/phải2 cm; số trang giữa phía trên, không thêm chữ header/footer. Thông tin cá nhân, phân công hướng dẫn và chữ ký chưa được cung cấp để trống có hướng dẫn, không tự bịa.
