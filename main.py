from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import pandas as pd
from sklearn.metrics.pairwise import cosine_similarity
import pickle
import os # Untuk memeriksa keberadaan file

# Inisialisasi aplikasi FastAPI
app = FastAPI(
    title="Course Recommendation API",
    description="API untuk merekomendasikan kursus berdasarkan kueri pekerjaan menggunakan TF-IDF dan Cosine Similarity.",
    version="1.0.0"
)

# --- Kelas untuk Mendefinisikan Skema Data Input dan Output ---
# Skema untuk input kueri pekerjaan
class QueryInput(BaseModel):
    query: str

# Skema untuk output rekomendasi kursus
class CourseRecommendation(BaseModel):
    title: str
    platform: str
    similarity_score: float

# --- Memuat Model dan Data yang Telah Disimpan ---
# Path ke file-file model dan data
TFIDF_VECTORIZER_PATH = 'tfidf_vectorizer.pkl'
TFIDF_MATRIX_PATH = 'item_similarity_matrix.pkl'

# Variabel global untuk menyimpan model dan data yang dimuat
tfidf_vectorizer = None
tfidf_matrix = None
courses_df = pd.read_csv("courses_classentral.csv")

# Fungsi untuk memuat model dan data saat aplikasi dimulai
@app.on_event("startup")
async def load_models():
    global tfidf_vectorizer, tfidf_matrix, courses_df

    print("Memuat model dan data...")
    try:
        if not os.path.exists(TFIDF_VECTORIZER_PATH):
            raise FileNotFoundError(f"File {TFIDF_VECTORIZER_PATH} tidak ditemukan. Pastikan Anda sudah menjalankah script persiapan.")
        if not os.path.exists(TFIDF_MATRIX_PATH):
            raise FileNotFoundError(f"File {TFIDF_MATRIX_PATH} tidak ditemukan. Pastikan Anda sudah menjalankah script persiapan.")

        with open(TFIDF_VECTORIZER_PATH, 'rb') as f:
            tfidf_vectorizer = pickle.load(f)

        with open(TFIDF_MATRIX_PATH, 'rb') as f:
            tfidf_matrix = pickle.load(f)

        print("Model dan data berhasil dimuat.")
    except FileNotFoundError as e:
        print(f"Error: {e}. Harap jalankan script persiapan model terlebih dahulu.")
        # Opsi: Anda bisa memilih untuk keluar dari aplikasi atau membiarkannya berjalan
        # tetapi endpoint rekomendasi akan gagal. Untuk aplikasi nyata, disarankan keluar.
        import sys
        sys.exit(1) # Keluar jika file penting tidak ada
    except Exception as e:
        print(f"Terjadi kesalahan saat memuat model atau data: {e}")
        import sys
        sys.exit(1)


# --- Endpoint Utama untuk Rekomendasi ---
@app.post("/recommend/", response_model=list[CourseRecommendation])
async def recommend_courses(input: QueryInput, top_n: int = 3):
    """
    Merekomendasikan kursus berdasarkan kueri pekerjaan.

    - **query**: String yang mendeskripsikan pekerjaan (misal: "data analyst", "UI/UX designer").
    - **top_n**: Jumlah kursus teratas yang ingin direkomendasikan (default: 3).
    """
    if tfidf_vectorizer is None or tfidf_matrix is None:
        raise HTTPException(status_code=503, detail="Model belum dimuat. Coba lagi nanti atau periksa log server.")

    # Vektorisasi kueri pekerjaan menggunakan vectorizer yang dimuat
    query_vector = tfidf_vectorizer.transform([input.query])

    # Hitung cosine similarity antara query_vector dan tfidf_matrix (matriks kursus)
    cosine_similarities = cosine_similarity(query_vector, tfidf_matrix).flatten()

    # Dapatkan indeks kursus dengan similaritas tertinggi
    # argsort mengembalikan indeks yang akan mengurutkan array
    # [:-top_n-1:-1] mengambil top_n indeks dari yang terbesar
    related_course_indices = cosine_similarities.argsort()[:-top_n-1:-1]

    recommendations = []
    for i in related_course_indices:
        recommendations.append(
            CourseRecommendation(
                title=courses_df['judul'].iloc[i],
                platform=courses_df['platform'].iloc[i],
                similarity_score=float(cosine_similarities[i]) # Pastikan tipe data float
            )
        )
    return recommendations

# --- Endpoint Root (Opsional) ---
@app.get("/")
async def read_root():
    return {"message": "Selamat datang di API Rekomendasi Kursus. Gunakan endpoint /recommend/ untuk mendapatkan rekomendasi."}