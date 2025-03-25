import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# --- Memuat Dataset ---
file_path = "dashboard/day.csv"
data = pd.read_csv(file_path)

# --- Praproses Data ---
data['dteday'] = pd.to_datetime(data['dteday'])

# --- Sidebar Navigasi ---
st.sidebar.title("📊 Pilihan Analisis Data")
menu = st.sidebar.selectbox("Pilih Analisis:", [
    "Tampilan Awal Data", "Distribusi Penyewaan", "Tren Penyewaan", 
    "Analisis Musiman", "Analisis RFM", "Pengaruh Cuaca"])

# --- Filter Interaktif ---
st.sidebar.subheader("📅 Rentang Waktu")
start = st.sidebar.date_input("Dari Tanggal", data['dteday'].min())
end = st.sidebar.date_input("Hingga Tanggal", data['dteday'].max())

st.sidebar.subheader("🎯 Kriteria Tambahan")
# Filter musim
seasons = {1: "Spring", 2: "Summer", 3: "Fall", 4: "Winter"}
pilih_musim = st.sidebar.selectbox("Musim", ["Semua"] + list(seasons.values()))

# Filter jumlah penyewaan minimum
min_peminjam = st.sidebar.slider("Batas Minimum Penyewaan", 0, int(data["cnt"].max()), 0)

# Filter dataset berdasarkan input
filtered_data = data[
    (data['dteday'] >= pd.Timestamp(start)) & 
    (data['dteday'] <= pd.Timestamp(end)) & 
    (data['cnt'] >= min_peminjam)]

if pilih_musim != "Semua":
    season_num = list(seasons.keys())[list(seasons.values()).index(pilih_musim)]
    filtered_data = filtered_data[filtered_data['season'] == season_num]

# Opsi untuk menampilkan data mentah
if st.sidebar.checkbox("Lihat Data Mentah", False):
    st.subheader("📋 Data Setelah Difilter")
    st.dataframe(filtered_data.head())

# --- Tampilan Dataset ---
if menu == "Tampilan Awal Data":
    st.title("📂 Dataset Penyewaan Sepeda")
    st.dataframe(filtered_data.head())

# --- Distribusi Penyewaan Sepeda ---
elif menu == "Distribusi Penyewaan":
    st.title("📊 Distribusi Penyewaan Sepeda")
    fig, ax = plt.subplots(figsize=(8, 6))
    sns.histplot(filtered_data['cnt'], bins=30, kde=True, ax=ax, color='blue')
    ax.set_xlabel("Jumlah Penyewaan")
    ax.set_ylabel("Frekuensi")
    st.pyplot(fig)

# --- Tren Penyewaan Sepeda ---
elif menu == "Tren Penyewaan":
    st.title("📈 Tren Penyewaan Sepeda")
    fig, ax = plt.subplots(figsize=(12, 6))
    sns.lineplot(x=filtered_data['dteday'], y=filtered_data['cnt'], ax=ax, marker="o")
    ax.set_xlabel("Tanggal")
    ax.set_ylabel("Jumlah Penyewaan")
    plt.xticks(rotation=45)
    st.pyplot(fig)

# --- Analisis Musiman ---
elif menu == "Analisis Musiman":
    st.title("📊 Penyewaan Sepeda Berdasarkan Musim")
    fig, ax = plt.subplots(figsize=(8, 6))
    sns.barplot(x=filtered_data['season'], y=filtered_data['cnt'], estimator=sum, ax=ax, palette="coolwarm")
    ax.set_xlabel("Musim")
    ax.set_ylabel("Total Penyewaan")
    st.pyplot(fig)

# --- Analisis RFM ---
elif menu == "Analisis RFM":
    st.title("📊 Analisis RFM Pengguna Sepeda")
    filtered_data['user_id'] = filtered_data.index % 1000
    rfm = filtered_data.groupby('user_id').agg(
        Recency=('dteday', lambda x: (filtered_data['dteday'].max() - x.max()).days),
        Frequency=('user_id', 'count'),
        Monetary=('cnt', 'sum')
    ).reset_index()
    
    st.subheader("Tabel Analisis RFM")
    st.dataframe(rfm.head(10))
    
    fig, ax = plt.subplots(figsize=(10, 5))
    sns.scatterplot(x=rfm['Recency'], y=rfm['Monetary'], hue=rfm['Frequency'], palette='coolwarm', ax=ax)
    ax.set_xlabel("Recency (Hari sejak transaksi terakhir)")
    ax.set_ylabel("Total Penyewaan")
    st.pyplot(fig)

# --- Pengaruh Cuaca terhadap Penyewaan ---
elif menu == "Pengaruh Cuaca":
    st.title("☀️ Hubungan Cuaca dan Penyewaan Sepeda")
    fig, ax = plt.subplots(figsize=(8, 6))
    sns.scatterplot(x=filtered_data['temp'], y=filtered_data['cnt'], alpha=0.6, ax=ax)
    ax.set_xlabel("Temperatur")
    ax.set_ylabel("Jumlah Penyewaan")
    st.pyplot(fig)
    
    fig, ax = plt.subplots(figsize=(8, 6))
    sns.barplot(x=filtered_data['weathersit'], y=filtered_data['cnt'], estimator=sum, ax=ax, palette="coolwarm")
    ax.set_xlabel("Kondisi Cuaca")
    ax.set_ylabel("Total Penyewaan")
    st.pyplot(fig)

st.sidebar.info("Gunakan menu di samping untuk memilih jenis analisis yang ingin ditampilkan.")