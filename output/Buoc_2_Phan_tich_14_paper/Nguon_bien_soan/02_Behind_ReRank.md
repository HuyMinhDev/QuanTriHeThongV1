# 02. Behind the Re-Rank: giải thích cái giá của tái xếp hạng công bằng

## 1. Nhận diện và cách dùng bài trong luận văn

Raciel Yera và Luis Martínez công bố **Behind the Re-Rank: Explaining Fairness in Top-N Recommendations**, UMAP 2026, tr. 21–29, DOI https://doi.org/10.1145/3774935.3806165. Bản tác giả đọc được tại https://ruja.ujaen.es/server/api/core/bitstreams/78628cee-deca-474f-9dad-ca0bd6fc0e8c/content. Repository chính thức: https://github.com/ryera/fairness-explanation-topn. PDF bản lưu còn DOI placeholder ở một số vị trí; dùng DOI hoàn chỉnh của publication link trong repository để trích dẫn.

Đây là công trình về **giải thích tác động của reranking**, không phải đề xuất một optimizer mới tối ưu ba mục tiêu. Nó đặc biệt hữu ích sau khi luận văn đã có reranker accuracy–diversity–exposure hoạt động: ngoài hỏi hệ đạt metric gì, ta hỏi hệ đã đẩy/hạ loại sản phẩm nào và người dùng hiểu thông điệp ra sao. Chương phân tích bài gốc và README, có ví dụ tự tạo và kế hoạch mở rộng; chưa chạy pipeline gốc hoặc khảo sát người thật.

## 2. Kiến thức nền và bản đồ đọc

Hãy tưởng tượng ứng dụng vốn định giới thiệu năm nhà hàng quen thuộc. Sau chính sách tăng cơ hội cho một nhóm ít hiển thị, hai nhà hàng bị đổi chỗ. Người dùng nhìn thấy thay đổi nhưng không biết lý do. Một giải thích chung “hệ ưu tiên công bằng” chưa cho biết item nào chịu ảnh hưởng. Ngược lại, nói rõ “món bạn thích đã bị hạ” có thể khiến họ cảm thấy mất lợi ích. Đây là vấn đề đồng thời kỹ thuật và hành vi.

Người mới cần hiểu ba tầng: recommender tính điểm, reranker thay danh sách, explainer mô tả thay đổi. Sau đó học cây quyết định như mô hình phân loại dễ đọc: điều kiện về genre/location dẫn đến nhãn tăng hoặc giảm hạng. Cây chỉ mô phỏng kết quả của reranker; nó không trở thành reranker và không tự nhận diện nguyên nhân nhân quả.

Đọc §3 trước để hiểu cách tạo nhãn và luật; §4 để biết fidelity đo trên users nào; §5 để đọc user study; sau đó quay về related work §2. Khi xem bảng, luôn hỏi metric thuộc utility, độ trung thành của lời giải thích hay cảm nhận người dùng. Ba loại bằng chứng này khác nhau. Tất cả phép suy luận số/toy trong chương được ghi riêng để không bị nhầm với thí nghiệm tác giả.

## 3. Đầu vào, đầu ra và câu hỏi nghiên cứu

Đầu vào gồm tập user U, items I, điểm S_ui của backbone, top-P candidates mỗi user, thuộc tính item X và một thuộc tính xác định nhóm được bảo vệ. Reranker tạo top-N với N<P. Explainer nhận hai danh sách trước/sau cùng metadata; nó học luật nào thường đi với việc item tăng hoặc giảm hạng. Đầu ra gồm các luật, fidelity của chúng và câu giải thích bằng template.

Điểm khác với nghiên cứu chỉ tối ưu exposure là đầu ra có ngôn ngữ cho user. Luật “thuộc genre Adventure thì thường bị hạ khi tăng Action” là một mô tả hành vi trong thiết lập được quan sát; không có nghĩa mọi phim Adventure bị phân biệt đối xử, hoặc chính genre đã gây ra kết quả. Điểm relevance và tương quan metadata cũng tham gia quá trình chọn item.

Tác giả đặt các câu hỏi về tính đáng tin của luật qua MF/VAECF, độ nhạy với định nghĩa fairness và ảnh hưởng kiến trúc tới kiểu thuộc tính bị thay thế. User study tiếp tục hỏi cách diễn đạt có đổi cảm nhận không. Đây không phải thử nghiệm tỷ lệ mua thật; cũng không đo tác động dài hạn của fairness lên nhà cung cấp.

## 4. Công trình trước và khoảng trống có điều kiện

Các phương pháp fairness post-processing đã biết cách thay danh sách. Các giải thích phản thực thường hỏi cần sửa dữ liệu/thuộc tính gì để đạt fairness. Hướng ở bài này bắt đầu từ một can thiệp đã xảy ra: item nào được thay thế, đặc trưng chung của chúng là gì, và diễn đạt sao cho người xem hiểu được. Người học nên phân biệt câu factual “đã hạ nhóm này” với counterfactual “nếu lịch sử khác thì kết quả khác”.

Khoảng trống sát đề tài có thể là giải thích đúng các ràng buộc exposure và diversity trong một reranker mới, bằng tiếng Việt, có kiểm tra hiểu đúng thay vì chỉ thang hài lòng. Nhưng việc dịch template hoặc đổi dataset tự nó chưa đủ là đóng góp mới. Cần so với các cơ chế giải thích công bằng đã có, đo fidelity dưới drift và chứng minh thông điệp không che mất một đánh đổi quan trọng.

Một giới hạn của surrogate toàn cục là nhiều users có cùng metadata item nhưng score và candidates khác nhau. Nếu cây chỉ dùng đặc trưng item, nó có thể không mô tả được vì sao cùng item tăng với user này mà giảm với user khác. Đó là giả thuyết kiểm tra bằng dữ liệu, không phải kết luận chắc rằng phương pháp tác giả thất bại.

## 5. Ký hiệu và định nghĩa qua ví dụ

`L_base_u` là danh sách gốc của user u; `L_re_u` là danh sách sau reranking. `P` là số ứng viên, `N`/`K` là độ dài danh sách cuối tùy ký hiệu trong bài. `A_ui∈{0,1}` cho biết item có được chọn hay không; nó không trực tiếp biểu diễn mọi hoán vị vị trí. `S_ui` là score, `λ` là trọng số fairness, `I_p` và `I_np` là hai nhóm item.

`R_c` là tỷ lệ nhóm được bảo vệ trong lịch sử dùng làm target của calibrated visibility ở bài này. Nó khác phân bố sở thích cá nhân P(u) của ADF. `w_i` là trọng số chú ý theo thứ hạng; trong công thức exposure của bài nó gắn với **thứ hạng gốc**. Nếu luận văn dùng vị trí cuối để đo exposure, phải khai báo khác biệt thay vì coi hai phép đo hoàn toàn giống nhau.

`Δ(i,u)` là vị trí mới trừ vị trí cũ. Nếu item từ thứ 4 lên thứ 2 thì Δ=−2, nhãn promotion +1. Nếu từ thứ 2 xuống thứ 4 thì Δ=+2, nhãn demotion −1. Item rời danh sách được gán dịch chuyển dương theo quy ước của bài. Trường hợp Δ=0 không thuộc hai nhánh trong Eq. 3; khi tái lập phải kiểm tra cách code xử lý, không tự gán thành promotion.

`T` là cây surrogate, `D_disc` là dữ liệu luật từ users discovery, `D_val` từ users validation. `Fid` là độ đúng dự đoán nhãn promotion/demotion trên D_val. Nếu đo trên chính tập huấn luyện, đó không phải bằng chứng luật khái quát. `Sacr_Attr` là thuộc tính thường xuất hiện trong luật demotion, không mặc nhiên là biến nhân quả quan trọng nhất.

## 6. Công thức reranking: đọc từng thành phần

Eq. 1 có dạng `max_A (1−λ)Σ S_ui A_ui − λ F(A,I_p,I_np)`, với `Σ_i A_ui=N`, `A_ui` nhị phân. Phần đầu giữ utility theo score; phần sau phạt lệch fairness. λ=0 trả trọng tâm về score; λ lớn làm thay đổi utility để giảm penalty. Để so λ giữa mô hình, thang score và normalization F phải rõ. Một mô hình score từ 0–100 sẽ có cân bằng khác mô hình score 0–1 nếu giữ mọi thứ còn lại.

Với symmetric visibility, penalty là độ chênh tỷ lệ được chọn của hai nhóm. Calibrated visibility phạt chênh giữa tỷ lệ nhóm p và target R_c. Exposure parity thêm trọng số vị trí rồi so hai nhóm với hệ số chuẩn hóa Z. Không có một định nghĩa “công bằng duy nhất” ở đây; thay target đổi bài toán chuẩn tắc. Đặc biệt ép 50/50 không tương đương giữ tỷ lệ catalog hoặc tỷ lệ tương tác.

Đây là mô hình chọn tập item, được giải bằng CBC qua PuLP theo bài. Không được nhầm rằng Eq. 1 đã chứa biến gán item vào từng vị trí cuối. Nếu muốn áp ràng buộc exposure đúng vị trí cuối, một formulation khác có thể dùng biến x_uir; đó là mở rộng cần phân tích chi phí. Với bài toán nhỏ có thể duyệt tổ hợp để kiểm tra solver, nhưng phương pháp duyệt này chỉ phục vụ toy.

Eq. 2–3 chuyển thay đổi vị trí thành nhãn. Eq. 4 tính `Fid=Σ 1[T(x_i)=y_i]/|D_val|`. Ví dụ đúng 7/8 nhãn cho Fid=0,875. Nếu 95% item đều demotion, một mô hình dự đoán mọi item demotion đạt 0,95 nhưng ít hữu ích. Vì vậy luận văn nên thêm balanced accuracy, precision/recall từng nhãn và confusion matrix; đây là bổ sung đề xuất, không nói rằng bài đã báo đầy đủ chúng.

Eq. 5 đếm đặc trưng xuất hiện trong các luật âm để tìm thuộc tính “bị hy sinh”. Một đặc trưng có thể xuất hiện nhiều vì biểu diễn one-hot hoặc vì cây dùng nhiều nhánh, nên nên kiểm tra ổn định qua bootstrap. Eq. 6 dùng chênh NDCG gốc trừ mới rồi trung bình theo user. Bảng có phần trăm: phải phân biệt công thức chênh tuyệt đối với cách chuẩn hóa bảng. Không suy mức tăng NDCG tuyệt đối từ một tỷ lệ khi chưa có NDCG nền.

## 7. Mã giả giải thích và phạm vi lý thuyết

```text
Chuẩn bị backbone, candidates và nhãn nhóm item
Tách users cho discovery và validation
Với từng thiết lập fairness và lambda:
  tạo L_base và L_re
  đối chiếu vị trí; gán promotion/demotion theo quy ước
  ghép nhãn với các thuộc tính được phép dùng để giải thích
  huấn luyện cây nhỏ trên users discovery
  đo fidelity trên users validation
  duyệt các đường từ gốc tới lá để lấy luật
  chuyển điều kiện luật sang template có kiểm tra bằng chứng
Đánh giá riêng ngôn ngữ giải thích bằng user study
```

Bài này không đưa định lý rằng cây độ sâu ba luôn giải thích đúng reranker. Fidelity là bằng chứng thực nghiệm. Tính tối ưu solver thuộc formulation và thời gian giải cụ thể, không đồng nghĩa NDCG test tối ưu. Mọi giải thích dùng từ nguyên nhân cần cẩn trọng: cây học quan hệ thống kê của outcome. Muốn chứng minh một thuộc tính gây thay đổi cần can thiệp hoặc phân tích phản thực có giả định rõ.

Câu template cũng phải bám đúng rule. Không thể lấy một luật có fidelity 0,7 rồi nói với từng user rằng “chắc chắn item này bị hạ vì thuộc tính A”. Nên phân biệt giải thích tổng quát cho nhóm với giải thích từng quyết định, có hỗ trợ và mức không chắc chắn. Đây là định hướng thực hành của chương, không phải một chức năng đã có sẵn trong repo.

## 8. Ví dụ tính tay về utility và fairness

Ví dụ mới: user có bốn ứng viên A,B,C,D, score 0,95;0,93;0,88;0,80. A,B ở nhóm không bảo vệ, C,D ở nhóm bảo vệ, chọn K=2. Target calibrated visibility bằng 0,5. Đặt `F=|n_p/2−0,5|`. Với λ=0,1, tập A,B có tổng score 1,88, F=0,5, objective=0,9×1,88−0,1×0,5=1,642. A,C có score 1,83, F=0, objective=1,647. B,C đạt 1,629. Reranker chọn A,C trong toy này.

Với λ=0,01, A,B có objective=0,99×1,88−0,01×0,5=1,8562; A,C chỉ 1,8117. Khi mức phạt thấp, relevance thắng. Ví dụ chứng minh λ có thể tạo điểm đổi quyết định; nó không chứng minh mọi λ lớn luôn làm metric test giảm. Nếu item C là relevant còn B không, can thiệp có thể tăng NDCG dù tổng score giảm.

Danh sách gốc `[A,B,C,D]`, mới `[A,C]`: A không đổi vị trí, B rời danh sách và bị demotion, C từ vị trí 3 lên 2 nên promotion. Nếu chỉ xét label khác 0, ta được cặp `(B,−1),(C,+1)`, cùng các item rời danh sách theo tập được phân tích. Phải công bố miền mẫu: toàn top-P hay chỉ item đổi. Cách lựa chọn này tác động trực tiếp tới độ mất cân bằng nhãn.

Để minh họa fidelity riêng, giả sử tám nhãn thật là `[-1,-1,+1,+1,-1,+1,-1,+1]`, luật dự báo sai một điểm thì Fid=7/8. Tệp `02_Behind_ReRank.py` duyệt mọi tổ hợp hai trong bốn item để in objective, nghiệm của hai λ và ví dụ fidelity. Nó không huấn luyện Cornac, không học CART, không chạy user study; lời giải thích sinh từ toy không phải output code tác giả.

## 9. Bản đồ code và lệnh nào đã có căn cứ

README chính thức xác định `expl_fairness_source.py` là script chính chứa recommendation, fairness reranking và rule extraction. `data.zip` chứa tài nguyên dữ liệu; `detailed results` có kết quả offline/rules, bảng và `working_scenario.pdf`; `user study materials` có kịch bản cùng log phân tích thống kê. Đây là tên/vai trò được xác minh ở README, không phải các module tự đặt.

Lệnh cài tác giả ghi là `pip install cornac pandas numpy pulp`, yêu cầu Python 3.x. Bài mô tả CART dùng scikit-learn nên khi dựng môi trường cần kiểm tra thêm package này. Chưa truy cập được nội dung script chính qua web do cache miss trong phiên hiện tại; vì vậy **không liệt kê tên hàm/class bên trong như đã đọc**, không gán flag dòng lệnh hoặc phiên bản solver chưa xác minh. Tải đủ repo ở môi trường có mạng rồi xem script trước khi chạy; không chạy một tệp thiếu data và coi lỗi đó là kết quả tái lập.

`Ma_nguon/02_Behind_ReRank` lưu ghi chú README đã đọc, đường dẫn script và trạng thái thiếu bản thân script. Nó không phải full repo snapshot. Toy độc lập được lưu ở thư mục khác để người đọc không nhầm nó là implementation chính thức. Khi có mã đầy đủ, cần kiểm tra split discovery/validation, xử lý Δ=0, code dựng penalty tuyệt đối, và cách chuyển selected set thành ranking. Bốn điểm đó là kiểm tra có mục đích, không phải lỗi đã chứng minh.

## 10. Thực nghiệm offline gốc: dữ liệu và tham số

MovieLens 1M được báo 6.040 users, 3.883 items, 1.000.209 ratings; HetRec2011 có 2.113/10.197/855.598. Yelp lấy Philadelphia, user có trên 25 ratings, còn 2.609 users, 5.592 items, 180.494 ratings. Recommendation dùng hold-out 80/20. Kiểm tra giải thích còn có lớp chia users 60/40 discovery/validation riêng. Hai phép split phục vụ hai mục đích, không cộng gộp thành “140% dữ liệu” hoặc thay nhau tùy tiện.

MF/Cornac có 30 factors, SGD 50 epochs, lr 0,01, L2 0,02. VAECF có latent 30, tanh, 50 epochs, batch 512, lr 0,001, KL annealing β=0,2. CBC/PuLP giải reranking; top-50 chuyển top-5/10, λ∈{0,01;0,1;0,8}. Cây CART dùng entropy, max_depth=3, min_samples_leaf=5, min_samples_split=4. Chưa xác minh phần cứng chạy toàn bộ thực nghiệm; không tự gán GPU vì có VAE.

Bảng 1, ML1M+MF@10, bảo vệ Action, λ=0,8: utility loss +11,0%, fidelity 0,779, thuộc tính bị hy sinh Adventure. VAECF@10, Animation, λ=0,8: utility loss −0,39%, fidelity 0,999. Dấu âm ở utility loss là cải thiện, không phải accuracy âm. Không so hai dòng khác protected group như một phép ablation chỉ đổi kiến trúc.

## 11. User study: bằng chứng con người không được thay bằng NDCG

§5 mô tả khảo sát within-subjects đã đăng ký trước, tuyển 55 người qua Prolific, loại một attention check, còn 54. Người tham gia xem kịch bản nhà hàng cố định, tám giải thích gồm hai trial cho mỗi trong bốn điều kiện, thứ tự ngẫu nhiên. Hai baseline là counterfactual T1 và global attribute T2; hai cách đề xuất là granular demotion T3 và side-effect promotion T4. Không gọi toàn bộ thiết kế này là ba điều kiện chỉ vì abstract nhóm cách diễn đạt khác nhau.

Bốn thang Likert 1–5 đo confidence, transparency, satisfaction, persuasiveness. Phân tích dùng linear mixed model và so sánh hậu nghiệm. Bảng 3 cho T1 lần lượt 2,41/2,39/2,86/2,50; T4 đạt 2,91/2,92/3,21/2,90. T3 transparency 3,26 cao hơn T4 nhưng satisfaction 2,48. Đây là estimated marginal means, không phải tỷ lệ click hay phần trăm chính xác.

Kết quả gợi ý sự rõ ràng kỹ thuật và mức chấp nhận không luôn đồng biến. Nhưng “framing tích cực” không cấp phép che giấu cái giá thực của chính sách. Muốn áp dụng có trách nhiệm nên đo thêm hiểu đúng khách quan và phát hiện thông tin gây hiểu lầm, cùng tùy chọn xem chi tiết thay đổi. Các yếu tố đó là đề xuất nghiên cứu tiếp, chưa phải kết quả đã đo trong bài.

## 12. Đóng góp và giới hạn có căn cứ

Đóng góp gồm pipeline audit outcome thành luật semantic, so sánh hành vi theo backbone/fairness và khảo sát cách diễn đạt. Tác giả nêu giới hạn một miền nhà hàng cho user study, cỡ mẫu vừa và tương tác ngắn hạn. Độ hài lòng sau đọc một câu không đo niềm tin sau nhiều tuần biết rằng hệ thường xuyên tái phân phối exposure.

Nhận xét riêng là cây fidelity cao chưa chứng minh causal explanation; accuracy của label có thể bị class imbalance; kết quả hold-out chưa trả lời temporal drift/cold-user. So sánh MF/VAE còn cần kiểm soát tuning và protected group trước khi nói latent space là nguyên nhân. Bài đưa diễn giải kiến trúc, còn luận văn nên coi các diễn giải cơ chế như giả thuyết cần thêm can thiệp/ablation.

## 13. Ba hướng phát triển có đối sánh và điều kiện bác bỏ

**Giải thích hai tầng có kiểm tra hiểu đúng.** Tầng đầu nêu mục tiêu exposure ngắn gọn, tầng hai cho phép xem item/thể loại đổi. So T1–T4, bản hai tầng và bản không giải thích trong khảo sát tiếng Việt. Giữ nguyên danh sách và số chữ gần nhau. Đo hiểu đúng bằng câu hỏi tình huống, fidelity, satisfaction. Bác bỏ nếu satisfaction tăng nhưng người xem hiểu sai lý do can thiệp hoặc không hơn template T4 ở cùng độ dài.

**Luật có điều kiện theo user và uncertainty.** Thêm đặc trưng lịch sử, candidate availability và mức chênh score; so cây item-only, cây thêm user và mô hình đơn giản có confidence. Đo fidelity trên users mới/thời gian mới, balanced accuracy, độ dài luật. Ablation từng nhóm đặc trưng. Bác bỏ nếu chất lượng tăng chỉ do leakage user ID hoặc do cây lớn quá mức làm mất khả năng đọc.

**Audit reranker ba mục tiêu.** Tách tác động diversity, exposure và phối hợp bằng ablation cùng checkpoint. Xuất bảng item đổi vì thành phần nào, kiểm tra lại bằng counterfactual tắt thành phần. So giải thích outcome thuần với giải thích có kiểm tra can thiệp. Bác bỏ nếu attribution không ổn định hoặc nhiều nguyên nhân tương tác khiến nhãn đơn “vì fairness” sai. Đóng góp nên là phương pháp audit trung thực, không chỉ giao diện đẹp.

## 14. Tự kiểm và tài liệu tham khảo

Trước khi báo cáo hãy kiểm tra: Fid có tập validation users độc lập không; Δ=0 xử lý thế nào; giải thích dùng feature bảo vệ hay feature khác; bảng có cùng target/λ không; user study có đo hiểu đúng hay chỉ cảm nhận. Khi trích số, ghi bảng, backbone, K, protected group và dấu utility loss. Ví dụ toy chỉ xác nhận phép tính của ví dụ; không gọi đó là tái lập bài gốc.

Nguồn: DOI https://doi.org/10.1145/3774935.3806165; PDF tác giả https://ruja.ujaen.es/server/api/core/bitstreams/78628cee-deca-474f-9dad-ca0bd6fc0e8c/content, §3–6, Eq.1–6, Bảng1–3; repository https://github.com/ryera/fairness-explanation-topn; script cần đọc tiếp https://github.com/ryera/fairness-explanation-topn/blob/main/expl_fairness_source.py. Dữ liệu nền https://grouplens.org/datasets/; framework https://cornac.readthedocs.io/. Nhật ký nguồn trong gói phân biệt README đã đọc với script chưa tải được, tránh hứa một bản tái lập chưa thực hiện.


## Phụ lục A. Danh mục trích dẫn chuẩn hóa
Các mục dưới đây ghi đủ tên công trình, năm/nơi công bố và link để tra cứu. Gồm bài chính và tài liệu đối chiếu cho luận văn; không khẳng định mọi mục đều nằm trong bibliography của bài gốc. Mã A1, A2… chỉ dùng trong phụ lục của tài liệu này.

[A1] Raciel Yera, Luis Martínez. Behind the Re-Rank: Explaining Fairness in Top-N Recommendations. ACM UMAP 2026, tr. 21–29. [DOI 10.1145/3774935.3806165](https://doi.org/10.1145/3774935.3806165). [Bài/toàn văn](https://ruja.ujaen.es/server/api/core/bitstreams/78628cee-deca-474f-9dad-ca0bd6fc0e8c/content); [code](https://github.com/ryera/fairness-explanation-topn).

[A2] Jingzhi Li, Zhiyong Cheng, Richang Hong, Meng Wang. Post-hoc Provider Fairness Adaptation via Hierarchical Exposure Alignment. ACM SIGIR 2026. [DOI 10.1145/3805712.3809597](https://doi.org/10.1145/3805712.3809597). [Bài/toàn văn](https://arxiv.org/html/2605.01524v1); [code](https://github.com/Tam-JQK/Post-train).

[A3] Amanda Aird, Elena Štefancová, Anas Buhayh, Cassidy All, Martin Homola, Nicholas Mattei, Robin Burke. Integrating Individual and Group Fairness for Recommender Systems through Social Choice. ACM RecSys 2025, tr. 177–186; 07/09/2025. [DOI 10.1145/3705328.3748087](https://doi.org/10.1145/3705328.3748087). [Bài/toàn văn](https://doi.org/10.1145/3705328.3748087); [code](https://github.com/that-recsys-lab/individual_fair_recsys2025).

[A4] Jaime Carbonell, Jade Goldstein. The Use of MMR, Diversity-Based Reranking for Reordering Documents and Producing Summaries. SIGIR 1998, 335–336. [DOI 10.1145/290941.291025](https://doi.org/10.1145/290941.291025).

[A5] Xiangnan He, Kuan Deng, Xiang Wang, Yan Li, Yongdong Zhang, Meng Wang. LightGCN: Simplifying and Powering Graph Convolution Network for Recommendation. SIGIR 2020, 639–648. [DOI 10.1145/3397271.3401063](https://doi.org/10.1145/3397271.3401063).
