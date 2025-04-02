# Crypto Pattern Scanner

## Cài đặt TradingView Charting Library

1. Đăng ký tài khoản TradingView Developer: https://www.tradingview.com/HTML5-stock-forex-bitcoin-charting-library/

2. Sau khi được phê duyệt, tải Charting Library từ repository của TradingView

3. Copy các file từ thư mục `charting_library` vào `app/static/charting_library/`:
```bash
app/
  static/
    charting_library/
      charting_library.min.js
      chart.css
      ...
```

## Cấu Trúc Project

```
app/
├── __init__.py              # Flask app initialization
├── routes.py               # API endpoints & route handlers
├── models/
│   └── pattern.py          # Pattern database model
├── services/
│   ├── binance_service.py  # Binance API integration
│   ├── pattern_analyzer.py # Technical analysis
│   └── telegram_service.py # Notifications
├── static/
│   ├── css/
│   │   └── style.css      # Custom styles
│   ├── js/
│   │   ├── main.js        # Main dashboard logic
│   │   ├── tradingview-chart.js    # Chart initialization
│   │   ├── pattern-overlay.js      # Pattern visualization
│   │   └── price-levels.js         # Entry/SL/TP handling
│   └── charting_library/  # TradingView library files
└── templates/
    └── index.html         # Main dashboard template
```

## Khởi Động Development

1. Cài đặt dependencies:
```bash
pip install -r requirements.txt
```

2. Chạy migration:
```bash
python scripts/apply_migration.py
```

3. Chạy development server:
```bash
run_dev.bat
```

## Tính Năng

1. TradingView Chart
- Hiển thị biểu đồ nến theo thời gian thực
- Vẽ các mô hình giá đã phát hiện
- Tùy chỉnh các mức Entry/SL/TP bằng kéo-thả
- Tính toán Risk:Reward tự động
- Gửi cảnh báo qua Telegram

2. Pattern Recognition
- Phát hiện tự động 12+ mô hình giá phổ biến
- Đánh giá độ tin cậy dựa trên nhiều chỉ báo
- Lọc và sắp xếp theo độ tin cậy
- Lưu trữ lịch sử phát hiện

3. Notifications
- Gửi thông báo Telegram định kỳ mỗi giờ
- Cảnh báo khi phát hiện mô hình mới
- Chi tiết điểm vào, SL/TP và R:R ratio
