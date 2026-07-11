# utils.py

import pickle
import os
import pandas as pd
import streamlit as st

# ===============================
# PATH
# ===============================
DATA_PATH = "jurusan dataset.xlsx"
MODEL_DIR = "models_arima"

# ===============================
# LOAD DATA
# ===============================
@st.cache_data
def load_data():

    if not os.path.exists(DATA_PATH):
        st.error(f"Dataset tidak ditemukan:\n{DATA_PATH}")
        st.stop()

    df = pd.read_excel(DATA_PATH)

    # Pastikan kolom wajib ada
    kolom_wajib = ["Tahun", "Jurusan"]

    for kolom in kolom_wajib:
        if kolom not in df.columns:
            st.error(f"Kolom '{kolom}' tidak ditemukan pada dataset.")
            st.write("Kolom yang tersedia:")
            st.write(df.columns.tolist())
            st.stop()

    # Jika belum ada kolom Jumlah,
    # hitung otomatis jumlah siswa per Tahun & Jurusan
    if "Jumlah" not in df.columns:
        df = (
            df.groupby(["Tahun", "Jurusan"])
              .size()
              .reset_index(name="Jumlah")
        )

    return df


# ===============================
# LOAD MODEL
# ===============================
@st.cache_resource
def load_model(nama_jurusan):

    safe_name = (
        nama_jurusan
        .strip()
        .replace(" ", "_")
        .replace("/", "-")
    )

    path = os.path.join(
        MODEL_DIR,
        f"arima_{safe_name}.pkl"
    )

    if not os.path.exists(path):
        return None

    with open(path, "rb") as f:
        return pickle.load(f)


# ===============================
# DAFTAR JURUSAN
# ===============================
def get_daftar_jurusan():

    df = load_data()

    return sorted(df["Jurusan"].unique().tolist())


# ===============================
# LOGIN
# ===============================
def cek_login():

    if (
        "logged_in" not in st.session_state
        or
        not st.session_state["logged_in"]
    ):
        st.warning("⚠️ Silakan login terlebih dahulu.")
        st.stop()

# ===============================
# CUSTOM CSS GLOBAL
# ===============================
def set_custom_css():
    st.markdown("""
        <style>
        /* Background hijau muda semua halaman */
        .stApp {
            background-color: #E8F5E9 !important;
        }

        /* Paksa semua teks hitam */
        html, body, [class*="css"], .stMarkdown, .stText,
        .stMetric, .stCaption, p, h1, h2, h3, h4, h5, h6,
        label, span, div {
            color: #000000 !important;
        }

        /* Sidebar background hijau tua */
        [data-testid="stSidebar"] {
            background-color: #2E7D1F !important;
        }

        /* Sidebar teks putih */
        [data-testid="stSidebar"] * {
            color: white !important;
        }

        /* Tombol logout sidebar */
        [data-testid="stSidebar"] button {
            background-color: white !important;
            color: #2E7D1F !important;
            border-radius: 8px;
            font-weight: bold;
        }
        </style>
    """, unsafe_allow_html=True)
