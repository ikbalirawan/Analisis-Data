import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from babel.numbers import format_currency

sns.set(style='dark')

data = pd.read_csv('dashboard/main_data.csv')

if 'Survived' not in data.columns:
    st.warning("Kolom 'Survived' tidak ditemukan di main_data.csv.")

st.title('Dashboard Analisis Data Titanic')

st.write('Data Penumpang Titanic:')
st.write(data)

def create_survival_rate_df(df):
    if 'Survived' in df.columns:
        survival_rate_df = df['Survived'].value_counts().reset_index()
        survival_rate_df.columns = ['Survived', 'Count']
        return survival_rate_df
    else:
        return pd.DataFrame(columns=['Survived', 'Count'])

def create_age_distribution_df(df):
    return df['Age'].dropna()

def create_class_survival_df(df):
    if 'Survived' in df.columns:
        class_survival_df = df.groupby(['Pclass', 'Survived']).size().reset_index(name='Count')
        return class_survival_df
    else:
        return pd.DataFrame(columns=['Pclass', 'Survived', 'Count'])

survival_rate_df = create_survival_rate_df(data)
age_distribution_df = create_age_distribution_df(data)
class_survival_df = create_class_survival_df(data)

if not survival_rate_df.empty:
    st.write('### Jumlah Penumpang yang Selamat')
    fig1, ax1 = plt.subplots(figsize=(8, 6))
    sns.barplot(x='Survived', y='Count', data=survival_rate_df, ax=ax1, palette='pastel')
    ax1.set_xticklabels(['Tidak Selamat', 'Selamat'])
    ax1.set_ylabel('Jumlah Penumpang')
    ax1.set_title('Jumlah Penumpang yang Selamat dan Tidak Selamat', fontsize=15)
    st.pyplot(fig1)

st.write('### Distribusi Usia Penumpang')
fig2, ax2 = plt.subplots(figsize=(8, 6))
sns.histplot(age_distribution_df, bins=20, kde=True, color="skyblue", ax=ax2)
ax2.set_title('Distribusi Usia Penumpang', fontsize=15)
ax2.set_xlabel('Usia')
ax2.set_ylabel('Frekuensi')
st.pyplot(fig2)

if not class_survival_df.empty:
    st.write('### Hubungan Kelas Kabin dan Keselamatan')
    fig3, ax3 = plt.subplots(figsize=(8, 6))
    sns.barplot(x='Pclass', y='Count', hue='Survived', data=class_survival_df, ax=ax3, palette='pastel')
    ax3.set_xticklabels(['Kelas 1', 'Kelas 2', 'Kelas 3'])
    ax3.set_ylabel('Jumlah Penumpang')
    ax3.set_title('Hubungan Kelas Kabin dan Keselamatan', fontsize=15)
    st.pyplot(fig3)

total_passengers = len(data)
total_survived = data['Survived'].sum() if 'Survived' in data.columns else 0
survival_percentage = (total_survived / total_passengers) * 100 if total_passengers > 0 else 0

col1, col2, col3 = st.columns(3)
with col1:
    st.metric("Total Penumpang", value=total_passengers)
with col2:
    st.metric("Total yang Selamat", value=total_survived)
with col3:
    st.metric("Persentase Selamat", value=f"{survival_percentage:.2f}%")

st.subheader("Demografi Penumpang Titanic")

gender_distribution_df = data['Sex'].value_counts().reset_index()
gender_distribution_df.columns = ['Gender', 'Count']

fig4, ax4 = plt.subplots(figsize=(8, 6))
sns.barplot(x='Gender', y='Count', data=gender_distribution_df, ax=ax4, palette='pastel')
ax4.set_title('Distribusi Penumpang Berdasarkan Jenis Kelamin', fontsize=15)
ax4.set_xlabel('Jenis Kelamin')
ax4.set_ylabel('Jumlah Penumpang')
st.pyplot(fig4)

data['AgeGroup'] = pd.cut(data['Age'], bins=[0, 12, 18, 60, 100], labels=['Anak', 'Remaja', 'Dewasa', 'Lansia'])
age_group_distribution_df = data['AgeGroup'].value_counts().reset_index()
age_group_distribution_df.columns = ['Age Group', 'Count']

fig5, ax5 = plt.subplots(figsize=(8, 6))
sns.barplot(x='Age Group', y='Count', data=age_group_distribution_df, ax=ax5, palette='pastel')
ax5.set_title('Distribusi Penumpang Berdasarkan Kelompok Umur', fontsize=15)
ax5.set_xlabel('Kelompok Umur')
ax5.set_ylabel('Jumlah Penumpang')
st.pyplot(fig5)

# st.caption('Copyright © Data Analysis Titanic - 2025')
