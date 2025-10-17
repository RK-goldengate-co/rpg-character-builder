# RPG Character Builder

## Mô tả
Ứng dụng tạo nhân vật RPG toàn diện với các tính năng:

- **Chọn Class**: Warrior, Mage, Rogue, Cleric, Ranger và nhiều hơn nữa
- **Hệ thống Skill**: Cây kỹ năng phong phú với nhiều nhánh phát triển
- **Chỉ số nhân vật**: Phân bổ điểm cho STR, DEX, INT, WIS, CON, CHA
- **Tùy chỉnh ngoại hình**: Chọn màu tóc, mắt, trang phục, phụ kiện
- **Export file**: Tạo file tương thích với RPG Maker (JSON format)
- **Quản lý Profile**: Lưu và tải nhiều nhân vật khác nhau

## Cấu trúc dự án

```
rpg-character-builder/
├── backend/              # API Python cho xử lý logic
│   ├── api/             # REST API endpoints
│   ├── models/          # Data models
│   ├── services/        # Business logic
│   └── utils/           # Utility functions
├── frontend/            # React UI
│   ├── src/
│   │   ├── components/  # React components
│   │   ├── pages/       # Page components
│   │   ├── services/    # API calls
│   │   └── styles/      # CSS/styling
│   └── public/          # Static files
├── data/                # Cấu hình mẫu
│   ├── classes/         # Class definitions
│   ├── skills/          # Skill trees
│   └── templates/       # Export templates
├── tests/               # Test suites
│   ├── backend/         # Backend tests
│   └── frontend/        # Frontend tests
├── README.md
├── LICENSE
├── .gitignore
├── requirements.txt     # Python dependencies
└── package.json         # Node.js dependencies
```

## Công nghệ sử dụng

- **Backend**: Python 3.9+, Flask/FastAPI
- **Frontend**: React 18+, Material-UI
- **Database**: SQLite/PostgreSQL
- **Export**: JSON format cho RPG Maker

## Cài đặt

### Backend
```bash
cd backend
pip install -r requirements.txt
python app.py
```

### Frontend
```bash
cd frontend
npm install
npm start
```

## Sử dụng

1. Khởi động backend API
2. Khởi động frontend development server
3. Truy cập http://localhost:3000
4. Tạo nhân vật mới hoặc tải profile đã lưu
5. Chọn class, phân bổ skill points, tùy chỉnh ngoại hình
6. Export file cho RPG Maker

## License

MIT License - see LICENSE file for details
