# pages/5_Rekomendasi_Kuota.py
import streamlit as st
import pandas as pd
import plotly.express as px
from io import BytesIO
from utils import load_data, load_model, get_daftar_jurusan, cek_login

st.set_page_config(page_title="Rekomendasi Kuota", page_icon="", layout="wide")
cek_login()

st.title("Rekomendasi Kuota PPDB")
st.caption("Estimasi kuota penerimaan siswa baru berdasarkan hasil prediksi ARIMA")
st.divider()

COL_JURUSAN = "Jurusan"
COL_JUMLAH  = "Jumlah"
TAHUN_PRED  = [2026, 2027, 2028]
BUFFER      = 1.10  # tambah buffer 10% untuk kuota

daftar_jurusan = get_daftar_jurusan()

# ── Generate Rekomendasi Semua Jurusan ────────────
rows = []
for jurusan in daftar_jurusan:
    model = load_model(jurusan)
    if model is None:
        continue
    forecast = model.predict(n_periods=len(TAHUN_PRED))
    for i, tahun in enumerate(TAHUN_PRED):
        pred   = max(0, round(forecast[i]))
        kuota  = max(0, round(pred * BUFFER))
        rows.append({
            "Jurusan": jurusan,
            "Tahun": tahun,
            "Prediksi Pendaftar": pred,
            "Rekomendasi Kuota": kuota,
        })

df_kuota = pd.DataFrame(rows)

# ── Metrik ────────────────────────────────────────
c1, c2, c3 = st.columns(3)
for i, tahun in enumerate(TAHUN_PRED):
    total = df_kuota[df_kuota["Tahun"] == tahun]["Rekomendasi Kuota"].sum()
    [c1, c2, c3][i].metric(f"Total Kuota {tahun}", f"{total:,} siswa")

st.divider()

# ── Filter Tahun ──────────────────────────────────
pilih_tahun = st.radio(
    "Tampilkan Tahun",
    TAHUN_PRED,
    horizontal=True
)

df_tampil = df_kuota[df_kuota["Tahun"] == pilih_tahun].reset_index(drop=True)

# ── Tabel ─────────────────────────────────────────
st.subheader(f"Rekomendasi Kuota Tahun {pilih_tahun}")
st.dataframe(
    df_tampil[["Jurusan", "Prediksi Pendaftar", "Rekomendasi Kuota"]]
    .style.background_gradient(subset=["Rekomendasi Kuota"], cmap="Blues"),
    use_container_width=True,
    hide_index=True,
)

st.caption("ℹ️ Rekomendasi kuota = prediksi pendaftar + buffer 10%")

st.divider()

# ── Grafik ────────────────────────────────────────
st.subheader(f"📊 Perbandingan Kuota Antar Jurusan — {pilih_tahun}")

fig = px.bar(
    df_tampil.sort_values("Rekomendasi Kuota", ascending=False),
    x="Jurusan",
    y=["Prediksi Pendaftar", "Rekomendasi Kuota"],
    barmode="group",
    color_discrete_map={
        "Prediksi Pendaftar": "#636EFA",
        "Rekomendasi Kuota": "#00CC96"
    },
    labels={"value": "Jumlah Siswa", "variable": "Keterangan"},
)
fig.update_layout(xaxis_tickangle=-30, legend_title="Keterangan")
st.plotly_chart(fig, use_container_width=True)

st.divider()

# ── Download Excel Semua Tahun ────────────────────
st.subheader("⬇️ Download Rekomendasi Kuota")

output = BytesIO()
with pd.ExcelWriter(output, engine="openpyxl") as writer:
    for tahun in TAHUN_PRED:
        df_dl = df_kuota[df_kuota["Tahun"] == tahun][
            ["Jurusan", "Prediksi Pendaftar", "Rekomendasi Kuota"]
        ]
        df_dl.to_excel(writer, sheet_name=str(tahun), index=False)

st.download_button(
    label="⬇️ Download Excel (Semua Tahun)",
    data=output.getvalue(),
    file_name="rekomendasi_kuota_2026_2028.xlsx",
    mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
)

# ── Sidebar logout ────────────────────────────────
with st.sidebar:
    st.write(f"👤 {st.session_state.get('username', '')}")
    if st.button("🚪 Logout"):
        st.session_state.clear()
        st.rerun()