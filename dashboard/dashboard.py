import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np

# --- Muat Data ---
data_path = "dashboard/day.csv"
try:
    df = pd.read_csv(data_path, on_bad_lines='skip', engine='python')
except FileNotFoundError:
    st.error(f"Data tidak ditemukan di {data_path}. Silakan periksa lokasi file.")
    st.stop()

# --- Persiapan Data ---
df['dteday'] = pd.to_datetime(df['dteday'])

# Tambahkan label musim dan cuaca
df['musim'] = df['season'].map({1: "Semi", 2: "Panas", 3: "Gugur", 4: "Dingin"})
df['cuaca'] = df['weathersit'].map({1: "Cerah", 2: "Berawan", 3: "Hujan/Salju"})

# --- Navigasi Sidebar ---
st.sidebar.title("📈 Menu Visualisasi")
menu = st.sidebar.selectbox("Pilih Jenis Visualisasi", [
    "Lihat Data", "Distribusi Musiman", "Tren Harian", 
    "Total per Musim", "Pengaruh Cuaca", "Hari Kerja vs Akhir Pekan"
])

# --- Filter Tanggal ---
st.sidebar.subheader("🗓️ Filter Tanggal")
awal = st.sidebar.date_input("Mulai", df['dteday'].min())
akhir = st.sidebar.date_input("Akhir", df['dteday'].max())
df_filtered = df[(df['dteday'] >= pd.Timestamp(awal)) & (df['dteday'] <= pd.Timestamp(akhir))]

# --- Tampilkan Data ---
if menu == "Lihat Data":
    st.title("📄 Data Penyewaan Sepeda")
    st.dataframe(df_filtered.head())

# --- Visualisasi Distribusi Rata-rata per Musim ---
elif menu == "Distribusi Musiman":
    st.title("📊 Rata-rata Penyewaan per Musim")
    fig, ax = plt.subplots(figsize=(8, 6))
    sns.barplot(x="musim", y="cnt", data=df_filtered, estimator=np.mean, palette="viridis", ax=ax)
    ax.set_xlabel("Musim")
    ax.set_ylabel("Rata-rata Jumlah Penyewaan")
    ax.grid(True, linestyle="--", alpha=0.6)
    st.pyplot(fig)

# --- Tren Waktu ---
elif menu == "Tren Harian":
    st.title("📆 Tren Penyewaan Sepeda")
    fig, ax = plt.subplots(figsize=(12, 6))
    sns.lineplot(x=df_filtered['dteday'], y=df_filtered['cnt'], color="teal", ax=ax)
    ax.set_xlabel("Tanggal")
    ax.set_ylabel("Jumlah Penyewaan")
    ax.set_title("Tren Harian Penyewaan Sepeda")
    ax.grid(True, linestyle="--", alpha=0.5)
    plt.xticks(rotation=45)
    st.pyplot(fig)

# --- Total Penyewaan Berdasarkan Musim ---
elif menu == "Total per Musim":
    st.title("📊 Total Penyewaan per Musim")
    fig, ax = plt.subplots(figsize=(8, 6))
    sns.barplot(x="musim", y="cnt", data=df_filtered, estimator=np.sum, palette="magma", ax=ax)
    ax.set_xlabel("Musim")
    ax.set_ylabel("Total Penyewaan")
    ax.grid(True, linestyle="--", alpha=0.6)
    st.pyplot(fig)

# --- Analisis Berdasarkan Cuaca ---
elif menu == "Pengaruh Cuaca":
    st.title("🌦️ Penyewaan Berdasarkan Kondisi Cuaca")

    # Scatter plot suhu vs penyewaan
    fig, ax = plt.subplots(figsize=(8, 6))
    sns.scatterplot(x=df_filtered['temp'], y=df_filtered['cnt'], hue=df_filtered['cuaca'], palette="coolwarm", alpha=0.6, ax=ax)
    ax.set_xlabel("Temperatur (Skala Normal)")
    ax.set_ylabel("Jumlah Penyewaan")
    ax.grid(True, linestyle="--", alpha=0.5)
    st.pyplot(fig)

    # Rata-rata penyewaan per kondisi cuaca
    fig, ax = plt.subplots(figsize=(8, 6))
    sns.barplot(x='cuaca', y='cnt', data=df_filtered, estimator=np.mean, palette="rocket", ax=ax)
    ax.set_xlabel("Cuaca")
    ax.set_ylabel("Rata-rata Penyewaan")
    ax.grid(True, linestyle="--", alpha=0.6)
    st.pyplot(fig)

# --- Hari Kerja vs Akhir Pekan ---
elif menu == "Hari Kerja vs Akhir Pekan":
    st.title("🧑‍💼 Hari Kerja vs 🛌 Akhir Pekan")

    df_temp = df_filtered.copy()
    df_temp['Jenis Hari'] = df_temp['workingday'].map({0: "Akhir Pekan", 1: "Hari Kerja"})

    fig, ax = plt.subplots(figsize=(8, 6))
    sns.barplot(x='Jenis Hari', y='cnt', data=df_temp, estimator=np.mean, palette="coolwarm", ax=ax)
    ax.set_xlabel("Jenis Hari")
    ax.set_ylabel("Rata-rata Penyewaan")
    ax.set_title("Perbandingan Penyewaan antara Hari Kerja dan Akhir Pekan")
    ax.grid(True, linestyle="--", alpha=0.5)
    st.pyplot(fig)

st.sidebar.info("Silakan pilih menu visualisasi untuk melihat hasil analisis.")
