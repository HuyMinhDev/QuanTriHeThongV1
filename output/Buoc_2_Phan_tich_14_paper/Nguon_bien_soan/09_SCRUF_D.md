# 09. SCRUF-D: kết hợp công bằng cá thể và nhóm bằng lựa chọn xã hội

## 1. Bài báo, nguồn đọc và cách dùng tài liệu

Amanda Aird, Elena Štefancová, Anas Buhayh, Cassidy All, Martin Homola, Nicholas Mattei và Robin Burke, **Integrating Individual and Group Fairness for Recommender Systems through Social Choice**, RecSys 2025, trang 177–186. Bản chính thức: https://doi.org/10.1145/3705328.3748087. Code: https://github.com/that-recsys-lab/individual_fair_recsys2025. Kiểm tra ngày 15/11/2026.

SCRUF-D viết tắt Social Choice for Recommendation Under Fairness–Dynamic. Bài 2025 mở rộng dòng nghiên cứu có trước; không phải lần đầu xuất hiện kiến trúc nhiều fairness agents. Tài liệu này dẫn các mục, công thức và bảng của bài chính thức, sau đó xây dựng giải thích, ví dụ và hướng thực nghiệm độc lập. Những ví dụ tự xây dựng không được xem là kết quả của tác giả.

Người học nên ghi riêng ba câu: hệ thống lấy danh sách từ đâu; ai được quyền yêu cầu công bằng; cơ chế nào hòa giải các yêu cầu. Khi trả lời được ba câu đó mới nên đọc bảng kết quả, vì một điểm fairness cao không có ý nghĩa nếu chưa biết fairness dành cho đối tượng nào.

## 2. Kiến thức nền và lộ trình đọc cho người mới

Cần biết top-N recommendation, BPR-MF, catalog coverage, NDCG và khái niệm bỏ phiếu theo thứ hạng. “Agent” trong bài là một thành phần biểu diễn mục tiêu, không mặc định là LLM hay chatbot tự suy luận. Có thể hiện thực agent bằng vài hàm thống kê và một quy tắc sắp xếp.

Ví dụ một cửa hàng có ba tiếng nói. Người mua muốn sản phẩm phù hợp; nhóm nhà cung cấp muốn có tỷ lệ hiển thị nhất định; bộ phận phát triển danh mục muốn nhiều sản phẩm khác nhau được nhìn thấy. Nếu cộng ngay tất cả vào một loss thì phải chọn một cách đo chung. Social choice cho phép mỗi bên gửi một thứ hạng rồi dùng quy tắc tổng hợp. Nhưng cách tổng hợp vẫn là lựa chọn thiết kế, không tự nhiên là công bằng tuyệt đối.

Trình tự đọc gợi ý: Mục 3 và Hình 1 để hiểu luồng xử lý; Mục 4 để hiểu agent; Mục 5.2–5.4 để biết dữ liệu và cơ chế; Mục 5.5 để đọc metric; Bảng 2–4 để kiểm tra đánh đổi. Đọc kết luận sau cùng để xem tác giả có thừa nhận sự phụ thuộc miền và xung đột mục tiêu hay không.

## 3. Bài toán, đầu vào và đầu ra

Đầu vào của một lượt là user đang đến, danh sách ứng viên do recommender chấm điểm, trạng thái lịch sử gợi ý gần đây và tập fairness agents. Đầu ra là danh sách ngắn được rerank và lịch sử exposure được cập nhật. Backbone có thể là BPR nhưng kiến trúc không buộc chỉ dùng BPR.

Mỗi agent có ba thành phần. Fairness metric nhìn lại lịch sử để đánh giá mục tiêu đã được phục vụ tới đâu. Compatibility metric xem user hiện tại có phù hợp để hỗ trợ mục tiêu ấy không. Ranking function đề xuất thứ tự item theo lợi ích của agent. Sau đó allocation quyết định agent nào tham gia lượt này; choice mechanism tổng hợp thứ hạng agent và sở thích user.

Điều này khác cân bằng mỗi danh sách độc lập. Một provider có thể ít xuất hiện ở vài lượt rồi được hỗ trợ ở lượt sau. Vì vậy thứ tự user, độ dài cửa sổ lịch sử và trạng thái khởi tạo có thể ảnh hưởng kết quả. Muốn tái lập phải lưu cả trình tự arrival, không chỉ lưu danh sách user trong test.

## 4. Nghiên cứu trước và khoảng trống cần phát biểu chính xác

Nguồn gần nhất là **Dynamic Fairness-aware Recommendation Through Multi-agent Social Choice**, DOI https://doi.org/10.1145/3690653, và **Social Choice for Heterogeneous Fairness in Recommendation**, arXiv https://arxiv.org/abs/2410.04551. Các công trình đó đã nghiên cứu nhiều quan tâm fairness và hai bước allocation/aggregation. Đóng góp bài 2025 tập trung thêm provider-side individual fairness vào cơ chế vốn đã có group fairness.

Individual fairness trong thực nghiệm được vận hành qua catalog coverage. Đây là một proxy cụ thể; không đồng nhất hoàn toàn với định nghĩa “các cá thể tương tự phải được đối xử tương tự” trong mọi bài fairness. Nếu luận văn dùng coverage, hãy gọi rõ coverage-based item fairness và báo thêm phân bố exposure để tránh một item được xuất hiện một lần rồi coi như vấn đề đã giải quyết.

Khoảng trống điều kiện cho đề tài ba mục tiêu là phối hợp coverage/exposure với diversity trong danh sách và kiểm soát thiệt hại theo nhóm user. Không thể tuyên bố “dùng nhiều agents” là mới. Cần chứng minh cơ chế hoặc chính sách mới có lợi ở điều kiện mà SCRUF-D gốc gặp khó, chẳng hạn mục tiêu đối kháng, lịch sử ít hoặc arrival distribution thay đổi.

## 5. Ký hiệu và các đại lượng dễ nhầm

| Ký hiệu | Diễn giải |
|---|---|
| u, i | User đang đến và item ứng viên |
| l, l' | Danh sách ban đầu và danh sách sau rerank |
| L | Tập danh sách của nhiều lượt/user |
| C | Catalog item đủ điều kiện được gợi ý |
| g, I_g(i) | Nhóm provider và chỉ báo item thuộc nhóm |
| E_g | Tỷ lệ item thuộc nhóm g trong các danh sách |
| theta | Target exposure hoặc coverage do thiết kế đặt |
| Ebar_g | Fairness đã chuẩn hóa theo target |
| F, m_i | Tập agents và fairness score của từng agent |
| m_1/2 | Điểm tổng hợp fairness bằng biểu thức căn bậc hai |
| k, k' | Độ dài danh sách gốc và cuối khi tính NLIP |
| rho(i,l) | Vị trí item i trong danh sách gốc, bắt đầu từ 1 |
| RBO | Mức chồng lấp các tiền tố danh sách theo định nghĩa của bài |
| NLIP | Item được nâng sâu nhất từ danh sách gốc, đã chuẩn hóa |

Coverage của cả hệ thống và độ đa dạng một danh sách có mẫu số khác nhau. Hai danh sách đều chỉ có một thể loại nhưng chứa những item khác nhau vẫn có thể làm catalog coverage cao. Ngược lại, mỗi danh sách có nhiều thể loại nhưng luôn lặp lại cùng vài item có thể cho coverage thấp. Hai mục tiêu cần đo riêng trong luận văn.

Target 30% không phải quan sát có sẵn trong dữ liệu, cũng không tự chứng minh là mức hợp lý về đạo đức. Nó là đầu vào chính sách. Khi thay target 30% thành 40%, đang thay yêu cầu của hệ thống, không chỉ đổi một siêu tham số kỹ thuật trung tính.

## 6. Công thức fairness và tổng hợp: đọc từng phép toán

Ở Mục 4.1, exposure nhóm được tính bằng:

```text
E_g = tổng số item thuộc g trong tất cả các danh sách
      / tổng số vị trí của tất cả các danh sách.
Ebar_g = min(1, E_g / theta_g).
```

Đây là đếm vị trí không chiết khấu, nên rank 1 và rank 10 đóng góp như nhau. Nếu luận văn đổi sang 1/log2(rank+1), phải đặt tên biến thể và tái đo mọi baseline cùng định nghĩa. Ví dụ 4/20 vị trí là 20%; target 25% cho mức hoàn thành 0,8. Việc này không có nghĩa 80% người dùng hài lòng.

Ở Mục 4.2, coverage bằng số item khác nhau từng được gợi ý chia kích thước catalog. Với 100 item và hợp danh sách chứa 60 item, coverage=0,6. Nếu chuẩn hóa target 0,5 thì tỷ số là 1,2. Bảng của bài có giá trị coverage chuẩn hóa lớn hơn 1; không coi đó là raw coverage 120%. Cần phân biệt tỷ số chưa chặn với phiên bản min(1,·) dùng trong logic agent.

Công thức (1) tổng hợp m fairness scores:

```text
m_1/2 = (sum_j sqrt(m_j))^2 / m^2.
```

Với [0,8;0,2], trung bình bằng 0,5 còn biểu thức này bằng 0,45. Chênh lệch phản ánh việc một agent có mức phục vụ thấp. Dùng trung bình đơn thuần có thể che một mục tiêu bị bỏ lại. Tuy nhiên phép tổng hợp vẫn lựa chọn một quan niệm về cân bằng; nó không thay thế bảng metric riêng cho từng agent.

Công thức (2) của bài tính RBO bằng trung bình độ chồng lấp các tiền tố đến độ dài ngắn hơn. Khi hiện thực, dùng đúng biểu thức bài đã dùng; không tự đổi sang một biến thể RBO có tham số continuation rồi so trực tiếp số. NLIP xét vị trí gốc xa nhất trong các item đã được nâng vào danh sách cuối, trừ độ dài cuối và chuẩn hóa phần đuôi có thể khai thác.

## 7. Cơ chế phân bổ và bỏ phiếu

Least Fair chọn agent đang kém được phục vụ nhất theo fairness score chuẩn hóa; không dùng compatibility như Lottery/Weighted. Lottery chọn ngẫu nhiên một agent dựa trên nhu cầu và compatibility. Weighted cho nhiều agents tham gia với trọng số. Không nên tự viết một công thức xác suất cụ thể rồi gán cho tác giả nếu chưa đối chiếu implementation của phiên bản đang chạy.

Borda cho điểm theo vị trí trong mỗi phiếu rồi cộng, có thể thêm trọng số người mua. Copeland xét thắng–thua giữa các cặp item, nên hai item có thể đảo thứ tự dù điểm số gốc gần nhau. Rescoring dùng kết hợp điểm số, tận dụng cường độ preference mà cách bỏ phiếu thuần thứ hạng bỏ qua.

Sự khác biệt có thể thấy bằng hai phiếu cùng thứ tự nhưng khoảng cách score rất khác. Borda nhìn hai phiếu như nhau nếu thứ hạng giống nhau; rescoring có thể phân biệt 0,99 so với 0,01 và 0,51 so với 0,50. Vì vậy không có lý do mặc định cơ chế nào luôn tốt hơn. Bài kiểm tra nhiều tổ hợp và quan sát kết quả thay đổi theo miền dữ liệu.

## 8. Lý thuyết, lập luận và giới hạn bảo đảm

Bài không đưa ra một định lý rằng mọi tập agents đều đạt tất cả fairness targets. Đóng góp chủ yếu là thiết kế và bằng chứng thực nghiệm. Khi trình bày trước hội đồng, không đổi việc metric có công thức thành bảo đảm thuật toán hội tụ hay đảm bảo fairness toàn cục.

Có thể tự kiểm tra một tính chất của công thức tổng hợp bằng đại số. Với hai score a,b≥0, m_1/2=(a+b+2sqrt(ab))/4. Trung bình là (a+b)/2. Hiệu trung bình trừ m_1/2 bằng (sqrt(a)−sqrt(b))^2/4≥0. Đây là **diễn giải đại số của người biên soạn**, không phải một định lý mới được bài công bố. Nó giải thích tại sao score tổng hợp phạt mất cân bằng.

Lập luận về chi phí trong Mục 3.1 dựa trên số agents, số ứng viên và cửa sổ lịch sử bị chặn. Với 50 ứng viên và tối đa ba agents trong thí nghiệm, chi phí bổ sung nhỏ. Nếu tăng candidates từ 50 lên 50.000, so cặp của Copeland không còn là một “hằng số nhỏ”. Khi luận văn mở rộng phạm vi phải viết chi phí theo kích thước thật, không chỉ trích lại kết luận thời gian thực.

Một phản ví dụ khái niệm hữu ích: chỉ có hai nhóm item A/B; tất cả ứng viên đều thuộc A nhưng target B là 40%. Không cơ chế bỏ phiếu nào đạt target. Hoặc hai agents cùng yêu cầu toàn bộ K vị trí cho hai tập rời nhau: hai yêu cầu không thể đồng thời thỏa. Như vậy tính khả thi phải được kiểm tra trước khi quy mọi thất bại cho cơ chế allocation.

## 9. Mã giả theo một lượt user

```text
state = lịch sử danh sách đã phát
for user u theo thứ tự arrival cố định:
    candidates, user_scores = backbone(u)
    for agent a:
        fairness[a] = đánh giá state trong cửa sổ lịch sử
        compatibility[a] = mức phù hợp user u với mục tiêu a
        vote[a] = thứ hạng candidates theo mục tiêu a
    active_agents = allocation(fairness, compatibility)
    combined = choice(user_vote, active_votes, weights)
    output = lấy K item đầu của combined
    cập nhật state bằng output
```

Đây là mã giả học tập. Các bước phải giữ causal order: agent lượt t chỉ xem trạng thái đã xảy ra trước lượt t, không xem danh sách tương lai. Nếu chia dữ liệu theo thời gian, compatibility cũng phải được tính từ lịch sử hợp lệ. Một lỗi phổ biến là dùng toàn bộ ratings để xác định user thích gì rồi đánh giá trên test; điều đó làm lộ thông tin.

## 10. Ví dụ tự xây dựng: từng phiếu đến danh sách cuối

Bài có Hình 1 về kiến trúc, không cung cấp ví dụ bốn item này. **Ví dụ sau do người biên soạn tự xây dựng** và dùng Borda có trọng số để minh họa choice; không giả định đó là cấu hình thắng ở mọi dữ liệu.

Candidates là A,B,C,D. User xếp A>B>C>D; agent nhóm xếp C>A>B>D; agent coverage xếp D>C>B>A. Với bốn item, điểm Borda mỗi phiếu từ cao xuống là 3,2,1,0. Trọng số user=2, hai agents đều=1. A nhận 2×3+2+0=8; B nhận 2×2+1+1=6; C nhận 2×1+3+2=7; D nhận 0+0+3=3. Kết quả A>C>B>D; top-2 đổi từ [A,B] thành [A,C].

RBO theo định nghĩa bài: ở tiền tố 1, overlap=1; tiền tố 2, overlap=1/2; trung bình=0,75. Item C có rank gốc 3; NLIP=(3−2)/(4−2)=0,5. Nếu trước đó hệ thống đã gợi [A,B], hợp item với danh sách mới là {A,B,C}; coverage=3/4=0,75. Chia target 0,85 cho tỷ số chuẩn hóa 0,882353.

Ví dụ này chưa tính compatibility hay trạng thái nhiều lượt, và không chứng minh accuracy tăng. Nếu C không liên quan user, việc nâng C có thể làm NDCG giảm. Bài tập tiếp theo là thay nhãn relevance rồi tính NDCG bằng tay, sau đó đổi trọng số user từ 2 thành 4 để xem mức can thiệp giảm như thế nào.

File `Vi_du_chay_tay/09_SCRUF_D.py` dùng thư viện chuẩn và đã chạy với kết quả Borda A=8,B=6,C=7,D=3; RBO=0,750000; NLIP=0,500000. File cũng kiểm tra tỷ số 1/0,65=1,538462 để minh họa vì sao target-normalized coverage có thể vượt 1.

## 11. Đọc mã tác giả và thực hành cài đặt

README chính thức xác nhận thư mục `configurations/`, `scruf_d/`, `post_processing/`. Các lựa chọn cấu hình gồm `least_fair`, `product_lottery`, `weighted_product_allocation`; choice gồm `weighted_scoring`, `RuleBorda`, `RuleCopeland`. File entry mà README chỉ dẫn là `scruf_d/__main__recsys_25.py`. Các đường dẫn này giúp đối chiếu tên cơ chế bài với lựa chọn chạy.

Trong phiên biên soạn, README và cấu trúc repo truy cập được; nội dung đầy đủ entry và các lớp agent chưa tải được qua web cache. Do đó tài liệu không bịa tên class/function bên trong hay khẳng định đã audit implementation từng cơ chế. Ghi chú Ma_nguon/09_SCRUF_D/SOURCE.md phân biệt rõ phần xác minh và phần chưa có.

README yêu cầu Python 3.9 trở xuống vì Whalrus. Từ môi trường phù hợp, cài và chạy theo cấu trúc repo:

```bash
pip install -r scruf_d/requirements.txt
# Trong configurations/movie_experiments/all:
python ../../../scruf_d/__main__recsys_25.py
# Trong post_processing:
clang -shared -fPIC -o metrics.so metrics.c
python run_movie_experiments.py
```

Đây là lệnh được README mô tả, chưa được thực thi trên dữ liệu chính thức trong lần biên soạn. Cần tải dataset và tạo file đúng định dạng trước. Trên máy 16 GB, MovieLens 1M thích hợp để thử; AMBAR đầy đủ có catalog lớn hơn nhiều và cần đo RAM.

## 12. Thiết kế và số liệu thực nghiệm của bài gốc

Mục 5 dùng MovieLens 1M bổ sung metadata từ The Movies Dataset và AMBAR music. MovieLens có 6.040 user, 3.706 item và 1.000.209 ratings; random split 80/20 lặp năm lần. AMBAR có 31.013 user, 443.921 item, 3.311.462 tương tác; lấy năm mẫu 6.000 user. BPR-MF trong RecBole sinh 50 candidates rồi đánh giá top-10; đây không phải temporal split.

MovieLens có mục tiêu nhóm Women W/D 30%, Non-English 7%, coverage target 0,85. AMBAR dùng Women Artists 25% và coverage target 0,65. Những target mang tính minh họa của nghiên cứu. Baseline là BPR không rerank, individual-only, group-only và kết hợp, cùng các tổ hợp allocation/choice.

Bảng 3, MovieLens, Both Lottery+Borda: NDCG 0,085±0,008 so gốc 0,073±0,002; coverage chuẩn hóa 0,728±0,053 so 0,661±0,056. Dấu ± là khoảng tin cậy 95% theo các partitions, không phải standard deviation. Bảng 2 AMBAR, Both cho NDCG 0,101 so 0,103 gốc; tác động fairness kết hợp hạn chế hơn. Không kết luận phương pháp luôn tăng accuracy.

Bảng 4 cho tương quan coverage và Women W/D −0,416; với Non-English −0,210. Tương quan quan sát không xác định nguyên nhân, nhưng đủ cảnh báo rằng tăng độ phủ item không tự động tăng cơ hội mọi nhóm provider. Nên lưu bảng đầy đủ thay vì chỉ trích cấu hình MovieLens đẹp nhất.

## 13. Đóng góp, hạn chế và ba hướng luận văn có thể bác bỏ

Tác giả mở rộng kiến trúc với individual fairness, khảo sát kết hợp mục tiêu khác loại và giới thiệu NLIP. Tác giả cũng thừa nhận sự phụ thuộc dataset, cơ chế không có người thắng nhất quán và coverage là một lựa chọn đơn giản chưa xét vị trí. Không gọi các mục tiêu nhóm nhân khẩu trong bài thành fairness pháp lý cho sản phẩm nếu không có ngữ cảnh tương ứng.

Nhận xét độc lập: cửa sổ lịch sử có thể gây quên hoặc dao động; ít user tương thích có thể khiến agent bị đói allocation; đối sánh chủ yếu với các biến thể kiến trúc chưa thay thế benchmark rerank mới hơn. Random split và metadata bổ sung cũng tạo giới hạn ngoại suy. Muốn phát triển luận văn cần kiểm tra những điều kiện đó thay vì chỉ thêm agent mới vào demo.

Hướng A: agent exposure có trọng số vị trí cộng agent diversity. Đối sánh SCRUF-D gốc, MMR, ElasticRank và phiên bản thêm từng agent. Đo ILD, NDCG, exposure Gini và violation theo thời gian. Bác bỏ nếu lợi ích fairness chỉ là chuyển item xuống cuối danh sách hoặc diversity thấp đi khi đo đúng vị trí.

Hướng B: chống agent starvation. Theo dõi số lượt liên tiếp không được chọn; thử hạn mức phân bổ tối thiểu trong khi giữ ràng buộc accuracy. Ablation bỏ compatibility và bỏ lịch sử. Bác bỏ nếu hạn mức làm giảm accuracy nhiều hơn mức fairness đạt thêm hoặc chỉ tốt ở một thứ tự user.

Hướng C: compatibility có bất định cho cold users. Dùng lịch sử ngắn để ước lượng khoảng tin cậy, giảm can thiệp khi sở thích chưa chắc. So compatibility gốc và quy tắc dựa số tương tác đơn giản, cùng temporal split. Bác bỏ nếu mô hình phức tạp không hơn quy tắc đơn giản ở cùng ngân sách tuning.

## 14. Tài liệu tham khảo và bài tập đọc

- Bài chính, code và DOI: Mục 1; đọc kỹ Mục 4–6.
- SCRUF-D nền tảng: https://doi.org/10.1145/3690653 và https://arxiv.org/abs/2303.00968.
- Heterogeneous fairness: https://arxiv.org/abs/2410.04551.
- BPR: https://proceedings.mlr.press/r7/rendle09a.html.
- MovieLens: https://grouplens.org/datasets/movielens/1m/.
- FairRec: https://doi.org/10.1145/3366423.3380196.
- ElasticRank: https://doi.org/10.1145/3726302.3730106.

Tự kiểm tra hiểu bài bằng hai phản ví dụ: coverage tăng nhưng group fairness giảm; group fairness đạt target nhờ nâng một vài item vốn đã phổ biến nhưng long-tail coverage gần như không đổi. Nếu giải thích được cả hai mà không đánh tráo mẫu số, người học đã nắm đúng đóng góp và giới hạn của bài.


## Phụ lục A. Danh mục trích dẫn chuẩn hóa
Các mục dưới đây ghi đủ tên công trình, năm/nơi công bố và link để tra cứu. Gồm bài chính và tài liệu đối chiếu cho luận văn; không khẳng định mọi mục đều nằm trong bibliography của bài gốc. Mã A1, A2… chỉ dùng trong phụ lục của tài liệu này.

[A1] Amanda Aird, Elena Štefancová, Anas Buhayh, Cassidy All, Martin Homola, Nicholas Mattei, Robin Burke. Integrating Individual and Group Fairness for Recommender Systems through Social Choice. ACM RecSys 2025, tr. 177–186; 07/09/2025. [DOI 10.1145/3705328.3748087](https://doi.org/10.1145/3705328.3748087). [Bài/toàn văn](https://doi.org/10.1145/3705328.3748087); [code](https://github.com/that-recsys-lab/individual_fair_recsys2025).

[A2] Jingzhi Li, Zhiyong Cheng, Richang Hong, Meng Wang. Post-hoc Provider Fairness Adaptation via Hierarchical Exposure Alignment. ACM SIGIR 2026. [DOI 10.1145/3805712.3809597](https://doi.org/10.1145/3805712.3809597). [Bài/toàn văn](https://arxiv.org/html/2605.01524v1); [code](https://github.com/Tam-JQK/Post-train).

[A3] Chen Xu, Jujia Zhao, Wenjie Wang, Liang Pang, Jun Xu, Tat-Seng Chua, Maarten de Rijke. Understanding Accuracy-Fairness Trade-offs in Re-ranking through Elasticity in Economics. ACM SIGIR 2025, tr. 539–548. [DOI 10.1145/3726302.3730106](https://doi.org/10.1145/3726302.3730106). [Bài/toàn văn](https://arxiv.org/html/2504.14991v1); [code](https://github.com/XuChen0427/ElasticRank).

[A4] Steffen Rendle, Christoph Freudenthaler, Zeno Gantner, Lars Schmidt-Thieme. BPR: Bayesian Personalized Ranking from Implicit Feedback. UAI 2009, 460–469. [PMLR và PDF](https://proceedings.mlr.press/r7/rendle09a.html).

[A5] Wayne Xin Zhao và cộng sự. RecBole: Towards a Unified, Comprehensive and Efficient Framework for Recommendation Algorithms. CIKM 2021. [DOI 10.1145/3459637.3482016](https://doi.org/10.1145/3459637.3482016); [code](https://github.com/RUCAIBox/RecBole).
