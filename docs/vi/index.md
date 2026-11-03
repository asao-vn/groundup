# groundup (tiếng Việt)

**Mô phỏng tự nhiên theo từng tầng. Luật của mọi tầng phía trên đều do máy
tự rút ra từ tầng dưới, không viết tay.**

groundup là dự án nghiên cứu mã nguồn mở của [ASAO](https://asao.vn).

## Ý tưởng

Vật lý, hóa học và sinh học thường được mô phỏng bằng những mô hình tách rời.
Luật của tầng trên, chẳng hạn tốc độ phản ứng trong tế bào, thường do con người
đo trong phòng thí nghiệm rồi nhập vào. groundup làm theo hướng ngược lại:

1. Chỉ tầng dưới cùng (cơ học lượng tử) được viết tay, và giải bằng công cụ đã
   được kiểm chứng.
2. Luật của tầng kế tiếp do máy **tự rút ra** từ kết quả tầng dưới, kèm hồ sơ
   nguồn gốc: lấy từ đâu, rút bằng cách nào, mất bao nhiêu thông tin.
3. Tầng trên chỉ chạy bằng luật đã rút ra.
4. Mọi tầng đều được so với số đo thực nghiệm có trích nguồn.

Năm 1929, Dirac viết rằng các định luật vật lý cần cho toàn bộ hóa học đã được
biết đầy đủ; khó khăn chỉ là các phương trình quá phức tạp để giải
([Dirac 1929](../references.md#dirac1929)). groundup thử đẩy ranh giới đó
từng bước một.

## Khoảng trống mà dự án nhắm tới

Khoa học hiện nay đang tiến từ hai đầu nhưng chưa gặp nhau
(chi tiết: [Vision](../vision.md)):

- **Từ dưới lên:** "lò phản ứng nano" chỉ dùng luật lượng tử mà vẫn tự tìm ra
  đường tạo glycine ([Wang et al. 2014](../references.md#wang2014)). Nhưng nó chỉ
  chạy được vài nghìn nguyên tử trong vài nano giây.
- **Từ trên xuống:** năm 2026 lần đầu có mô phỏng trọn chu kỳ sống của một tế bào
  tối giản ([Thornburg et al. 2026](../references.md#thornburg2026)). Nhưng tốc độ
  phản ứng trong đó lấy từ thí nghiệm, không tự sinh ra từ vật lý.

Ở giữa là một chuỗi mà luật tầng trên tự sinh ra từ tầng dưới. Chưa ai làm được
chuỗi đó.

## Vì sao không mô phỏng cả tế bào từng nguyên tử?

- **Lượng tử bùng nổ theo cấp số nhân:** giải chính xác chỉ làm được với hệ rất nhỏ
  ([Feynman 1982](../references.md#feynman1982)).
- **Thang thời gian:** mỗi bước mô phỏng chỉ khoảng một femto giây. Theo ước lượng
  của dự án, một giây sống của tế bào nhỏ nhất (khoảng 6 tỷ nguyên tử,
  [Stevens et al. 2023](../references.md#stevens2023)) cần khoảng 200.000 năm
  tính toán, ngay cả với giả định máy rất nhanh.

Vì vậy groundup không cố mô phỏng cả tế bào. Nó xây **các mối nối** giữa các tầng,
để ngày càng ít luật phải nhập tay. Chi tiết: [Concepts](../concepts.md).

## Bước đầu tiên: M0, phân tử H₂

1. **Tầng lượng tử:** giải chính xác phương trình Schrödinger cho H₂.
2. **Cầu nối:** máy tự rút ra luật liên kết giữa hai nguyên tử từ kết quả đó.
3. **Tầng nguyên tử:** hai nguyên tử chuyển động theo định luật Newton và luật vừa
   rút ra.
4. **Kiểm chứng:** so với số đo của NIST.

| Đại lượng | groundup | Thực nghiệm | Sai số |
|---|---|---|---|
| Độ dài liên kết | 0.7426 Å | 0.7414 Å | +0.16% |
| Tần số dao động | 4411 cm⁻¹ | 4401 cm⁻¹ | +0.22% |
| Năng lượng phá liên kết | 4.430 eV | 4.478 eV | −1.06% |
| Bước nhảy dao động đầu tiên | 4154 cm⁻¹ | 4159 cm⁻¹ | −0.10% |

Hai chỗ mất thông tin được ghi lại có chủ đích: hình dạng luật liên kết chỉ xấp xỉ
đường cong thật (độ lệch dao động sai 5.8%), và nguyên tử cổ điển không có dao động
điểm không của lượng tử (6.1%). Chi tiết: [M0](../milestones/m0-h2.md).

## Tiếp theo

M1 là phản ứng hóa học đầu tiên: H + H₂ → H₂ + H. Vẫn chỉ có hydro nên tầng lượng
tử vẫn giải chính xác được, và đây sẽ là lần đầu liên kết tự đứt và tự hình thành
trong mô phỏng. Xem [Roadmap](../roadmap.md).

## Nguồn

Mọi thông tin lấy từ công trình khác đều có trích dẫn trong
[References](../references.md).
