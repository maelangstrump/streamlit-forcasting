# Home.py
import streamlit as st

# HARUS PALING ATAS
st.set_page_config(
    page_title="Home",
    page_icon="🏠",
    layout="wide"
)
# ── Custom CSS Sidebar Hijau ──────────────────────
st.markdown("""
    <style>
    /* Sidebar background */
    [data-testid="stSidebar"] {
        background-color: #E8F5E9 !important;
    }

    /* Semua teks di sidebar */
    [data-testid="stSidebar"] * {
        color: white !important;
    }

    /* Menu item aktif */
    [data-testid="stSidebar"] [aria-selected="true"] {
        background-color: #1B5E13 !important;
        border-radius: 8px;
        font-weight: bold;
    }

    /* Hover menu item */
    [data-testid="stSidebar"] a:hover {
        background-color: #3DAA2A !important;
        border-radius: 8px;
    }

    /* Tombol Logout */
    [data-testid="stSidebar"] button {
        background-color: white !important;
        color: #2E7D1F !important;
        border: none;
        border-radius: 8px;
        font-weight: bold;
    }

    /* Divider di sidebar */
    [data-testid="stSidebar"] hr {
        border-color: rgba(255,255,255,0.3) !important;
    }
    </style>
""", unsafe_allow_html=True)
# ─────────────────────────────────────────────────
from login import show_login
from utils import cek_login

# Cek apakah sudah login
if "logged_in" not in st.session_state or not st.session_state["logged_in"]:
    show_login()
    st.stop()   # Menghentikan eksekusi jika belum login

st.markdown(f"""
    <div style='padding: 1rem 0'>
        <h1> Sistem Forecasting Minat Jurusan</h1>
        <h3 style='color:gray'>SMKN 1 Sakra — Lombok Timur</h3>
    </div>
""", unsafe_allow_html=True)

st.divider()

col1, col2 = st.columns([2, 1])

with col1:
    st.subheader("📌 Tentang Sistem")
    st.write("""
        Sistem ini dirancang untuk membantu pihak sekolah dalam **memprediksi
        tren minat jurusan** calon peserta didik baru (PPDB) berdasarkan data
        historis tahun 2020–2025.

        Model yang digunakan adalah **ARIMA (AutoRegressive Integrated Moving Average)**
        yang dibangun menggunakan metode CRISP-DM dan divalidasi dengan
        metrik MAPE, RMSE, dan MAE.
    """)

    st.subheader("📚 Jurusan yang Tersedia")
    jurusan_list = [
        "Agribisnis Pengolahan Hasil Pertanian",
        "Agribisnis Tanaman Pangan Dan Hortikultura",
        "Agribisnis Ternak Ruminansia",
        "Gribisnis Ternak Unggas",
        "Alat mesin Pertanian",
        "Mekanisasi Pertanian",
        "Multimedia",
        "Perhotelan",
        "tata Kecantikan Kulit Dan Rambut",
        "Teknik Energi Surya, Hidro Dan Angin",
        "Teknik Komputer Dan Jaringan",
        "Usaha Layanan Wisata",
    ]

    for j in jurusan_list:
        st.markdown(f"- {j}")

with col2:
    st.subheader("📊 Ringkasan Data")
    st.metric("Periode Data", "2020 – 2025")
    st.metric("Jumlah Jurusan", "12 Jurusan")
    st.metric("Tahun Prediksi", "2026 – 2028")
    st.metric("Rata-rata MAPE", "~7.93%")

st.divider()

st.caption(f"Login sebagai: **{st.session_state.get('username', '-')}**")

# Tombol logout di sidebar
with st.sidebar:
    st.write(f"{st.session_state.get('username', '')}")

    if st.button("🚪 Logout"):
        st.session_state.clear()
        st.rerun()
