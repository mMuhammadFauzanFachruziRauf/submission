# file: dashboard_bike_sharing.py

import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np

# --- Load Dataset ---
file_path = "dashboard/day.csv"
try:
    day_df = pd.read_csv(file_path, on_bad_lines='skip', engine='python')
except FileNotFoundError:
    st.error(f"File {file_path} tidak ditemukan. Pastikan file tersedia di folder Dashboard.")
    st.stop()

# --- Preprocessing ---
day_df['dteday'] = pd.to_datetime(day_df['dteday'])

season_mapping = {1: "Spring", 2: "Summer", 3: "Fall", 4: "Winter"}
day_df['season_label'] = day_df['season'].map(season_mapping)

weather_mapping = {1: "Clear", 2: "Cloudy", 3: "Rain/Snow"}
day_df['weather_label'] = day_df['weathersit'].map(weather_mapping)

# --- Sidebar Navigation ---
st.sidebar.title("📊 Menu Analisis Data")
option = st.sidebar.selectbox("Pilih Analisis", [
    "Preview Dataset", "Distribusi Penyewaan Sepeda", "Tren Penyewaan Sepeda",
    "Barplot Musiman", "Analisis Cuaca", "Pola Hari Kerja vs Akhir Pekan", 
    "Pertanyaan, Insight, Kesimpulan"
])

# --- Filter Tanggal ---
st.sidebar.subheader("📅 Filter Rentang Tanggal")
start_date = st.sidebar.date_input("Tanggal Mulai", day_df['dteday'].min())
end_date = st.sidebar.date_input("Tanggal Akhir", day_df['dteday'].max())

filtered_df = day_df[
    (day_df['dteday'] >= pd.Timestamp(start_date)) & 
    (day_df['dteday'] <= pd.Timestamp(end_date))
]

# --- Preview Dataset ---
if option == "Preview Dataset":
    st.title("📂 Dataset Bike Sharing")
    st.dataframe(filtered_df.head())

# --- Distribusi Penyewaan Sepeda ---
elif option == "Distribusi Penyewaan Sepeda":
    st.title("📊 Distribusi Penyewaan Sepeda Berdasarkan Musim")
    fig, ax = plt.subplots(figsize=(8, 6))
    sns.barplot(x="season_label", y="cnt", data=filtered_df, estimator=np.mean, palette="viridis", ax=ax)
    ax.set_xlabel("Musim")
    ax.set_ylabel("Rata-rata Penyewaan Sepeda")
    ax.grid(True, linestyle="--", alpha=0.7)
    st.pyplot(fig)

# --- Tren Sepanjang Tahun ---
elif option == "Tren Penyewaan Sepeda":
    st.title("📈 Tren Penyewaan Sepeda Sepanjang Tahun")
    fig, ax = plt.subplots(figsize=(12, 6))
    sns.lineplot(x=filtered_df['dteday'], y=filtered_df['cnt'], color="blue", marker="o", ax=ax)
    ax.set_xlabel("Tanggal")
    ax.set_ylabel("Jumlah Penyewaan Sepeda")
    ax.set_title("Tren Penyewaan Sepeda Sepanjang Tahun")
    plt.xticks(rotation=45)
    ax.grid(True, linestyle="--", alpha=0.7)
    st.pyplot(fig)

# --- Barplot Musiman ---
elif option == "Barplot Musiman":
    st.title("📊 Total Penyewaan Sepeda Berdasarkan Musim")
    fig, ax = plt.subplots(figsize=(8, 6))
    sns.barplot(x="season_label", y="cnt", data=filtered_df, estimator=np.sum, palette="magma", ax=ax)
    ax.set_xlabel("Musim")
    ax.set_ylabel("Total Penyewaan Sepeda")
    ax.grid(True, linestyle="--", alpha=0.7)
    st.pyplot(fig)

# --- Analisis Cuaca ---
elif option == "Analisis Cuaca":
    st.title("☀️ Analisis Cuaca dan Penyewaan Sepeda")

    fig, ax = plt.subplots(figsize=(8, 6))
    sns.scatterplot(x=filtered_df['temp'], y=filtered_df['cnt'], hue=filtered_df['weather_label'], palette="coolwarm", alpha=0.6, ax=ax)
    ax.set_xlabel("Temperatur (Normalisasi)")
    ax.set_ylabel("Jumlah Penyewaan Sepeda")
    ax.grid(True, linestyle="--", alpha=0.7)
    st.pyplot(fig)

    fig, ax = plt.subplots(figsize=(8, 6))
    sns.barplot(x=filtered_df['weather_label'], y=filtered_df['cnt'], estimator=np.mean, palette="rocket", ax=ax)
    ax.set_xlabel("Kondisi Cuaca")
    ax.set_ylabel("Rata-rata Penyewaan Sepeda")
    ax.grid(True, linestyle="--", alpha=0.7)
    st.pyplot(fig)

# --- Hari Kerja vs Akhir Pekan ---
elif option == "Pola Hari Kerja vs Akhir Pekan":
    st.title("📅 Pola Penyewaan Sepeda: Hari Kerja vs Akhir Pekan")

    df_copy = filtered_df.copy()
    df_copy["Kategori Hari"] = df_copy["workingday"].map({0: "Akhir Pekan", 1: "Hari Kerja"})

    fig, ax = plt.subplots(figsize=(8, 6))
    sns.barplot(x="Kategori Hari", y="cnt", data=df_copy, estimator=np.mean, palette="coolwarm", ax=ax)
    ax.set_xlabel("Kategori Hari")
    ax.set_ylabel("Rata-rata Penyewaan Sepeda")
    ax.set_title("Perbandingan Penyewaan Sepeda pada Hari Kerja vs. Akhir Pekan")
    ax.grid(True, linestyle="--", alpha=0.7)
    st.pyplot(fig)

# --- Insight dan Kesimpulan ---
elif option == "Pertanyaan, Insight, Kesimpulan":
    st.title("🧠 Insight, Kesimpulan, dan Rekomendasi")

    st.subheader("📌 Pertanyaan Eksplorasi")
    st.markdown("**Bagaimana distribusi penyewaan sepeda pada setiap musim?**")

    st.subheader("🔍 Temuan / Insight")
    st.markdown("""
    - Musim **gugur (Fall)** menunjukkan jumlah rata-rata dan total penyewaan sepeda **tertinggi**.
    - Musim **semi (Spring)** memiliki penyewaan **terendah** dibanding musim lain.
    - Pengaruh musim terhadap penyewaan sangat signifikan — musim dengan suhu nyaman mendorong lebih banyak aktivitas luar ruangan.
    """)

    st.subheader("✅ Kesimpulan")
    st.markdown("""
    - **Fall (Musim Gugur)** adalah musim dengan permintaan tertinggi terhadap layanan penyewaan sepeda.
    - **Spring (Musim Semi)** menjadi musim dengan tingkat penyewaan terendah, kemungkinan karena suhu yang belum stabil.
    - Strategi bisnis harus mempertimbangkan fluktuasi ini untuk efisiensi dan peningkatan layanan.
    """)

    st.subheader("💡 Rekomendasi")
    st.markdown("""
    1. **Tingkatkan stok sepeda dan tenaga operasional pada musim Fall dan Summer**.
    2. **Adakan promosi khusus saat Spring**, seperti diskon penyewaan atau kampanye komunitas.
    3. **Gunakan data historis cuaca dan musim** untuk merencanakan logistik dan operasional lebih baik.
    4. **Evaluasi lokasi-lokasi strategis penyewaan** berdasarkan pola musim untuk optimalisasi penempatan sepeda.
    """)

st.sidebar.info("Pilih menu di atas untuk melihat analisis data yang sesuai.")
