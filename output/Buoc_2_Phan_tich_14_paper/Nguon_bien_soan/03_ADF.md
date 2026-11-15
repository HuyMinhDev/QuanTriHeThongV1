# 03. ADF: hiểu đúng công bằng theo sở thích và đa dạng có ràng buộc

## 1. Nhận diện bài và phạm vi của chương

Célina Treuillier, Sylvain Castagnos, Evan Dufraisse, Özlem Özgöbek và Armelle Brun công bố **Shift your Focus for the Greater Good: Improving Fairness at no cost for Accuracy and Diversity in News Recommender Systems**, ACM Transactions on Recommender Systems 4(3), Article 44, 1–36, online ngày 05/03/2026, DOI https://doi.org/10.1145/3790097. Mã tác giả: https://github.com/celinatreuillier/ADF_framework. Chương này đối chiếu nội dung bài, README và tệp `re_ranking/ADF.py` được đọc qua web ngày 15/11/2026; chưa huấn luyện hoặc tái lập thực nghiệm gốc.

Điểm phải ghi nhớ ngay: fairness trong ADF là **tính tương thích giữa các khía cạnh được gợi ý và sở thích của một người dùng**. Nó không phải chia đều lượt hiển thị giữa nhà cung cấp. Hai hệ có cùng calibration của từng user vẫn có thể đưa hàng triệu lượt hiển thị cho vài sản phẩm giống nhau. Vì vậy ADF là đối sánh gần về đa dạng có ràng buộc, nhưng không thay thế baseline exposure fairness của luận văn.

## 2. Kiến thức cần có và thứ tự đọc

Trước hết hãy hiểu phân bố xác suất: nếu 10 tin đã đọc gồm 6 thể thao, 3 văn hóa, 1 kinh tế thì hồ sơ sở thích là `(0,6; 0,3; 0,1)`. Tổng bằng một; mỗi tọa độ chỉ mang nghĩa tương đối trong tập chủ đề đã chọn. Sau đó học entropy, khoảng cách giữa hai phân bố và thao tác lấy top-K theo điểm. Chưa cần biết chi tiết Transformer để hiểu reranker vì nó nhận điểm của một mô hình đã có.

Lượt đọc đầu nên đi theo §3.1–3.5 để biết năm bước ADF, bỏ qua tên các backbone. Lượt thứ hai đọc §4 để hiểu chủ đề được định nghĩa ra sao và dữ liệu được tách thế nào. Lượt thứ ba đọc §5.3, so với các baseline ở §5.2; đừng đọc riêng tiêu đề rồi kết luận rằng accuracy luôn không giảm. Cuối cùng mở `ADF.py`, tìm `get_selection_distribution`, `normalized_entropy`, `div`, `homogeneization`, `ADF`; đây là cầu nối từ công thức sang thao tác dữ liệu.

Trong bản tự học này, các phép tính nhỏ, lập luận đại số, phản ví dụ làm tròn và kế hoạch cải tiến bên dưới là **phân tích sư phạm của người biên soạn**, không phải thí nghiệm mới hay định lý mới của tác giả.

## 3. Bài toán nghiên cứu: đầu vào, đầu ra và động cơ

Một recommender tin tức thường lấy các bài có điểm cao nhất. Người chỉ đọc thể thao có thể tiếp tục nhận toàn thể thao. Tăng đa dạng một cách máy móc lại có thể làm hệ đẩy quá nhiều tin của một chủ đề mà người đó gần như không quan tâm. ADF muốn tăng mức đa dạng nhưng giữ thứ tự tương đối của các sở thích, tránh diễn giải việc tăng diversity thành quyền tự ý đảo hướng quan tâm của user.

Đầu vào gồm lịch sử tương tác của user u, tập khía cạnh A, danh sách ứng viên với điểm relevance và nhãn khía cạnh, cùng độ dài K. ADF xây phân bố lựa chọn P(u), tính diversity của P, đặt diversity đích cho user, tìm một phân bố đích tương thích rồi lấy item theo phân bố đó. Đầu ra là danh sách gợi ý cuối và các thông tin diversity mục tiêu/phân bố dùng để kiểm tra.

Giả định quan trọng nằm ở phép biểu diễn. Nếu dùng chủ đề làm khía cạnh thì công bằng chỉ được xét trong không gian chủ đề. Không thể từ đó suy ra hệ giữ nguyên ý kiến chính trị, cảm xúc hoặc quan điểm của người dùng khi chưa đo các khía cạnh đó. Tương tác đã quan sát cũng có thể chịu ảnh hưởng của exposure trước đó; tỷ lệ đọc không mặc nhiên bằng một sở thích thật đã nhận diện nhân quả.

## 4. Nghiên cứu trước làm gì và khoảng trống có điều kiện

Greedy diversification tăng khác biệt giữa các item nhưng không yêu cầu tỷ lệ chủ đề đầu ra phù hợp hồ sơ user. Calibrated recommendation cố làm đầu ra gần lịch sử nhưng có thể giữ nguyên sự tập trung quá mạnh của lịch sử. ADF nối hai ý: thay vì buộc sao chép hoàn toàn lịch sử, tạo một phân bố đa dạng hơn nhưng vẫn tương thích với thứ tự các mối quan tâm. Phần mới cần hiểu là cách kết hợp mục tiêu và ràng buộc theo user, không phải phát minh entropy hay top-K.

Đối với đề tài thương mại điện tử, khoảng trống có điều kiện là: liệu có thể vừa giữ tính tương thích theo user, vừa giới hạn exposure head trên toàn batch, dưới chất lượng hồ sơ không đồng đều? Chưa được gọi đây là khoảng trống toàn ngành chỉ vì ADF không làm. Phải so thêm CatDive, VRisker, SCRUF-D, ElasticRank và các bài quản trị exposure. Cũng cần xác định ưu tiên khi hai ràng buộc xung đột: một user chủ yếu thích nhóm head có thể không đạt đồng thời quota head thấp và calibration sát.

## 5. Từ điển ký hiệu có ví dụ số

`u` là người dùng; `a` là khía cạnh, chẳng hạn thể thao; `m=|A|` là số khía cạnh trong phép đánh giá; `p_a` là tỷ lệ tương tác của user với a. `P=(p_1,…,p_m)` là toàn bộ hồ sơ, `P*` là phân bố đích; `Q` là phân bố thực tế của danh sách cuối. Ba phân bố này phải có cùng thứ tự cột chủ đề. Nếu cột thể thao và văn hóa bị đảo khi join bảng, mọi phép tính vẫn có thể ra số nhưng ý nghĩa sai hoàn toàn.

`H(P)` là entropy chuẩn hóa. `α,β` là tham số biến đổi diversity đích; `t` trong chương này là mức trộn với phân bố đều để tránh nhầm với λ của greedy baseline. Code tác giả dùng tên `l`/`optimal_lambda` cho t. `s_ui` là điểm relevance từ backbone; nó không phải xác suất click trừ khi đã có hiệu chuẩn tương ứng. `l_a` là số item yêu cầu ở khía cạnh a; không phải xác suất. `K` là số vị trí, chẳng hạn 10 hoặc 20.

Ví dụ P=(0,6;0,3;0,1), Q=(0,3;0,6;0,1) có entropy bằng nhau vì chỉ hoán vị tọa độ. Nhưng Q đã đổi ưu tiên thể thao và văn hóa. Ví dụ này giải thích vì sao chỉ khớp entropy không đủ bảo đảm fairness theo định nghĩa ADF.

## 6. Công thức trung tâm và ý nghĩa từng phép biến đổi

Hồ sơ từ tương tác được tính theo dạng `p(a|u)=I_u(a)/I_u(A)` trong §4.4. Với 6/10 tương tác thể thao, p=0,6. Nếu một tin có nhiều nhãn, phải định nghĩa chia trọng số hoặc nhân bản nhãn trước khi tính; không tùy ý dùng cả hai giữa các thí nghiệm.

Entropy chuẩn hóa là `H(P)=−Σ p_a log2(p_a)/log2(m)`, quy ước `0 log 0=0`. Nó bằng 0 khi một chủ đề nhận toàn bộ khối lượng và bằng 1 khi m chủ đề đồng đều. Code `normalized_entropy` chia entropy SciPy cho `log2(len(distribution))`. Trường hợp m=1 cần xử lý riêng trong implementation mới vì mẫu số bằng 0. H cao nói rằng phân bố rộng hơn; nó không chứng minh user hài lòng hơn.

Code hiện thực diversity đích bằng `h*=(1−β)H(P)^(1−α)+β`, trong `div(x,a,b)`. Khi β=0, α=0 cho h*=H(P); α lớn hơn đẩy h* lên đối với H nằm giữa 0 và 1. Biên H=0, α=1 tạo trường hợp lũy thừa cần nêu quy ước rõ ràng. Không nên để hành vi số học của ngôn ngữ âm thầm trở thành giả định nghiên cứu.

Phân bố được làm đồng đều dần theo `P_t=(1−t)P+tU`, với U=(1/m,…,1/m), 0≤t≤1. Một lập luận đại số đơn giản cho ta `P_t(a)−P_t(b)=(1−t)[P(a)−P(b)]`. Vì 1−t không âm, thứ tự hai tọa độ được giữ hoặc trở thành hòa tại t=1. Đây là giải thích sư phạm về tính tương thích của phép trộn, không phải bảo đảm rằng quota sau làm tròn hoặc cảm nhận người dùng cũng giữ nguyên.

Code tìm t trên lưới 0;0,05;…;1 để làm `|H(P_t)−h*|` nhỏ nhất. Đây là tìm kiếm số hữu hạn, không phải nghiệm liên tục chính xác. Sau đó mỗi chủ đề có quota `l_a=round(K p*_a)` và lấy item có điểm cao nhất trong chủ đề đó. Mỗi quota tối ưu riêng về relevance nếu quota đã cố định, item chỉ có một chủ đề và không có ràng buộc chéo. Không được mở rộng kết luận này thành tối ưu toàn cục của bài toán ba mục tiêu bất kỳ.

Bài dùng chỉ số `C_H(P,Q)=0,5×||sqrt(P)−sqrt(Q)||_2` trong Eq.3 để đánh giá calibration. Phép căn lấy theo từng tọa độ, rồi tính chuẩn Euclid. Cần giữ đúng hệ số công thức khi tái lập: ký hiệu Hellinger có nhiều chuẩn hóa trong tài liệu, không tráo công thức rồi so số tuyệt đối. Một khoảng cách gần 0 cho biết Q gần phân bố đích đang xét; nó không nói exposure toàn catalog đều.

## 7. Thuật toán và những chỗ bản cài đặt cần được kiểm tra

Mã giả dưới đây mô tả luồng đã đọc trong `ADF.py`, dùng tên t cho hệ số trộn:

```text
Với từng user u:
  lấy lịch sử train và ứng viên có điểm
  tính P trên các chủ đề đã thống nhất
  h = entropy_chuẩn_hóa(P)
  h_đích = (1-beta)*h**(1-alpha)+beta
  t = argmin trong {0,.05,...,1} |H((1-t)P+tU)-h_đích|
  P_đích = (1-t)P+tU
  Với mỗi chủ đề a:
    quota = round(K*P_đích[a])
    lấy quota item điểm cao nhất trong a
  ghép các item đã chọn và xuất thống kê
```

Tệp gốc có fallback: nếu chủ đề không xuất hiện trong ứng viên, chọn ngẫu nhiên tin chưa đọc của chủ đề từ metadata và gán score 0. Như vậy có nhánh mở rộng ra ngoài tập candidates ban đầu. Khi luận văn cố định candidate pool để so công bằng, cần tách hai cấu hình: giữ nguyên pool và cho phép mở rộng. Không thể so ADF được truy cập toàn catalog với baseline chỉ được 100 ứng viên rồi quy mọi lợi ích cho reranking.

Làm tròn độc lập có thể khiến tổng quota khác K. Với P*=(0,5;0,25;0,25), K=2, phép round kiểu Python cho quota (1;0;0), chỉ được một item. Chương trình minh họa đi kèm chủ động in phản ví dụ này. Cách phân bổ phần dư lớn nhất có thể sửa độ dài nhưng là sửa đổi implementation cần ghi riêng; nó không biến mọi quota thành đúng P* nếu K quá nhỏ. Cũng phải kiểm tra chủ đề có đủ item hợp lệ hay không.

## 8. Ví dụ tính tay từ đầu đến cuối

Đây là ví dụ mới phục vụ giảng giải, không phải bảng kết quả của bài. Giả sử P=(0,6;0,3;0,1), m=3, K=10 và chọn mức trộn minh họa t=0,3. Khi đó P*=(0,52;0,31;0,17). Entropy lịch sử khoảng 0,817 và entropy đích khoảng 0,914. Hồ sơ đa dạng hơn nhưng vẫn giữ thứ tự chủ đề. Quota làm tròn là (5;3;2), tổng bằng 10.

Trong chủ đề A có các điểm 0,99;0,97;0,95;0,94;0,92;0,90, ta giữ năm item đầu. B có 0,89;0,87;0,85;0,80, ta giữ ba item đầu. C có 0,83;0,79;0,70, ta giữ hai item đầu. Tổng điểm của tập chọn là 9,00. Top-10 điểm thuần có sáu A, ba B, một C và tổng điểm 9,11. Đánh đổi relevance trong ví dụ là 0,11 đơn vị điểm, không phải giảm NDCG 0,11. Muốn tính NDCG còn cần nhãn relevant độc lập.

Phân bố thực tế sau quota là Q=(0,5;0,3;0,2), khác P* vì số vị trí hữu hạn. H(Q) xấp xỉ 0,937. Một phép trộn đặt diversity đích 0,914 có thể tạo đầu ra có diversity 0,937 sau làm tròn. Vì vậy phải xuất cả mục tiêu lẫn kết quả đạt được, không chỉ ghi “đã thỏa”. Nếu tập C hết ứng viên, cần báo thiếu quota và chính sách xử lý; không im lặng giảm K.

Tệp `Vi_du_chay_tay/03_ADF.py` tính entropy, quota, item được chọn và phản ví dụ làm tròn. Nó không tải tin tức, không huấn luyện backbone và không được dùng làm bằng chứng tái lập ADF trên MIND.

Để kiểm tra cả bước tìm tham số, cùng P trên nhưng đặt α=0,4, β=0. Diversity đích là `0,817345^0,6≈0,886020`. Quét lưới t theo bước 0,05 cho t=0,20 có sai số nhỏ nhất, entropy 0,886718; P*≈(0,546667;0,306667;0,146667). Với K=10, quota round thành (5;3;1), tổng chỉ bằng 9. Phép tính này, cũng có trong toy, cho thấy luồng năm bước có thể cần xử lý phần dư trước khi so metric ở K cố định. Chương không tự thêm bước sửa vào thuật toán tác giả.

## 9. Bản đồ code và hướng chạy có thể kiểm tra

Trong `re_ranking/ADF.py`, `get_df_by_user` nhóm dữ liệu theo user; `get_selection_distribution` đếm chủ đề; `normalized_entropy` và `compute_entropy_users` tính entropy; `div` tạo đích; `homogeneization` trộn phân bố đều; `ADF` tìm t, phân quota và ghép kết quả. Đầu script đọc tham số `-d`, `-a`, `-v`, file relevance và metadata; cuối script ghi `reco_scores_ADF/...`. `-v` được chia 10, nên giá trị 4 tương ứng α=0,4 trong nhánh tham số ngắn đã đọc.

README gốc cung cấp cách chạy NewsRecLib cho LSTUR/NAML/NPA/NRMS và ví dụ CentroidVector bằng ClayRS. Đây không phải gói `pip install adf` có sẵn. Một lệnh suy ra trực tiếp từ parser là `python re_ranking/ADF.py -d MIND -a NAML -v 4`; chỉ chạy được khi các file đường dẫn tương đối tồn tại đúng cấu trúc. Đây là lệnh hình thành từ code, không phải khẳng định đã chạy thành công. Đọc cả danh sách `list_users_MIND.csv`, metadata và recommendation JSON trước khi thực thi.

Tài nguyên lưu tại `Ma_nguon/03_ADF` là bản trích đọc qua web và ghi chú nguồn, không phải full repository đã clone hay môi trường đã khóa commit. Code có bước min-max scores; khi tất cả score bằng nhau cần quy ước để không chia cho 0. Cache phân bố cũng cần gắn checksum với split để tránh tái dùng nhầm sau thay đổi dữ liệu. Đây là kiểm tra triển khai đề xuất, chưa phải lỗi được tái hiện trên thực nghiệm tác giả.

## 10. Thiết kế thực nghiệm gốc và cách đọc kết quả

ADF đánh giá MIND-small tiếng Anh và Adressa-1week tiếng Na Uy. Sau lọc ban đầu, bài báo nêu lần lượt 20.292/7.343 users, 66.986/10.106 news và 1.260.987/654.190 tương tác. Phân tích sau đó giữ người dùng test có ít nhất năm tương tác, còn 3.757/1.633 users. Sự lọc này phải được nêu khi chuyển sang câu hỏi cold-user: kết quả chính không đại diện nhóm ít tương tác bị loại.

Các backbone là CentroidVector, LSTUR, NAML, NPA, NRMS; so thêm greedy diversification và calibration. MIND dùng validation công khai làm test, train chia tiếp theo timestamp. Adressa dùng năm ngày đầu train; ngày cuối tách 20% validation và phần còn lại test; tạo 20 negatives/click theo protocol được mô tả. Cần xem cấu hình cụ thể trước khi tái lập, không thay bằng random split rồi coi là cùng thiết lập.

Ngôn ngữ là Python, với ClayRS, NewsRecLib, spaCy, tomotopy; biểu diễn MIND dùng LDA 128 chiều, Adressa dùng bge-m3 1.024 chiều. Các metric gồm Precision@20, ILD theo nội dung, SRecall chủ đề và C_H. ILD dùng embedding khác nhau giữa hai miền nên số tuyệt đối không trực tiếp so được. Chưa xác minh một cấu hình phần cứng huấn luyện đầy đủ trong nguồn code đã đọc; không tự điền GPU hoặc thời gian chạy.

§5.3.2 và Hình 7–8 cho thấy tính phụ thuộc dữ liệu: MIND+NAML Precision@20 từ khoảng 0,100 xuống khoảng 0,092 tại α=0,4; Adressa+NAML từ 0,081 lên 0,105 tại α=0,6. Những số này không chứng minh mọi cấu hình đều không tốn accuracy. Chúng cũng là Precision, không đổi nhãn thành Recall/NDCG. Đừng tính phần trăm từ câu diễn giải nếu trị số trong hình hoặc văn bản không nhất quán; ưu tiên ghi cặp số và cấu hình.

## 11. Đóng góp, giới hạn và đánh giá phản biện

Đóng góp nên trình bày thành cơ chế đặt diversity mục tiêu theo user, xây phân bố tương thích và reranking theo phân bố đó, kèm bằng chứng trên hai miền tin tức. Tác giả nhận giới hạn dữ liệu lịch sử, tập baseline và metric còn hẹp, đánh giá offline và nhu cầu user study. Các kết luận về hành vi xã hội cần thí nghiệm riêng; tin đa dạng hơn không tự chứng minh giảm phân cực.

Nhận xét riêng cho luận văn gồm độ tin cậy của lịch sử ngắn, quota nguyên, thiếu ứng viên, chi phí fallback và thiếu ràng buộc exposure toàn hệ. Định nghĩa tương thích có thể giữ thứ tự chủ đề nhưng không giữ nguyên mọi tỷ lệ; điều này là chủ ý mô hình, không nên gọi là sai. Ngược lại, nếu đề tài muốn công bằng cơ hội hiển thị sản phẩm thì cần định nghĩa thêm đối tượng và mẫu số exposure, không thể chỉ đổi tên C_H.

## 12. Ba hướng phát triển có phép bác bỏ

**Hướng A: calibration đồng thời với exposure budget.** Thêm giới hạn exposure head và diversity tối thiểu, giữ cùng backbone/candidates. So ADF nguyên bản, exposure-only, diversity-only, tổ hợp tuyến tính và bản ràng buộc. Đo NDCG, ILD, C_H, tỷ lệ vi phạm và runtime. Ablation bỏ từng ràng buộc. Bác bỏ lợi ích nếu cải thiện exposure chỉ do hy sinh accuracy vượt ngưỡng đã đăng ký hoặc do mở rộng candidate pool riêng.

**Hướng B: hồ sơ có bất định.** Dùng Bayesian smoothing hoặc bootstrap lịch sử train để ước lượng khoảng tin cậy của P. User có hai hành vi không được nhận cùng mức tin cậy với user có 200 hành vi. So ADF điểm ước lượng, smoothing cố định và thích nghi theo uncertainty; đánh giá theo nhóm lịch sử. Bác bỏ nếu lợi ích biến mất khi cùng tuning budget hoặc chỉ có ở nhóm dày. Không gọi smoothing một mình là đóng góp mới.

**Hướng C: quota khả thi và bằng chứng tính đúng.** Dùng phân bổ nguyên có kiểm soát phần dư, giới hạn tồn kho candidates và slack khi không khả thi. Công bố phản ví dụ, chứng minh luôn đủ K dưới điều kiện có đủ items, rồi đo độ lệch đích. So rounding gốc, largest-remainder và tối ưu nguyên nhỏ. Nếu chỉ sửa lỗi độ dài mà không tạo lợi ích khoa học khác, đóng góp phù hợp là engineering/reproducibility, chưa đủ tự đảm bảo một paper mới.

## 13. Tự kiểm tra và tài liệu tham khảo

Hãy tự trả lời: entropy bằng nhau có chứng minh hai phân bố tương thích không; tại sao tăng α lại khác tăng λ greedy; quota đúng có đủ bảo đảm relevance không; và vì sao C_H thấp chưa giải exposure? Nếu chưa trả lời được, hãy chạy ví dụ nhỏ rồi đổi K=2 và đổi thứ tự chủ đề. Kiểm tra checksum split, metadata mapping, mức độ trùng candidates và file raw metrics trước khi viết kết luận.

Nguồn chính: bài ADF DOI https://doi.org/10.1145/3790097, đặc biệt §3–6; repository và README https://github.com/celinatreuillier/ADF_framework; tệp đã đọc https://raw.githubusercontent.com/celinatreuillier/ADF_framework/main/re_ranking/ADF.py. Công cụ nền: https://newsreclib.readthedocs.io/en/latest/ và https://swapuniba.github.io/ClayRS/. Nguồn dữ liệu: https://msnews.github.io/ và https://reclab.idi.ntnu.no/dataset/. Các hướng nghiên cứu, toy và chẩn đoán triển khai trong chương là đề xuất của người biên soạn, không phải kết quả thực nghiệm được gán cho các nguồn này.


## Phụ lục A. Danh mục trích dẫn chuẩn hóa
Các mục dưới đây ghi đủ tên công trình, năm/nơi công bố và link để tra cứu. Gồm bài chính và tài liệu đối chiếu cho luận văn; không khẳng định mọi mục đều nằm trong bibliography của bài gốc. Mã A1, A2… chỉ dùng trong phụ lục của tài liệu này.

[A1] Célina Treuillier, Sylvain Castagnos, Evan Dufraisse, Özlem Özgöbek, Armelle Brun. Shift your Focus for the Greater Good: Improving Fairness at no cost for Accuracy and Diversity in News Recommender Systems. ACM Transactions on Recommender Systems 4(3), Article 44, 1–36; online 05/03/2026. [DOI 10.1145/3790097](https://doi.org/10.1145/3790097). [Bài/toàn văn](https://doi.org/10.1145/3790097); [code](https://github.com/celinatreuillier/ADF_framework).

[A2] Rikiya Takehi, Fernando Diaz, Tetsuya Sakai. Diversification as Risk Minimization. ACM WSDM 2026, tr. 618–628. [DOI 10.1145/3773966.3777985](https://doi.org/10.1145/3773966.3777985). [Bài/toàn văn](https://arxiv.org/html/2510.22681v1); [code](https://github.com/RikiyaT/VRisk).

[A3] Jaeri Lee, Jongjin Kim, U Kang. CatDive: A simple yet effective method for maximizing category diversity in sequential recommendation. PLOS ONE 21(1), e0341419; 30/01/2026. [DOI 10.1371/journal.pone.0341419](https://doi.org/10.1371/journal.pone.0341419). [Bài/toàn văn](https://journals.plos.org/plosone/article?id=10.1371/journal.pone.0341419); [code](https://github.com/snudatalab/CatDive).

[A4] Diego Carraro, Derek Bridge. Enhancing Recommendation Diversity by Re-ranking with Large Language Models. ACM Transactions on Recommender Systems 4(2), Article 18, 1–40; trang publisher hiển thị 22/11/2025. [DOI 10.1145/3700604](https://doi.org/10.1145/3700604). [Bài/toàn văn](https://arxiv.org/html/2401.11506v2); [code](https://github.com/cdiego89phd/chat-reranking).

[A5] Jaime Carbonell, Jade Goldstein. The Use of MMR, Diversity-Based Reranking for Reordering Documents and Producing Summaries. SIGIR 1998, 335–336. [DOI 10.1145/290941.291025](https://doi.org/10.1145/290941.291025).
