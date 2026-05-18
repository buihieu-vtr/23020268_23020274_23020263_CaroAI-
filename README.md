# Caro AI (4-In-A-Row) in Python
Một trò chơi cờ Caro (phiên bản ăn 4 nước để thắng) tích hợp trí tuệ nhân tạo (AI) được viết bằng Python. Dự án sử dụng thuật toán tìm kiếm thực nghiệm kết hợp tối ưu hóa để người chơi có thể trực tiếp thử thách độ thông minh với máy tính thông qua giao diện đồ họa `pygame`.

## :mag_right: Tổng Quan 
Trò chơi được cấu hình trên bàn cờ kích thước **9x9**. Khác với luật Gomoku quốc tế tiêu chuẩn, phiên bản này áp dụng luật **ăn 4 nước liên tiếp** (hàng dọc, hàng ngang hoặc đường chéo) để giành chiến thắng nhằm tăng tốc độ trận đấu và tối ưu hóa cho không gian bàn cờ nhỏ.

AI trong dự án được xây dựng dựa trên thuật toán **Minimax** đi kèm kỹ thuật **Cắt tỉa Alpha-Beta (Alpha-Beta Pruning)**. Giao diện trực quan cho phép bạn:
* Lựa chọn chế độ chạy: **Minimax thuần túy** (để quan sát số trạng thái duyệt lớn) hoặc **Minimax + Alpha-Beta** (tối ưu hóa tốc độ).
* Chọn lượt đi: Người chơi đi trước (Quân X - Màu đen) hoặc AI đi trước (Quân O - Màu đỏ).
* Theo dõi các thông số vận hành của AI (thời gian xử lý, số lượng trạng thái đã duyệt) hiển thị thời gian thực qua Terminal.

## :pushpin: Yêu Cầu Hệ Thống 
Để chạy được chương trình, máy tính của bạn cần cài đặt thư viện thư viện `pygame`:
```
'pip install pygame'
```
## :open_file_folder: Cấu Trúc Thư Mục 
├── AI1.py         # Xử lý logic thuật toán Minimax, Alpha-Beta và sắp xếp nước đi (Move Ordering)
├── play1.py       # Khởi tạo giao diện Pygame, quản lý trạng thái màn hình và bắt sự kiện chuột
├── utils1.py      # Định nghĩa cấu hình bàn cờ, kiểm tra thắng thua và hàm đánh giá (Heuristic Evaluation)
└── README.md      # Tài liệu hướng dẫn sử dụng
## :video_game: Hướng Dẫn Chạy Game 

> git clone https://github.com/buihieu-vtr/23020268_23020274_23020263_CaroAI
> cd 23020268_23020274_23020263_CaroAI
> python3 play1.py

Các bước thiết lập trò chơi:
Bước 1 (Chọn thuật toán): Giao diện chính xuất hiện yêu cầu bạn chọn thuật toán cho AI.

  1. MINIMAX ONLY: Duyệt toàn bộ cây quyết định (Chậm hơn).
  
  2. MINIMAX + ALPHA-BETA: Sử dụng kỹ thuật cắt tỉa nhánh thừa để tăng tốc độ phản hồi.

Bước 2 (Chọn lượt đi): Bạn chọn 1. PLAYER FIRST nếu muốn cầm quân X đi trước, hoặc 2. AI FIRST để nhường quyền cho AI (Quân O) khai cuộc tại tâm bàn cờ.

Trong trận đấu: Nhấp chuột vào các giao điểm trên bàn cờ để đặt quân. Hệ thống sẽ luân phiên lượt đi giữa bạn và AI.

Kết thúc & Chơi lại: Khi có bên đạt đủ 4 quân liên tiếp hoặc bàn cờ bị lấp đầy (Hòa), thông báo kết quả sẽ hiển thị ở góc dưới. Nhấn phím R trên bàn phím bất kỳ lúc nào để reset trò chơi về màn hình chọn thuật toán ban đầu.

