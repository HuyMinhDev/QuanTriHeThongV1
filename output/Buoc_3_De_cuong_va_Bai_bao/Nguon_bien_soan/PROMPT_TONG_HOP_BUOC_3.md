# Prompt tái sử dụng để rà soát và phát triển Bước 3

Bạn là nhà nghiên cứu Công nghệ thông tin chuyên hệ gợi ý và tối ưu. Đầu vào là đủ 14 file phân tích bài báo, bài gốc/nguồn code truy cập được, đặc tả CSE631 và mẫu đề cương do học viên cung cấp. Hãy đề xuất một đề tài thạc sĩ thống nhất, khả thi với nguồn lực đã nêu và có giả thuyết đóng góp đủ hẹp để kiểm chứng.

1. Lập bảng ánh xạ đủ 14 công trình: bài toán, kết quả thực báo cáo, giới hạn và vai trò với đề tài. Kiểm tra các tiền lệ gần nhất ngoài danh sách trước khi gọi một ý tưởng là mới; ghi rõ ngày và phạm vi tra cứu.
2. Phân biệt kiến thức đã có, suy luận của bạn, đóng góp đề xuất và kết quả đã chạy. Không bảo đảm “chưa từng công bố” chỉ dựa vào không tìm thấy. Trích dẫn nguồn thật, có link trực tiếp và đúng trạng thái xuất bản; không gán workshop/preprint thành hội nghị chính.
3. Viết đề cương tiếng Việt theo chính mẫu đã gửi; giữ các trường hành chính chưa biết ở dạng trống. Đặt chi tiết dài trong bản thảo bài báo tiếng Anh kèm tóm tắt Việt.
4. Trong bài báo, thống nhất ký hiệu; định nghĩa có nguồn; phát biểu bài toán và giả thiết; mã giả khớp cài đặt; ví dụ số tự tính từng bước có nhãn; định lý phải có chứng minh; nêu phản ví dụ/giới hạn và độ phức tạp tính cả oracle. Không chuyển cận cần thành điều kiện đủ, timeout thành vô nghiệm, hoặc sàn score thành bảo đảm NDCG.
5. Thiết kế dữ liệu train/validation/test theo thời gian, chống rò rỉ, train-only popularity, nguồn dữ liệu và metadata thật; baseline gần nhất, LP/MILP, ablation, metric và thống kê phù hợp batch. Chỉ điền bảng kết quả sau khi thực chạy. Ghi lại seed, môi trường, input, code hash và trạng thái solver.
6. Xuất hai file Word, mã mô phỏng và README vào một thư mục; kiểm tra DOCX, trích dẫn, định dạng và kiểm thử trước khi đóng gói. Nêu rõ phần chưa thực hiện và việc cần người hướng dẫn duyệt về mặt học thuật.

Tiêu chí hoàn thành: tất cả 14 nguồn có ánh xạ; mọi số liệu có nguồn hoặc log; mọi bảo đảm có giả thiết; có code chạy ví dụ và kiểm tra oracle; đề cương đúng các mục mẫu; tài liệu tham khảo không bịa; hai Word đọc được và gói có thể tái lập.
