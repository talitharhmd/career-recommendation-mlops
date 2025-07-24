# 🎯 Career Recommendation Platform - Proyek MLOps

Sistem ini merupakan backend dari **Career Platform**, sebuah platform digital interaktif yang merekomendasikan pelatihan dan sertifikasi berdasarkan pekerjaan impian pengguna. Proyek ini dikembangkan dalam rangka tugas akhir modul Machine Learning Operations.

---

## 🚀 Fitur Utama
Sistem rekomendasi ini:
- Menggunakan pendekatan TF-IDF untuk mentransformasi teks.
- Menghitung kemiripan kosinus antara deskripsi pekerjaan dan data kursus.
- Menyediakan API dengan endpoint `/recommend` yang bisa menerima input dan memberikan output berupa kursus yang relevan.
- Dataset kursus diperoleh melalui _web scraping_ menggunakan Selenium.

---

## 📁 Struktur Folder
📁 FINAL PROJECT/
│
├── main.py # Skrip utama untuk scraping dan preprocessing
├── plask.py # API Flask untuk rekomendasi kursus
├── test.py # Skrip untuk menguji endpoint API
├── courses_classentral.csv # Dataset hasil scraping dari Class Central
├── tfidf_vectorizer.pkl # Model TF-IDF yang disimpan
├── item_similarity_matrix.pkl # Matriks TF-IDF untuk kursus
├── requirements.txt # File dependensi
└── README.md # Dokumentasi proyek


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
    "title": "Introduction to Data Science in Python",
    "platform": "Coursera",
    "similarity_score": 0.7623
  },
  ...
]

## Output Model
Output model disimpan dalam format:
- tfidf_vectorizer.pkl
- item_similarity_matrix.pkl
- Output JSON untuk integrasi front-end: PP_MLOps_[Nama1]_[Nama2]_Output.json

## 👥 Tim
- Talitha Rahmadewati W
- Keisha Hernantya Zahra
