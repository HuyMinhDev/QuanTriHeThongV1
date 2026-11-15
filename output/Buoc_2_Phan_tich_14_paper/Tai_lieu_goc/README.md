# Nguồn bài gốc và repo

Các bài đã được đọc qua toàn văn/nguồn web và đối chiếu với phần mã nguồn truy cập được. Phiên làm việc không tải trực tiếp được PDF/Git clone vì kênh mạng của shell không phân giải được GitHub; thư mục này không giả lập các file PDF chưa tải.

Link bài, DOI và code của từng paper có trong các file `NN_*.md` tại đây và `../danh_muc_nguon.json`. Phần mã đã đọc nằm ở `../Ma_nguon/`; đọc `SOURCE.md` để biết chính xác phần đã truy cập, phần thiếu và trạng thái license/commit.

Để lấy PDF và repo đầy đủ trên máy có kết nối Internet, từ thư mục gói chạy:

```bash
python3 Tai_lieu_goc/TAI_NGUON_CHINH_THUC.py
python3 Tai_lieu_goc/TAI_NGUON_CHINH_THUC.py --download
```

Lệnh đầu chỉ liệt kê. Lệnh thứ hai tải PDF và shallow-clone repo, không cài/chạy code. Có thể chọn một bài, ví dụ `--download --paper 11`. Tệp đang có được giữ nguyên; script ghi trạng thái thật và commit sau khi clone. Publisher có thể yêu cầu quyền truy cập hoặc thay đổi link; khi tải không được, mở link chính thức trong Word. Phiên bản tác giả/arXiv có thể khác bản final, cần ghi đúng phiên bản khi tái lập.

Dataset, model weights và API credentials không được mặc định cung cấp bởi việc có repo; làm theo README và điều kiện nguồn gốc.
