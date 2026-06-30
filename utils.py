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