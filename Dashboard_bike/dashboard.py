import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import streamlit as st
import numpy as np
import os
from datetime import datetime

sns.set(style='darkgrid')

# Menggunakan absolute path (untuk lokal development)
current_dir = os.path.dirname(os.path.abspath(__file__))
day_data_path = os.path.join(current_dir, "day.csv")
hour_data_path = os.path.join(current_dir, "hour.csv")

# Load datasets
day_df = pd.read_csv(day_data_path)
hour_df = pd.read_csv(hour_data_path)

# Data preprocessing untuk dataset day.csv
day_df.rename(columns={
    'dteday': 'dateday',
    'yr': 'year',
    'mnth': 'month',
    'weathersit': 'weather',
    'cnt': 'count',
    'casual': 'casual_count',
    'registered': 'registered_count'
}, inplace=True)

# Mapping untuk bulan dan cuaca
day_df['month'] = day_df['month'].map({
    1: 'Jan', 2: 'Feb', 3: 'Mar', 4: 'Apr', 5: 'May', 6: 'Jun',
    7: 'Jul', 8: 'Aug', 9: 'Sep', 10: 'Oct', 11: 'Nov', 12: 'Dec'
})
day_df['season'] = day_df['season'].map({
    1: 'Spring', 2: 'Summer', 3: 'Fall', 4: 'Winter'
})
day_df['weather'] = day_df['weather'].map({
    1: 'Clear/Partly Cloudy',
    2: 'Misty/Cloudy',
    3: 'Light Snow/Rain',
    4: 'Severe Weather'
})

# Convert 'dateday' to datetime
day_df['dateday'] = pd.to_datetime(day_df['dateday'])
day_df['season'] = day_df['season'].astype('category')
day_df['year'] = day_df['year'].astype('category')
day_df['month'] = day_df['month'].astype('category')
day_df['weather'] = day_df['weather'].astype('category')

# Data preprocessing untuk dataset hour.csv
hour_df['dteday'] = pd.to_datetime(hour_df['dteday'])

# Filter by date range (sidebar)
st.sidebar.header("Filter Data")

# Mengganti rentang tanggal sesuai kebutuhan proyek
start_date = st.sidebar.date_input("Start Date", value=day_df['dateday'].min())
end_date = st.sidebar.date_input("End Date", value=day_df['dateday'].max())

# Filter berdasarkan range tanggal
filtered_day_df = day_df[(day_df['dateday'] >= pd.to_datetime(start_date)) & (day_df['dateday'] <= pd.to_datetime(end_date))]
filtered_hour_df = hour_df[(hour_df['dteday'] >= pd.to_datetime(start_date)) & (hour_df['dteday'] <= pd.to_datetime(end_date))]

# Dashboard Title
st.title("Bike Sharing Data Analysis Dashboard")

# Menampilkan statistik dasar
st.header("Basic Statistics")
st.write(filtered_day_df.describe())

# Pertanyaan 1: Kontribusi Penyewaan Sepeda pada Akhir Pekan
st.subheader("Contribution of Weekend Rentals to Monthly Rentals")
filtered_day_df['is_weekend'] = filtered_day_df['dateday'].dt.dayofweek >= 5
weekend_rentals = filtered_day_df.groupby(filtered_day_df['dateday'].dt.to_period('M'))['is_weekend'].sum().reset_index()
month_total = filtered_day_df.groupby(filtered_day_df['dateday'].dt.to_period('M'))['count'].sum().reset_index()
weekend_rentals['total_rentals'] = month_total['count']
weekend_rentals['percentage'] = (weekend_rentals['is_weekend'] / weekend_rentals['total_rentals']) * 100

fig, ax = plt.subplots(figsize=(10, 6))
sns.barplot(x=weekend_rentals['dateday'].dt.strftime('%Y-%m'), y=weekend_rentals['percentage'], ax=ax, palette='coolwarm')
ax.set_title('Percentage of Weekend Rentals to Total Monthly Rentals')
ax.set_xlabel('Month-Year')
ax.set_ylabel('Weekend Rentals Percentage (%)')
ax.tick_params(axis='x', rotation=45)
st.pyplot(fig)

# Pertanyaan 2: Pengaruh Cuaca Ekstrem
st.subheader("Effect of Extreme Weather on Daily Rentals")
extreme_weather_df = hour_df[hour_df['weathersit'].isin([3, 4])]  # 3: Light Snow/Rain, 4: Severe Weather
normal_weather_df = hour_df[~hour_df['weathersit'].isin([3, 4])]

extreme_weather_rentals = extreme_weather_df.groupby(extreme_weather_df['dteday'].dt.date)['cnt'].sum().reset_index()
normal_weather_rentals = normal_weather_df.groupby(normal_weather_df['dteday'].dt.date)['cnt'].sum().reset_index()

fig, ax = plt.subplots(figsize=(10, 6))
ax.plot(extreme_weather_rentals['dteday'], extreme_weather_rentals['cnt'], label='Extreme Weather', color='red')
ax.plot(normal_weather_rentals['dteday'], normal_weather_rentals['cnt'], label='Normal Weather', color='blue')
ax.set_title('Daily Rentals: Extreme Weather vs Normal Weather')
ax.set_xlabel('Date')
ax.set_ylabel('Total Rentals')
ax.legend()
st.pyplot(fig)

# Pertanyaan 3: Tren Bulanan Casual vs Registered User
st.subheader("Monthly Trends: Casual Users vs Registered Users")
monthly_user_data = hour_df.groupby([hour_df['dteday'].dt.to_period('M')])[['casual', 'registered']].sum().reset_index()
monthly_user_data['month'] = monthly_user_data['dteday'].dt.strftime('%Y-%m')

fig, ax = plt.subplots(figsize=(10, 6))
monthly_user_data.plot(x='month', kind='bar', stacked=True, ax=ax, color=['skyblue', 'orange'])
ax.set_title('Monthly Rentals: Casual vs Registered Users')
ax.set_xlabel('Month-Year')
ax.set_ylabel('Total Rentals')
ax.tick_params(axis='x', rotation=45)
st.pyplot(fig)

# RFM Analysis
latest_date = day_df['dateday'].max()
day_df['days_since_last_rental'] = (latest_date - day_df['dateday']).dt.days

rfm_df = day_df.groupby('dateday').agg({
    'days_since_last_rental': 'min',
    'count': ['sum', 'count']
}).reset_index()

rfm_df.columns = ['dateday', 'recency', 'monetary', 'frequency']

st.subheader("RFM Analysis: Recency vs Monetary vs Frequency")

fig, ax = plt.subplots(figsize=(10, 6))
scatter = ax.scatter(rfm_df['recency'], rfm_df['monetary'], c=rfm_df['frequency'], cmap='viridis', s=100, alpha=0.7)
plt.colorbar(scatter, ax=ax, label='Frequency')
ax.set_title('RFM Analysis: Recency vs Monetary vs Frequency')
ax.set_xlabel('Recency (Days Since Last Rental)')
ax.set_ylabel('Monetary (Total Rentals)')
st.pyplot(fig)

st.caption('By: Amalina Shabrina')
st.caption('Data sourced from bike sharing dataset')