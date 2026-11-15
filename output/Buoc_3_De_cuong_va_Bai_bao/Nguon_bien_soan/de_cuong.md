# PHẦN I. ĐĂNG KÝ ĐỀ TÀI LUẬN VĂN THẠC SĨ

## I. HỌC VIÊN

Họ và tên: Nguyễn Minh Huy

Ngày, tháng, năm sinh: ………………………… Mã học viên: …………………………

Lớp: ………………………… Ngành: Công nghệ thông tin. Mã ngành: …………………

Cơ quan công tác: …………………………………………………………………………

Điện thoại: ………………………… Email: ……………………………………………

## II. NGƯỜI HƯỚNG DẪN

**1. Người hướng dẫn chính**

Họ và tên: …………………………………………………………………………………

Học hàm, học vị: ………………………… Chuyên ngành: ………………………………

Cơ quan công tác: …………………………………………………………………………

Địa chỉ liên hệ: ……………………………………………………………………………

Điện thoại: ………………………… Email: ……………………………………………

**2. Người hướng dẫn thứ hai (nếu có)**

Họ và tên: …………………………………………………………………………………

Học hàm, học vị: ………………………… Chuyên ngành: ………………………………

Cơ quan công tác: …………………………………………………………………………

Địa chỉ liên hệ: ……………………………………………………………………………

Điện thoại: ………………………… Email: ……………………………………………

<pagebreak>

## III. THÔNG TIN VỀ ĐỀ TÀI

**1. Tên đề tài:** Tái xếp hạng gợi ý đa mục tiêu với kiểm chứng tính khả thi dưới bất định độ phổ biến.

**Tên tiếng Anh:** Multi-objective Recommendation Re-ranking with Feasibility Auditing under Popularity Uncertainty.

**2. Đơn vị quản lý:** Phân hiệu Trường Đại học Thủy lợi tại Bình Dương.

**3. Phương pháp nghiên cứu và kết quả dự kiến:** Tổng quan có đối chiếu 14 công trình đã phân tích và các nghiên cứu gần nhất; mô hình hóa tối ưu nguyên, CVaR và sắp xếp; chứng minh cận dưới loại nhánh vô nghiệm; xây dựng thuật toán duy trì một nghiệm hoàn tất khả thi; mô phỏng và đánh giá trên MovieLens 1M, Amazon 2018 nếu dữ liệu và metadata truy cập được. Sản phẩm dự kiến gồm luận văn, mã Python, giao thức tái lập và bản thảo bài báo.

**4. Yêu cầu thực hiện:** Có kiến thức hệ gợi ý, xác suất, tối ưu và Python; dùng nguồn dữ liệu hợp lệ; có máy tính đáp ứng nghiên cứu thử nghiệm. Mục tiêu triển khai ban đầu trên CPU, RAM 16 GB; phải đo lại cấu hình thực tế và giới hạn bộ nhớ. Tên người hướng dẫn, mã ngành và thông tin hành chính được hoàn thiện theo quyết định/hồ sơ chính thức.

**5. Công việc chuyên môn hiện đang làm có liên quan:** ………………………………

……………………………………………………………………………………………

**6. Trạng thái đề xuất:** Đã có mô hình, chứng minh và mã mô phỏng kiểm tra hữu hạn; chưa huấn luyện, so sánh đầy đủ trên dữ liệu thực. Đóng góp mới và khả năng công bố là mục tiêu cần kiểm chứng, không phải kết luận đã xác nhận.

Tp. Hồ Chí Minh, ngày …… tháng …… năm ……

NGƯỜI ĐĂNG KÝ

(Ký, ghi rõ họ tên)

<pagebreak>

# PHẦN II. NỘI DUNG ĐỀ CƯƠNG CHI TIẾT

## 1. MỞ ĐẦU

### 1.1. Tính cấp thiết của đề tài

Hệ gợi ý chỉ tối ưu độ chính xác có thể tạo danh sách lặp thể loại và tập trung hiển thị vào nhóm phổ biến. Tái xếp hạng cho phép cân bằng utility, đa dạng và exposure sau khi mô hình chấm điểm được cố định. Tổng hợp 14 phân tích cho thấy nhiều hướng bổ sung nhau: điều chỉnh exposure, giải thích công bằng, đa dạng thể loại, tối ưu CVaR, đo Pareto và tối ưu công bằng nhóm [1–14]. Tuy nhiên, mục tiêu công bằng giữa các bài khác nhau; không thể gộp kết quả thành một khẳng định chung rằng cả ba mục tiêu luôn cải thiện.

Các tiền lệ quan trọng đã có sàn utility, kiểm tra khả năng hoàn tất và phân bổ nguyên dưới ràng buộc [15–17]. CVaR là công cụ đã biết [18]. Khoảng trống dự kiến hẹp hơn: kiểm tra rẻ khả năng hoàn tất danh sách khi nhãn phổ biến thay đổi tương quan qua nhiều kịch bản, đồng thời giữ sàn utility dự báo và độ phủ thể loại. Cận dưới độc lập từng kịch bản có thể bỏ qua xung đột lựa chọn cùng một danh sách.

Đề tài thuộc ngành Công nghệ thông tin vì nghiên cứu thuật toán tối ưu, phân tích độ phức tạp và hệ thống thực nghiệm gợi ý. Đề tài có khả năng ứng dụng cho dịch vụ nội dung/thương mại điện tử; chưa có bằng chứng triển khai tại Việt Nam trong tập nguồn khảo sát và không khẳng định đây là hướng chưa từng được nghiên cứu trong nước.

### 1.2. Mục đích và nhiệm vụ nghiên cứu

Mục tiêu là xây dựng và đánh giá cơ chế kiểm chứng tính khả thi cho tái xếp hạng đa mục tiêu. Ba câu hỏi chính: (i) kiểm soát CVaR qua kịch bản có cải thiện rủi ro audit độc lập không; (ii) cận dưới ghép kịch bản có tiết kiệm tổng chi phí kiểm tra không; (iii) duy trì nghiệm khả thi có cạnh tranh với MILP trực tiếp trong cùng thời hạn không? Nhiệm vụ gồm chuẩn hóa bài toán, chứng minh các tính chất, cài đặt, thiết kế baseline và đánh giá có thể tái lập. Các giả thuyết được phép bị bác bỏ bởi kết quả thực nghiệm.

<pagebreak>

### 1.3. Đối tượng và phạm vi nghiên cứu

Đối tượng là một batch người dùng, tập ứng viên hữu hạn và danh sách dài K. Utility là tổng điểm dự báo có trọng số vị trí; diversity là số thể loại phân biệt; exposure là tổng trọng số vị trí dành cho nhóm head. Một danh sách phải dùng chung cho mọi kịch bản. Không nghiên cứu học tăng cường trực tuyến, bảo đảm nhân quả hay công bằng nhân khẩu học. Sàn utility dự báo không đồng nghĩa với bảo đảm NDCG trên dữ liệu kiểm tra.

### 1.4. Cách tiếp cận và phương pháp nghiên cứu

Với nhị phân x_uir, điểm s_ui và trọng số w_r, đặt U_u=Σ_i,r w_rs_uix_uir và H_s=Σ_u,i,r w_rh_isx_uir/(BΣ_rw_r). Yêu cầu U_u≥(1−ε)U_u^base, độ phủ≥d_u và CVaR_α(H)≤θ, trong đó α là mức tin cậy và 1−α là khối lượng đuôi xấu. Nhãn h_is được tạo bằng lấy mẫu lại các khối thời gian của tập huấn luyện, sau đó tính nhóm top 10% phổ biến.

Phương pháp dự kiến WCR giữ một nghiệm hoàn tất đã kiểm tra, dùng cận dưới ghép kịch bản để loại lựa chọn chắc chắn vô nghiệm rồi gọi bộ giải hoàn tất. Cận nhỏ không chứng minh có nghiệm; hết thời gian phải trả “chưa kết luận”. Chứng minh dựa trên risk envelope của CVaR, weak duality, phép đổi chỗ khi sắp xếp và bất biến nghiệm khả thi. MILP, LP và liệt kê đầy đủ được dùng để đối chiếu, không khẳng định toàn bộ thuật toán có độ phức tạp đa thức.

### 1.5. Ý nghĩa khoa học và thực tiễn

Ý nghĩa dự kiến là làm rõ ranh giới giữa chính sách thất bại và tập ứng viên vốn vô nghiệm, đồng thời đánh giá chi phí của kiểm chứng. Cận dưới, CVaR và completion checking dùng nguyên lý đã có; tính mới chỉ có thể nằm ở cơ chế chuyên biệt và bằng chứng thực nghiệm so với tiền lệ gần nhất [15–18,21].

### 1.6. Kết quả dự kiến

Luận văn; mô hình và chứng minh có giả thiết rõ; mã Python; dữ liệu cấu hình/log; so sánh công bằng và bản thảo bài báo. Kiểm tra tổng hợp hiện có 40 bài toán, 240 tiền tố, cận ghép loại thêm 10 tiền tố so với cận độc lập. Đây là kiểm tra hữu hạn, chưa phải kết quả hiệu quả trên dữ liệu thực. Chi tiết thuật toán, ví dụ và chứng minh nằm trong bản thảo kèm theo.

<pagebreak>

## 2. DỰ KIẾN BỐ CỤC LUẬN VĂN

**Mở đầu:** Tính cấp thiết; mục tiêu/nhiệm vụ; đối tượng/phạm vi; tiếp cận/phương pháp; ý nghĩa; kết quả dự kiến.

**Chương 1. Tổng quan:** Hệ gợi ý đa mục tiêu, các nghiên cứu quốc tế và nguồn trong nước kiểm chứng được; phân biệt định nghĩa công bằng; khoảng trống và câu hỏi nghiên cứu.

**Chương 2. Cơ sở lý thuyết và phương pháp nghiên cứu:** Exposure vị trí, utility, độ phủ, CVaR; bài toán hữu hạn; MILP/LP; kịch bản và nguyên tắc đánh giá.

**Chương 3. Phương pháp đề xuất:** Cận dưới độc lập/ghép; WCR; mã giả; chứng minh, phản ví dụ và độ phức tạp; giới hạn của bảo đảm.

**Chương 4. Thực nghiệm:** MovieLens 1M [19], Amazon 2018 [20]; chia thời gian 70/10/20; BPR và LightGCN; baseline Top-K, MMR/SMMR, ElasticRank, FairSort, MILP và ablation. Đo NDCG/Recall, đa dạng, risk audit, trạng thái khả thi, gap, thời gian/bộ nhớ; phân tích CI theo batch và seed.

**Kết luận và kiến nghị:** Trả lời câu hỏi nghiên cứu theo kết quả thực tế, giới hạn, hướng mở. Tài liệu tham khảo và phụ lục tái lập.

## 3. TIẾN ĐỘ THỰC HIỆN DỰ KIẾN

| Thời gian sau khi duyệt | Công việc và sản phẩm |
|---|---|
| Tháng 1 | Chốt phạm vi, rà tính mới, chuẩn hóa dữ liệu và protocol |
| Tháng 2 | Hoàn thiện mô hình, chứng minh, unit test và MILP/LP |
| Tháng 3 | Chạy pilot, đo khả thi/tài nguyên, cài baseline cùng điều kiện |
| Tháng 4 | Thực nghiệm chính, audit độc lập, ablation và drift |
| Tháng 5 | Phân tích thống kê, đánh giá giả thuyết, viết luận văn/bài báo |
| Tháng 6 | Phản biện, sửa, đóng gói mã/dữ liệu và hoàn thiện bảo vệ |

Mốc quyết định: nếu pilot cho thấy MILP trực tiếp tốt hơn hoặc cận ghép không tiết kiệm chi phí, điều chỉnh kết luận/phạm vi với người hướng dẫn, giữ và công bố kết quả âm thay vì dựng số liệu.

Tp. Hồ Chí Minh, ngày …… tháng …… năm ……

NGƯỜI VIẾT ĐỀ CƯƠNG (Ký, ghi rõ họ tên)

<pagebreak>

# Ý KIẾN CỦA CÁC ĐƠN VỊ VÀ NGƯỜI HƯỚNG DẪN

**1. Người hướng dẫn chính**

……………………………………………………………………………………………

……………………………………………………………………………………………

Ngày ……/……/…………. Ký, ghi rõ họ tên: …………………………………………

**2. Người hướng dẫn thứ hai (nếu có)**

……………………………………………………………………………………………

……………………………………………………………………………………………

Ngày ……/……/…………. Ký, ghi rõ họ tên: …………………………………………

**3. Chủ tịch Hội đồng xét duyệt đề cương**

……………………………………………………………………………………………

……………………………………………………………………………………………

Ngày ……/……/…………. Ký, ghi rõ họ tên: …………………………………………

**4. Ban Đào tạo và Công tác sinh viên**

……………………………………………………………………………………………

……………………………………………………………………………………………

Ngày ……/……/…………. Ký, ghi rõ họ tên: …………………………………………
