# pages/2_Data_Explorer.py
import streamlit as st
import pandas as pd
from utils import load_data, cek_login

st.set_page_config(page_title="Data Explorer", page_icon="🔍", layout="wide")
cek_login()

st.title("🔍 Data Explorer")
st.caption("Telusuri data PPDB SMKN 1 Sakra per jurusan dan tahun")
st.divider()

df = load_data()

# ── Sesuaikan nama kolom ──────────────────────────
COL_TAHUN   = "Tahun"
COL_JURUSAN = "Jurusan"
COL_JUMLAH  = "Jumlah"
# ──────────────────────────────────────────────────

# ── Filter ────────────────────────────────────────
col1, col2 = st.columns(2)

with col1:
    pilih_jurusan = st.multiselect(
        "Filter Jurusan",
        options=sorted(df[COL_JURUSAN].unique().tolist()),
        default=sorted(df[COL_JURUSAN].unique().tolist()),
    )

with col2:
    pilih_tahun = st.multiselect(
        "Filter Tahun",
        options=sorted(df[COL_TAHUN].unique().tolist()),
        default=sorted(df[COL_TAHUN].unique().tolist()),
    )

# ── Terapkan Filter ───────────────────────────────
df_filtered = df[
    (df[COL_JURUSAN].isin(pilih_jurusan)) &
    (df[COL_TAHUN].isin(pilih_tahun))
].reset_index(drop=True)

st.divider()

# ── Metrik hasil filter ───────────────────────────
c1, c2, c3 = st.columns(3)
c1.metric("Total Baris Data", len(df_filtered))
c2.metric("Total Pendaftar", f"{df_filtered[COL_JUMLAH].sum():,}")
c3.metric("Rata-rata per Jurusan", f"{df_filtered[COL_JUMLAH].mean():,.1f}")

st.divider()

# ── Tabel Data ────────────────────────────────────
st.subheader("Tabel Data PPDB")

st.dataframe(
    df_filtered.style.background_gradient(subset=[COL_JUMLAH], cmap="Blues"),
    use_container_width=True,
    height=400,
)

# ── Download CSV ──────────────────────────────────
csv = df_filtered.to_csv(index=False).encode("utf-8")
st.download_button(
    label="⬇️ Download Data (CSV)",
    data=csv,
    file_name="data_ppdb_filtered.csv",
    mime="text/csv",
)

st.divider()

# ── Ringkasan per Jurusan ─────────────────────────
st.subheader("📊 Ringkasan per Jurusan")

df_summary = df_filtered.groupby(COL_JURUSAN)[COL_JUMLAH].agg(
    Total="sum",
    Rata_rata="mean",
    Minimum="min",
    Maksimum="max"
).round(1).reset_index()

df_summary.columns = ["Jurusan", "Total", "Rata-rata", "Minimum", "Maksimum"]

st.dataframe(
    df_summary.style.background_gradient(subset=["Total"], cmap="Greens"),
    use_container_width=True,
)

# ── Sidebar logout ────────────────────────────────
with st.sidebar:
    st.write(f"{st.session_state.get('username', '')}")
    if st.button("Logout"):
        st.session_state.clear()
        st.rerun()