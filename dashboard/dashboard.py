import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

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

st.subheader("Data Bike Sharing")
st.dataframe(filtered_df)
