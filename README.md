📊 Dashboard Analisis Penyewaan Sepeda

Dashboard ini dibuat menggunakan Streamlit untuk menganalisis data penyewaan sepeda berdasarkan berbagai faktor seperti musim, cuaca, dan tren harian.

📂 Struktur Proyek

dashboard/ → Folder yang berisi file dashboard utama.

dashboard.py → Script utama untuk Streamlit.

day.csv → Dataset penyewaan sepeda harian.

data/ → Folder yang menyimpan dataset tambahan.

notebook/ → Berisi analisis eksploratif dengan Jupyter Notebook.

requirements.txt → Daftar dependensi yang diperlukan untuk menjalankan proyek ini.

🚀 Cara Menjalankan

Pastikan Python telah terinstal (versi 3.8 atau lebih baru disarankan).

Install dependensi dengan perintah:

pip install -r requirements.txt

Jalankan dashboard Streamlit

streamlit run dashboard/dashboard.py

🛠 Fitur yang Tersedia

Preview Dataset → Menampilkan sampel data mentah setelah filter diterapkan.

Distribusi Penyewaan Sepeda → Analisis jumlah penyewaan berdasarkan musim.

Tren Penyewaan Sepeda → Visualisasi tren penggunaan sepeda sepanjang tahun.

Barplot Musiman → Total penyewaan sepeda berdasarkan musim.

RFM Analysis → Analisis Recency, Frequency, dan Monetary untuk pengguna.

Analisis Cuaca → Pengaruh suhu dan kondisi cuaca terhadap penyewaan sepeda.

📌 Catatan Penting

Pastikan dataset day.csv tersedia dalam folder dashboard/.

Jika terjadi error pada jalur file, gunakan path absolut sesuai direktori proyek Anda.