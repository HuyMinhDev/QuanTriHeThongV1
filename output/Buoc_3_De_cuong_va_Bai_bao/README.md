# Hồ sơ Bước 3 — đề cương luận văn và dự thảo bài báo

Đề tài thống nhất: **Tái xếp hạng gợi ý đa mục tiêu với kiểm chứng tính khả thi dưới bất định độ phổ biến.**

Ngày biên soạn: 15/11/2026. Đầu vào chính là 14 file Word phân tích Bước 2, đề tài CSE631 và mẫu `Mau-trinh-bay-de-cuong-LV-PH-2022.doc` do học viên cung cấp. Đây là hồ sơ nghiên cứu dự kiến, chưa phải luận văn/bài báo hoàn thành thực nghiệm trên dữ liệu thực.

## Mở các tệp nào?

- `01_De_cuong_Luan_van_Thac_si.docx`: đề cương tiếng Việt theo hai phần của mẫu, có đăng ký, sáu mục mở đầu, bố cục, tiến độ, ý kiến/chữ ký và tài liệu tham khảo.
- `02_Du_thao_Bai_bao_WCR.docx`: bản thảo tiếng Anh kèm tóm tắt Việt; tổng hợp cả 14 công trình, đối chiếu tiền lệ gần nhất, mô hình, mã giả, chứng minh, ví dụ số, độ phức tạp, kết quả mô phỏng và protocol dữ liệu thực.
- `Tai_lieu_dau_vao_14_Word/`: bản sao nguyên trạng 14 phân tích đã được đưa vào tổng hợp, để tiện gửi cùng thư mục.
- `Mo_phong/`: mã Python, bộ giải MILP/LP, liệt kê đầy đủ, WCR, unit test và script nghiên cứu nhỏ.
- `Kiem_tra/`: JSON/CSV đầu vào–kết quả mô phỏng, hình khoa học và báo cáo kiểm tra tệp.
- `Nguon_bien_soan/`: bản nguồn có thể sửa, danh mục tài liệu thật, manifest đầu vào và mẫu trình bày.

## Đã làm và chưa làm

Đã đọc bản trích xuất từ đủ 14 file Word; lưu SHA-256 để đối chiếu. Đã xây dựng mô hình hữu hạn, chứng minh với giả thiết rõ ràng, viết ví dụ tự xây dựng và code có thể chạy. Đã chạy 13 unit tests và nghiên cứu 40 instance/240 prefix tổng hợp. Cận ghép mạnh hơn tại 74 prefix và loại thêm 10 prefix so với cận độc lập trong tập thử này. MILP khớp liệt kê về giá trị risk tối ưu tại 40/40 instance.

Chưa tải/huấn luyện lại MovieLens hoặc Amazon, chưa tái lập đầy đủ các baseline xuất bản, chưa đo tốc độ/bộ nhớ trên benchmark thực. Không dùng các số tổng hợp để khẳng định chất lượng gợi ý hay speedup. Những bảng kết quả thực còn thiếu được ghi rõ trong bản thảo, không điền số giả. Mã tải/tiền xử lý dữ liệu thực và huấn luyện scorer là công việc tiếp theo của kế hoạch nghiên cứu, không được giới thiệu là đã triển khai trong gói này.

Tính mới là giả thuyết có điều kiện. CVaR, sàn utility, kiểm tra khả năng hoàn tất, validator, MILP và weak duality đều có tiền lệ. Đóng góp dự kiến hẹp hơn: cận dưới ghép kịch bản trên tập ứng viên còn lại và lợi ích thực tế của nó trong quy trình giữ nghiệm khả thi. Không thể bảo đảm hướng này chưa từng được công bố hoặc sẽ được tạp chí chấp nhận.

## Mẫu trình bày và thông tin cần điền

Đề cương dùng Times New Roman 13, dãn dòng 1,5; lề trên 3,5 cm, dưới 3 cm, trái 3,5 cm, phải 2 cm; số trang ở giữa phía trên, không có nội dung header/footer khác. Bìa dùng cỡ 14, tên đề tài cỡ 16. Mục lục dùng các trường PAGEREF để Word cập nhật theo phân trang thực tế. Dùng Ctrl+A rồi F9 (trên Mac có thể cần Fn+F9) nếu số trang chưa hiện sau khi mở. Hồ sơ hướng tới độ dài khoảng 10 trang theo mẫu; phân trang cuối phụ thuộc Word/font/máy in và cần kiểm tra trong Word trước khi in.

Các trường chưa được cung cấp được để trống: ngày sinh, mã học viên/lớp, mã ngành chính thức, nơi công tác, liên hệ, người hướng dẫn, ngày ký, ý kiến và chữ ký. Tên Nguyễn Minh Huy được suy từ tên hồ sơ hiện có; cần đối chiếu cách ghi chính thức. Không suy diễn giảng viên học phần thành người hướng dẫn luận văn. Tên đơn vị và phần ý kiến theo mẫu năm 2022 do người dùng gửi; cần đơn vị xác nhận nếu biểu mẫu hành chính đã thay đổi.

Đã kiểm tra cấu trúc XML, nội dung, trích dẫn, trường mục lục và thông số định dạng. Môi trường hiện tại không xuất được bản xem trước Word qua Quick Look; không khẳng định đã kiểm tra trực quan từng trang bằng Word. Hình mô phỏng đã được xem trực quan. Không tự điền số trang dự đoán vào mục lục.

## Chạy lại mô phỏng

Môi trường đã chạy: Python 3.14.3, NumPy 2.4.4, SciPy 1.17.1; macOS 26.4.1 arm64. Cần một môi trường có SciPy hỗ trợ `scipy.optimize.milp`; danh sách phiên bản trong `Mo_phong/requirements.txt` là phiên bản thực chạy, không phải cam kết tương thích với mọi máy. Không cần GPU.

```sh
cd Mo_phong
python3 -m unittest test_core -v
python3 run_study.py
```

`run_study.py` ghi lại `../Kiem_tra/simulation_results.json` và CSV. Seed cố định là 20261115. Kết quả logic phải nhất quán; thông báo solver, phiên bản và sai số cuối có thể thay đổi giữa nền tảng. File JSON có inputs, solver evidence, kiểm tra primal và hash source. Đây không phải dữ liệu tương tác thật.

Mặc định WCR dùng enumeration cho bài toán nhỏ. Dùng backend MILP như sau:

```python
from core import wcr, milp_oracle
result = wcr(instance, oracle=lambda p: milp_oracle(
    instance, prefix=p, time_limit=10))
```

Tham số `instance` là đối tượng `core.Instance`, xem `test_core.py` để lấy ví dụ đầu vào. ID item là số nguyên; thể loại là tuple; mỗi item có cùng số scenario. Dùng trọng số vị trí dương, không tăng theo thứ hạng như giả thiết bài toán. `time_limit` trên đây áp dụng từng lần gọi, chưa phải deadline toàn batch. `max_checks` của WCR là ngân sách toàn cục cho kiểm tra ứng viên. `UNKNOWN` không có nghĩa là vô nghiệm. Chỉ kết quả FEASIBLE đã qua `verify` mới thỏa hợp đồng số học theo tolerance.

## Tạo lại Word và quản lý nguồn

Cài `python-docx`, `mistune`, `matplotlib` trong môi trường tương thích rồi chạy:

```sh
python3 Nguon_bien_soan/ve_ket_qua.py
python3 Nguon_bien_soan/tao_tai_lieu.py
python3 Nguon_bien_soan/kiem_tra_tai_lieu.py
```

`references.json` là nguồn metadata cho 37 tài liệu. Bản thảo giữ số [1–37]; đề cương dùng tập chọn lọc được đánh số riêng [1–21]. Repo bên ngoài được dẫn link trong phụ lục bài báo; mã tác giả từng bài và ghi chú phạm vi đọc nằm ở hồ sơ Bước 2. Gói Bước 3 không khẳng định chứa toàn bộ repo của 14 công trình. Không gửi dữ liệu nghiên cứu hoặc email cho người khác bằng công cụ; thư mục ZIP được chuẩn bị để học viên tự gửi Thầy.
