import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import streamlit as st
import numpy as np
import os
from datetime import datetime

# Mengatur tampilan seaborn untuk visualisasi yang lebih baik
sns.set(style='darkgrid')

# Menentukan path file menggunakan absolute path (untuk lingkungan lokal)
lokasi_sekarang = os.path.dirname(os.path.abspath(__file__))
day_data_file = os.path.join(lokasi_sekarang, "day.csv")
hour_data_file = os.path.join(lokasi_sekarang, "hour.csv")

# Memuat dataset
data_harian = pd.read_csv(day_data_file)
data_jam = pd.read_csv(hour_data_file)

# Preprocessing dataset day.csv
data_harian.rename(columns={
    'dteday': 'tanggal',
    'yr': 'tahun',
    'mnth': 'bulan',
    'weathersit': 'cuaca',
    'cnt': 'jumlah_total',
    'casual': 'jumlah_casual',
    'registered': 'jumlah_terdaftar'
}, inplace=True)

# Mapping nama bulan dan kondisi cuaca
data_harian['bulan'] = data_harian['bulan'].map({
    1: 'Jan', 2: 'Feb', 3: 'Mar', 4: 'Apr', 5: 'Mei', 6: 'Jun',
    7: 'Jul', 8: 'Agu', 9: 'Sep', 10: 'Okt', 11: 'Nov', 12: 'Des'
})
data_harian['season'] = data_harian['season'].map({
    1: 'Semi', 2: 'Panas', 3: 'Gugur', 4: 'Dingin'
})
data_harian['cuaca'] = data_harian['cuaca'].map({
    1: 'Cerah/Agak Berawan',
    2: 'Berkabut/Berawan',
    3: 'Salju/Hujan Ringan',
    4: 'Cuaca Ekstrem'
})

# Konversi kolom tanggal ke tipe datetime
data_harian['tanggal'] = pd.to_datetime(data_harian['tanggal'])
data_harian['season'] = data_harian['season'].astype('category')
data_harian['tahun'] = data_harian['tahun'].astype('category')
data_harian['bulan'] = data_harian['bulan'].astype('category')
data_harian['cuaca'] = data_harian['cuaca'].astype('category')

# Preprocessing untuk dataset hour.csv
data_jam['dteday'] = pd.to_datetime(data_jam['dteday'])

# Filter data berdasarkan rentang tanggal melalui sidebar
st.sidebar.header("Filter Data")

# Mengganti rentang tanggal sesuai kebutuhan proyek
tanggal_mulai = st.sidebar.date_input("Tanggal Mulai", value=data_harian['tanggal'].min())
tanggal_selesai = st.sidebar.date_input("Tanggal Selesai", value=data_harian['tanggal'].max())

# Filter berdasarkan tanggal
data_harian_terfilter = data_harian[(data_harian['tanggal'] >= pd.to_datetime(tanggal_mulai)) & (data_harian['tanggal'] <= pd.to_datetime(tanggal_selesai))]
data_jam_terfilter = data_jam[(data_jam['dteday'] >= pd.to_datetime(tanggal_mulai)) & (data_jam['dteday'] <= pd.to_datetime(tanggal_selesai))]

# Judul Dashboard
st.title("Dashboard Analisis Data Bike Sharing")

# Menampilkan statistik dasar
st.header("Statistik Dasar")
st.write(data_harian_terfilter.describe())

# Pertanyaan 1: Kontribusi Penyewaan Sepeda di Akhir Pekan
st.subheader("Kontribusi Penyewaan Sepeda pada Akhir Pekan terhadap Total Penyewaan Bulanan")
data_harian_terfilter['akhir_pekan'] = data_harian_terfilter['tanggal'].dt.dayofweek >= 5
penyewaan_akhir_pekan = data_harian_terfilter.groupby(data_harian_terfilter['tanggal'].dt.to_period('M'))['akhir_pekan'].sum().reset_index()
penyewaan_bulanan = data_harian_terfilter.groupby(data_harian_terfilter['tanggal'].dt.to_period('M'))['jumlah_total'].sum().reset_index()
penyewaan_akhir_pekan['total_penyewaan'] = penyewaan_bulanan['jumlah_total']
penyewaan_akhir_pekan['persentase'] = (penyewaan_akhir_pekan['akhir_pekan'] / penyewaan_akhir_pekan['total_penyewaan']) * 100

# Visualisasi bar plot
fig, ax = plt.subplots(figsize=(10, 6))
sns.barplot(x=penyewaan_akhir_pekan['tanggal'].dt.strftime('%Y-%m'), y=penyewaan_akhir_pekan['persentase'], ax=ax, palette='coolwarm')
ax.set_title('Persentase Penyewaan Akhir Pekan terhadap Penyewaan Bulanan')
ax.set_xlabel('Bulan-Tahun')
ax.set_ylabel('Persentase Penyewaan Akhir Pekan (%)')
ax.tick_params(axis='x', rotation=45)
st.pyplot(fig)

# Pertanyaan 2: Pengaruh Cuaca Ekstrem
st.subheader("Pengaruh Cuaca Ekstrem terhadap Penyewaan Harian")
cuaca_ekstrem_df = data_jam[data_jam['weathersit'].isin([3, 4])]  # 3: Salju/Hujan Ringan, 4: Cuaca Ekstrem
cuaca_normal_df = data_jam[~data_jam['weathersit'].isin([3, 4])]

penyewaan_cuaca_ekstrem = cuaca_ekstrem_df.groupby(cuaca_ekstrem_df['dteday'].dt.date)['cnt'].sum().reset_index()
penyewaan_cuaca_normal = cuaca_normal_df.groupby(cuaca_normal_df['dteday'].dt.date)['cnt'].sum().reset_index()

# Visualisasi cuaca ekstrem vs normal
fig, ax = plt.subplots(figsize=(10, 6))
ax.plot(penyewaan_cuaca_ekstrem['dteday'], penyewaan_cuaca_ekstrem['cnt'], label='Cuaca Ekstrem', color='red')
ax.plot(penyewaan_cuaca_normal['dteday'], penyewaan_cuaca_normal['cnt'], label='Cuaca Normal', color='blue')
ax.set_title('Penyewaan Harian: Cuaca Ekstrem vs Cuaca Normal')
ax.set_xlabel('Tanggal')
ax.set_ylabel('Total Penyewaan')
ax.legend()
st.pyplot(fig)

# Pertanyaan 3: Tren Bulanan Pengguna Casual vs Terdaftar
st.subheader("Tren Bulanan: Pengguna Casual vs Pengguna Terdaftar")
data_pengguna_bulanan = data_jam.groupby([data_jam['dteday'].dt.to_period('M')])[['casual', 'registered']].sum().reset_index()
data_pengguna_bulanan['bulan'] = data_pengguna_bulanan['dteday'].dt.strftime('%Y-%m')

# Visualisasi bar plot untuk pengguna casual dan terdaftar
fig, ax = plt.subplots(figsize=(10, 6))
data_pengguna_bulanan.plot(x='bulan', kind='bar', stacked=True, ax=ax, color=['skyblue', 'orange'])
ax.set_title('Penyewaan Bulanan: Pengguna Casual vs Terdaftar')
ax.set_xlabel('Bulan-Tahun')
ax.set_ylabel('Total Penyewaan')
ax.tick_params(axis='x', rotation=45)
st.pyplot(fig)

# Analisis RFM
tanggal_terbaru = data_harian['tanggal'].max()
data_harian['hari_sejak_terakhir_penyewaan'] = (tanggal_terbaru - data_harian['tanggal']).dt.days

# Menggabungkan hasil RFM
rfm_data = data_harian.groupby('tanggal').agg({
    'hari_sejak_terakhir_penyewaan': 'min',
    'jumlah_total': ['sum', 'count']
}).reset_index()

rfm_data.columns = ['tanggal', 'recency', 'monetary', 'frequency']

# Visualisasi RFM Analysis
st.subheader("Analisis RFM: Recency vs Monetary vs Frequency")

fig, ax = plt.subplots(figsize=(10, 6))
scatter = ax.scatter(rfm_data['recency'], rfm_data['monetary'], c=rfm_data['frequency'], cmap='viridis', s=100, alpha=0.7)
plt.colorbar(scatter, ax=ax, label='Frequency')
ax.set_title('Analisis RFM: Recency vs Monetary vs Frequency')
ax.set_xlabel('Recency (Hari Sejak Penyewaan Terakhir)')
ax.set_ylabel('Monetary (Total Penyewaan)')
st.pyplot(fig)

st.caption('By: Amalina Shabrina')
st.caption('Data sourced from bike sharing dataset')