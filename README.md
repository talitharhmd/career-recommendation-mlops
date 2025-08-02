# 🎯 Career Recommendation Platform - Proyek MLOps

Repositori ini merupakan bagian dari proyek Final Project MLOps yang bertujuan membantu mahasiswa tingkat akhir dan pencari kerja awal untuk mendapatkan **rekomendasi pelatihan dan sertifikasi** yang relevan berdasarkan deskripsi pekerjaan impian mereka.

---

## 🚀 Fitur Utama
Sistem rekomendasi ini:
- Menggunakan pendekatan TF-IDF untuk mentransformasi teks.
- Menghitung kemiripan kosinus (similarity score) untuk mencocokkan *job title* dengan course relevan.
- Menyediakan API dengan endpoint `/recommend` yang bisa menerima input dan memberikan output berupa kursus yang relevan.
- Dataset kursus diperoleh melalui _web scraping_ menggunakan Selenium.

---

## 📁 Struktur Folder
📁 FINAL PROJECT/
│
├── src/
│   ├── __init__.py
│   ├── main.py                     # Skrip utama untuk scraping dan preprocessing
│   └── app.py                      # API Flask untuk rekomendasi kursus (dulu plask.py)
│
├── tests/
│   ├── __init__.py
│   └── test_api.py                 # Skrip untuk menguji endpoint API (dulu test.py)
│
├── data/
│   └── courses_classentral.csv     # Dataset hasil scraping dari Class Central
│
├── models/
│   ├── tfidf_vectorizer.pkl        # Model TF-IDF yang disimpan
│   └── item_similarity_matrix.pkl  # Matriks kesamaan item untuk kursus (dulu matriks TF-IDF untuk kursus)
│
├── requirements.txt                # File dependensi
├── .gitignore                      # File untuk mengabaikan berkas yang tidak perlu di-commit
└── README.md                       # Dokumentasi proyek


## 📡 Menjalankan API Secara Lokal
1. Pastikan Anda sudah menginstal semua dependensi:
   ```bash
   pip install -r requirements.txt
2. Jalankan API menggunakan:
python plask.py
3. Uji endpoint menggunakan test.py:
python test.py

## 🛠️ Endpoint API
- Endpoint: /recommend
- Metode: POST
- Input (form-data):
- query: string deskripsi pekerjaan
- top_n: jumlah kursus yang direkomendasikan (opsional, default = 3)
Contoh Respons:
[
  {
    "query": "web developer",
    "title": "AI for Clinical Trials and Precision Medicine - Ruishan Liu",
    "category": "Computer Science",
    "platform": "YouTube",
    "language": "English",
    "certificate": "No Certificate",
    "average_rating": 4.9,
    "price_type": "Free",
    "reviews": "10 reviews",
    "duration": "56 minutes",
    "link": "https://www.classcentral.comhttps://www.classcentral.com/classroom/youtube-ai-for-clinical-trials-and-precision-medicine-ruishan-liu-132489",
    "similarity_score": 0.7243166453431845
  },
  ...
]

## Output Model
Output model disimpan dalam format:
- tfidf_vectorizer.pkl
- item_similarity_matrix.pkl
- Output JSON untuk integrasi front-end: PP_MLOps_Talitha Rahmadewati W_Keisha Hernantya Z_Output.json

## 👥 Tim
- Talitha Rahmadewati W
- Keisha Hernantya Zahra
