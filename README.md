# Bike_Sharing_Dataset
# Nama Proyek : **Analisis Penyewaan Sepeda dengan Streamlit**

**Deskripsi Proyek**

Proyek ini bertujuan untuk menganalisis data penyewaan sepeda berbasis sistem berbagi sepeda (bike sharing) di sebuah kota. Dataset yang digunakan mencakup informasi penyewaan harian dan per jam dengan berbagai fitur terkait seperti cuaca, musim, hari dalam seminggu, jumlah pengguna terdaftar dan pengguna kasual, serta jumlah total penyewaan.

Tujuan utama dari analisis ini adalah untuk menemukan wawasan penting terkait pola penggunaan sepeda, pengaruh cuaca terhadap jumlah penyewaan, serta perbedaan tren penyewaan antara pengguna terdaftar dan pengguna kasual. Hasil analisis akan divisualisasikan dalam bentuk dashboard interaktif yang dibangun menggunakan Streamlit, serta mencakup beberapa filter data yang memudahkan eksplorasi lebih lanjut.

Proyek ini juga akan membantu dalam memahami kontribusi penyewaan di akhir pekan, pengaruh cuaca ekstrem terhadap penyewaan harian, serta memberikan gambaran tentang tren bulanan antara pengguna terdaftar dan pengguna kasual.

**Fitur Dashboard**
1. Statistik Dasar: Menampilkan ringkasan statistik dasar dari dataset penyewaan harian, seperti rata-rata, nilai minimum, maksimum, serta distribusi data.
2. Kontribusi Penyewaan Akhir Pekan: Visualisasi kontribusi penyewaan sepeda selama akhir pekan dibandingkan dengan total penyewaan bulanan.
3. Pengaruh Cuaca Ekstrem: Grafik perbandingan penyewaan harian pada kondisi cuaca normal dan cuaca ekstrem seperti hujan deras atau salju.
4. Tren Pengguna Kasual vs Terdaftar: Visualisasi perbandingan jumlah penyewaan pengguna kasual dan terdaftar pada skala bulanan.
Analisis RFM (Recency, Frequency, Monetary): Analisis perilaku pengguna berdasarkan tiga indikator utama: seberapa sering pengguna menyewa (frekuensi), berapa lama sejak terakhir kali menyewa (recency), dan jumlah total penyewaan (monetary).

**Dataset**

Dataset yang digunakan berasal dari data bike sharing yang tersedia secara publik. Dataset terdiri dari dua file:
1. day.csv: Menyimpan data penyewaan sepeda secara harian.
2. hour.csv: Menyimpan data penyewaan sepeda secara per jam.

**Setiap file berisi informasi berikut:**
1. Tanggal (dteday): Tanggal dari penyewaan sepeda.
2. Musim (season): Menunjukkan musim pada hari tersebut (Spring, Summer, Fall, Winter).
3. Cuaca (weather): Kondisi cuaca pada hari tersebut (Clear/Partly Cloudy, Misty/Cloudy, Light Snow/Rain, Severe Weather).
4. Jumlah Penyewaan (cnt): Total penyewaan sepeda pada hari tersebut (atau per jam untuk dataset hour).
5. Pengguna Terdaftar (registered): Jumlah pengguna yang terdaftar menyewa sepeda.
6. Pengguna Kasual (casual): Jumlah penyewaan sepeda oleh pengguna kasual.

**Teknologi yang Digunakan**
- Python: Bahasa pemrograman utama untuk data preprocessing, analisis, dan visualisasi.
- Pandas: Digunakan untuk manipulasi dan analisis data.
- Matplotlib dan Seaborn: Untuk membuat visualisasi grafis.
- Streamlit: Framework untuk membuat dashboard interaktif berbasis web.
- Git: Untuk pengelolaan versi kode proyek.

**Instalasi**
1. Clone repositori:
   ```bash
   git clone https://github.com/AmalinaShabrina/Bike_Sharing_Dataset.git
   cd Bike_Sharing_Dataset

3. Instal dependensi: Pastikan Anda telah menginstal Python versi terbaru. Kemudian jalankan:
   ```bash
   pip install -r requirements.txt

5. Menjalankan dashboard: Untuk menjalankan dashboard Streamlit:
   ```bash
   streamlit run dashboard.py

**Penggunaan**

Setelah dashboard berjalan, Anda dapat menggunakan filter di sidebar untuk menyaring data berdasarkan rentang tanggal. Dashboard akan menampilkan berbagai visualisasi yang interaktif untuk mengeksplorasi data bike sharing lebih dalam.

**Kontribusi**

Kontribusi pada proyek ini sangat diterima. Anda dapat melakukan fork, membuat branch baru, dan mengajukan pull request untuk peninjauan.

**Lisensi**

Proyek ini dilisensikan di bawah lisensi MIT. Silakan lihat file LICENSE untuk informasi lebih lanjut.

**Author**

Amalina Shabrina - [amalinashabrina2504@students.unnes.ac.id](mailto:amalinashabrina2504@students.unnes.ac.id)

