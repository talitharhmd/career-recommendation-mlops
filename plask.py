from flask import Flask, request, jsonify
import pandas as pd
from sklearn.metrics.pairwise import cosine_similarity
import pickle
import os # Untuk memeriksa keberadaan file

# Inisialisasi aplikasi Flask
app = Flask(__name__)

# --- Memuat Model dan Data yang Telah Disimpan ---
# Path ke file-file model dan data
TFIDF_VECTORIZER_PATH = 'tfidf_vectorizer.pkl'
TFIDF_MATRIX_PATH = 'item_similarity_matrix.pkl'
COURSES_DF_PATH = "courses_classentral.csv"

# Variabel global untuk menyimpan model dan data yang dimuat
tfidf_vectorizer = None
tfidf_matrix = None
courses_df = pd.read_csv(COURSES_DF_PATH)

def load_models_and_data():
    """
    Fungsi untuk memuat model dan data saat aplikasi dimulai.
    """
    global tfidf_vectorizer, tfidf_matrix, courses_df
    
    print("Memuat model dan data...")
    try:
        if not os.path.exists(TFIDF_VECTORIZER_PATH):
            raise FileNotFoundError(f"File {TFIDF_VECTORIZER_PATH} tidak ditemukan. Pastikan Anda sudah menjalankan script persiapan.")
        if not os.path.exists(TFIDF_MATRIX_PATH):
            raise FileNotFoundError(f"File {TFIDF_MATRIX_PATH} tidak ditemukan. Pastikan Anda sudah menjalankan script persiapan.")

        with open(TFIDF_VECTORIZER_PATH, 'rb') as f:
            tfidf_vectorizer = pickle.load(f)
        
        with open(TFIDF_MATRIX_PATH, 'rb') as f:
            tfidf_matrix = pickle.load(f)
        
        print("Model dan data berhasil dimuat.")
    except FileNotFoundError as e:
        print(f"Error: {e}. Harap jalankan script persiapan model terlebih dahulu.")
        # Untuk Flask, kita bisa menangani ini dengan mengembalikan error saat request jika model belum siap
        # atau memastikan aplikasi tidak berjalan jika file penting tidak ada.
        # Untuk kesederhanaan, kita akan biarkan error terjadi saat request jika tidak dimuat.
        pass # Biarkan aplikasi tetap berjalan, error akan muncul saat request ke endpoint
    except Exception as e:
        print(f"Terjadi kesalahan saat memuat model atau data: {e}")
        pass # Biarkan aplikasi tetap berjalan, error akan muncul saat request ke endpoint

# Panggil fungsi pemuatan saat startup aplikasi
# Ini akan dijalankan sekali saat server Flask dimulai
load_models_and_data()


# --- Endpoint Utama untuk Rekomendasi ---
@app.route('/recommend', methods=['POST'])
def recommend_courses():
    """
    Merekomendasikan kursus berdasarkan kueri pekerjaan.
    Menerima input JSON: {"query": "nama_pekerjaan", "top_n": jumlah_rekomendasi}
    """
    if tfidf_vectorizer is None or tfidf_matrix is None or courses_df is None:
        return jsonify({"error": "Model atau data belum dimuat. Coba lagi nanti atau periksa log server."}), 503

    data = request.form.to_dict()
    if not data or 'query' not in data:
        return jsonify({"error": "Input JSON tidak valid. Diperlukan kunci 'query'."}), 400

    query = data['query']
    top_n = int(data.get('top_n', 3)) # Ambil top_n dari JSON, default 3
    print(data)
    print(query, top_n)

    # Vektorisasi kueri pekerjaan menggunakan vectorizer yang dimuat
    query_vector = tfidf_vectorizer.transform([query])

    # Hitung cosine similarity antara query_vector dan tfidf_matrix (matriks kursus)
    cosine_similarities = cosine_similarity(query_vector, tfidf_matrix).flatten()

    # Dapatkan indeks kursus dengan similaritas tertinggi
    related_course_indices = cosine_similarities.argsort()[:-top_n-1:-1]

    recommendations = []
    for i in related_course_indices:
        recommendations.append({
            "title": courses_df['Title'].iloc[i],
            "platform": courses_df['Provider'].iloc[i],
            "similarity_score": float(cosine_similarities[i]) # Pastikan tipe data float
        })
    
    return jsonify(recommendations)

# --- Endpoint Root (Opsional) ---
@app.route('/')
def index():
    return jsonify({"message": "Selamat datang di API Rekomendasi Kursus. Gunakan endpoint /recommend (POST) untuk mendapatkan rekomendasi."})

# Menjalankan aplikasi Flask
if __name__ == '__main__':
    # Untuk lingkungan produksi, gunakan Gunicorn atau sejenisnya.
    # Untuk pengembangan, cukup app.run()
    app.run(debug=True, host='0.0.0.0', port=5000)