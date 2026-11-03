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

## Bước thứ hai: M1, phản ứng hóa học đầu tiên D + H₂ → HD + H

Đây là lần đầu tiên liên kết tự đứt và tự hình thành trong mô phỏng. D là
deuteri, tức hydro có thêm một neutron. Dùng D vì phản ứng này đã được đo trực
tiếp ở nhiệt độ cao ([Michael & Fisher 1990](../references.md#michael1990)).
Bề mặt năng lượng chỉ phụ thuộc vào electron và điện tích hạt nhân, không phụ
thuộc khối lượng ([Born & Oppenheimer 1927](../references.md#born1927)). Vì vậy
một bề mặt duy nhất, rút ra từ H₃, dùng được cho mọi đồng vị.

1. **Tầng lượng tử:** giải chính xác H₃ (3 electron) quanh đỉnh rào năng lượng.
   Rào cao 9,94 kcal/mol.
2. **Cầu nối 1:** máy tự rút ra luật phản ứng cho ba nguyên tử (dạng LEPS) từ luật
   liên kết của M0, cộng thêm đúng một tham số. Tham số đó được chọn sao cho rào
   khớp tầng lượng tử, không lấy gì từ thí nghiệm.
3. **Tầng nguyên tử:** bắn D vào H₂ ở 100 mức năng lượng. Không ai bảo chúng phản
   ứng. Dưới 0,45 eV thì D bật ra, từ 0,45 eV trở lên thì liên kết D–H mới tự hình
   thành và H bay đi.
4. **Cầu nối 2:** tính tốc độ phản ứng k(T) chỉ từ luật vừa rút ra, bằng lý thuyết
   trạng thái chuyển tiếp ([Eyring 1935](../references.md#eyring1935)) cộng hiệu
   ứng xuyên hầm ([Wigner 1932](../references.md#wigner1932)).
5. **Kiểm chứng:** so với số đo bằng ống sóng xung kích.

| Nhiệt độ | groundup (cm³/s) | Thực nghiệm (cm³/s) | Tỉ lệ |
|---|---|---|---|
| 700 K | 3,69 × 10⁻¹³ | 3,04 × 10⁻¹³ | 1,21 |
| 1000 K | 2,28 × 10⁻¹² | 2,57 × 10⁻¹² | 0,89 |
| 1500 K | 1,22 × 10⁻¹¹ | 1,35 × 10⁻¹¹ | 0,90 |
| 1900 K | 2,83 × 10⁻¹¹ | 2,73 × 10⁻¹¹ | 1,04 |

Ngưỡng đạt là sai lệch không quá 2 lần, và được chốt trước lần chạy đầu tiên.
Kết quả khớp tốt hơn mức các giả định cho phép, nên một phần là do các sai số
bù trừ nhau. Chẳng hạn, rào ở tầng lượng tử cao hơn ước lượng chính xác nhất
(9,60 kcal/mol, [Peterson et al. 1994](../references.md#peterson1994)) khoảng
0,34 kcal/mol. Mọi chỗ mất thông tin đều được ghi lại. Chi tiết:
[M1](../milestones/m1-dh2.md).

## Tiếp theo

M1b: đếm trực tiếp các quỹ đạo phản ứng trong không gian 3 chiều, với phân tử ở
nhiệt độ thật, trên cùng luật của M1. Tốc độ phản ứng khi đó được đếm ra chứ
không giả định, và sẽ cho biết lý thuyết trạng thái chuyển tiếp sai bao nhiêu.
Xem [Roadmap](../roadmap.md).

## Nguồn

Mọi thông tin lấy từ công trình khác đều có trích dẫn trong
[References](../references.md).
