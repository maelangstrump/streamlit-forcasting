# pages/Dashboard.py

import streamlit as st
import pandas as pd
import plotly.express as px

from utils import load_data, cek_login

# ===========================
# Konfigurasi Halaman
# ===========================
st.set_page_config(
    page_title="Dashboard",
    page_icon="📊",
    layout="wide"
)

cek_login()

# ===========================
# Header
# ===========================
st.title("📊 Dashboard")
st.caption("Ringkasan Data PPDB SMKN 1 Sakra Tahun 2020–2025")

st.divider()

# ===========================
# Load Data
# ===========================
df = load_data()

# ==========================================================
# Jika dataset belum memiliki kolom Jumlah,
# hitung otomatis jumlah siswa berdasarkan Tahun dan Jurusan
# ==========================================================
if "Jumlah" not in df.columns:
    df = (
        df.groupby(["Tahun", "Jurusan"])
        .size()
        .reset_index(name="Jumlah")
    )

# ===========================
# Cek Kolom
# ===========================
required = ["Tahun", "Jurusan", "Jumlah"]

missing = [col for col in required if col not in df.columns]

if missing:
    st.error(f"Kolom berikut tidak ditemukan: {missing}")
    st.write("Kolom yang tersedia:")
    st.write(df.columns.tolist())
    st.stop()

# ===========================
# Ringkasan
# ===========================
total = df["Jumlah"].sum()

rata = (
    df.groupby("Tahun")["Jumlah"]
    .sum()
    .mean()
)

tahun_max = (
    df.groupby("Tahun")["Jumlah"]
    .sum()
    .idxmax()
)

jurusan_top = (
    df.groupby("Jurusan")["Jumlah"]
    .sum()
    .idxmax()
)

c1, c2, c3, c4 = st.columns(4)

c1.metric("Total Pendaftar", f"{int(total):,}")
c2.metric("Rata-rata per Tahun", f"{rata:.0f}")
c3.metric("Tahun Terbanyak", str(tahun_max))
c4.metric("Jurusan Terpopuler", jurusan_top)

st.divider()

# ===========================
# Grafik Tren
# ===========================
st.subheader("📈 Tren Pendaftar per Jurusan")

df_tren = (
    df.groupby(["Tahun", "Jurusan"])["Jumlah"]
    .sum()
    .reset_index()
)

fig = px.line(
    df_tren,
    x="Tahun",
    y="Jumlah",
    color="Jurusan",
    markers=True,
    labels={
        "Tahun": "Tahun",
        "Jumlah": "Jumlah Pendaftar",
        "Jurusan": "Jurusan"
    }
)

fig.update_layout(
    legend_title="Jurusan",
    hovermode="x unified"
)

st.plotly_chart(
    fig,
    use_container_width=True
)

st.divider()

# ===========================
# Grafik Bar & Heatmap
# ===========================
col1, col2 = st.columns(2)

# ---------------------------
# Grafik Bar
# ---------------------------
with col1:

    st.subheader("📊 Total Pendaftar per Tahun")

    df_total = (
        df.groupby("Tahun")["Jumlah"]
        .sum()
        .reset_index()
    )

    fig_bar = px.bar(
        df_total,
        x="Tahun",
        y="Jumlah",
        text="Jumlah",
        color="Jumlah",
        color_continuous_scale="Blues",
        labels={
            "Tahun": "Tahun",
            "Jumlah": "Total Pendaftar"
        }
    )

    fig_bar.update_traces(textposition="outside")
    fig_bar.update_layout(coloraxis_showscale=False)

    st.plotly_chart(
        fig_bar,
        use_container_width=True
    )

# ---------------------------
# Heatmap
# ---------------------------
with col2:

    st.subheader("Heatmap Peminat per Jurusan")

    heat = df.pivot_table(
        index="Jurusan",
        columns="Tahun",
        values="Jumlah",
        aggfunc="sum",
        fill_value=0
    )

    fig_heat = px.imshow(
        heat,
        text_auto=True,
        color_continuous_scale="YlOrRd",
        labels=dict(
            x="Tahun",
            y="Jurusan",
            color="Pendaftar"
        ),
        aspect="auto"
    )

    st.plotly_chart(
        fig_heat,
        use_container_width=True
    )

st.divider()

# ===========================
# Sidebar Logout
# ===========================
with st.sidebar:

    st.write(f"{st.session_state.get('username', '')}")

    if st.button("Logout"):
        st.session_state.clear()
        st.switch_page("home.py")