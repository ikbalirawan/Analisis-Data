import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

DATA_PATH = "dashboard/main_data.csv"

def load_data():
    df = pd.read_csv(DATA_PATH)
    df['dteday'] = pd.to_datetime(df['dteday'])
    return df

df = load_data()

st.sidebar.header("Filter Data")
date_range = st.sidebar.date_input("Pilih Rentang Tanggal", [df['dteday'].min(), df['dteday'].max()])
filtered_df = df[(df['dteday'] >= pd.to_datetime(date_range[0])) & (df['dteday'] <= pd.to_datetime(date_range[1]))]

st.title("Dashboard Bike Sharing")
st.write("Menampilkan analisis data bike sharing berdasarkan dataset harian dan per jam.")

st.subheader("Ringkasan Data")
st.write(f"Total Penggunaan Sepeda: {filtered_df['total_rentals_hour'].sum()}")

st.subheader("Tren Penggunaan Sepeda")
fig, ax = plt.subplots()
ax.plot(filtered_df['dteday'], filtered_df['total_rentals_hour'], marker='o', linestyle='-')
ax.set_xlabel("Tanggal")
ax.set_ylabel("Total Penyewaan")
ax.set_title("Tren Penyewaan Sepeda")
st.pyplot(fig)

st.subheader("Pengaruh Cuaca terhadap Jumlah Peminjaman Sepeda")
fig, ax = plt.subplots()
sns.scatterplot(x=filtered_df['temp_hour'], y=filtered_df['total_rentals_hour'], ax=ax)
ax.set_xlabel("Temperature per Jam")
ax.set_ylabel("Total Peminjaman")
ax.set_title("Hubungan antara Suhu dan Jumlah Peminjaman Sepeda")
st.pyplot(fig)

st.subheader("Jam Tersibuk dalam Sehari")
hourly_trend = df.groupby('hr')['total_rentals_hour'].mean()
fig, ax = plt.subplots()
ax.plot(hourly_trend.index, hourly_trend.values, marker='o', linestyle='-')
ax.set_xlabel("Jam")
ax.set_ylabel("Rata-rata Peminjaman")
ax.set_title("Jam Tersibuk dalam Sehari")
st.pyplot(fig)

st.subheader("Data Bike Sharing")
st.dataframe(filtered_df)