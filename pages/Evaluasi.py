# pages/4_Evaluasi_Model.py
import streamlit as st
import pandas as pd
import plotly.express as px
from utils import cek_login

st.set_page_config(page_title="Evaluasi Model", page_icon="", layout="wide")
cek_login()

st.title("Evaluasi Model ARIMA")
st.caption("Performa model per jurusan berdasarkan MAPE, RMSE, dan MAE")
st.divider()

# ── Data Evaluasi ─────────────────────────────────
data_evaluasi = {
    "Jurusan": [
        "Agribisnis Pengolahan Hasil Pertanian",
        "Agribisnis Tanaman Pangan Dan Hortikultura",
        "Agribisnis Ternak Ruminansia",
        "Agribisnis Ternak Unggas",
        "Alat Mesin Pertanian",
        "Mekanisasi Pertanian",
        "Multimedia",
        "Perhotelan",
        "Tata Kecantikan Kulit Dan Rambut",
        "Teknik Energi Surya, Hidro Dan Angin",
        "Teknik Komputer Dan Jaringan",
        "Usaha Layanan Wisata",
    ],
    "Model": [
        "ARIMA(0,1,0)", "ARIMA(0,1,0)", "ARIMA(0,1,0)", "ARIMA(0,1,0)",
        "ARIMA(1,1,0)", "ARIMA(2,0,1)", "ARIMA(0,1,0)", "ARIMA(2,1,0)",
        "ARIMA(0,1,0)", "ARIMA(0,1,0)", "ARIMA(1,1,0)", "ARIMA(1,1,0)",
    ],
    "MAPE (%)": [24.07, 16.67, 0.00, 93.75, 12.03, 1.96, 0.00, 24.03, 94.64, 0.00, 0.00, 0.58],
    "RMSE":     [13.00, 6.00,  0.00, 30.00, 8.30,  1.33, 0.00, 53.83, 53.00, 0.00, 0.00, 0.43],
    "MAE":      [13.00, 6.00,  0.00, 30.00, 8.30,  1.33, 0.00, 53.83, 53.00, 0.00, 0.00, 0.43],
    "Akurasi (%)": [75.93, 83.33, 100.00, 6.25, 87.97, 98.04, 100.00, 75.97, 5.36, 100.00, 100.00, 99.42],
}

df_eval = pd.DataFrame(data_evaluasi)

# ── Kategori Akurasi ──────────────────────────────
def kategori_mape(mape):
    if mape < 10:
        return "✅ Sangat Akurat"
    elif mape < 20:
        return "🟡 Akurat"
    elif mape < 50:
        return "🟠 Cukup Akurat"
    else:
        return "🔴 Kurang Akurat"

df_eval["Kategori"] = df_eval["MAPE (%)"].apply(kategori_mape)

# ── Metrik Ringkasan ──────────────────────────────
c1, c2, c3, c4 = st.columns(4)
c1.metric("Jumlah Model", len(df_eval))
c2.metric("Rata-rata MAPE", f"{df_eval['MAPE (%)'].mean():.2f}%")
c3.metric("MAPE Terbaik", f"{df_eval['MAPE (%)'].min():.2f}%")
c4.metric("MAPE Terburuk", f"{df_eval['MAPE (%)'].max():.2f}%")

st.divider()

# ── Tabel Evaluasi ────────────────────────────────
st.subheader("📊 Tabel Performa Model")
st.dataframe(
    df_eval.style.background_gradient(subset=["MAPE (%)"], cmap="RdYlGn_r"),
    use_container_width=True,
    hide_index=True,
)

st.divider()

# ── Grafik MAPE ───────────────────────────────────
st.subheader("📈 Grafik MAPE per Jurusan")

fig_mape = px.bar(
    df_eval.sort_values("MAPE (%)"),
    x="MAPE (%)",
    y="Jurusan",
    orientation="h",
    color="MAPE (%)",
    color_continuous_scale="RdYlGn_r",
    text="MAPE (%)",
    labels={"MAPE (%)": "MAPE (%)"},
)
fig_mape.update_traces(texttemplate="%{text:.1f}%", textposition="outside")
fig_mape.update_layout(coloraxis_showscale=False, yaxis={"categoryorder": "total ascending"})
st.plotly_chart(fig_mape, use_container_width=True)

# ── Grafik RMSE & MAE ─────────────────────────────
st.subheader("📉 Perbandingan RMSE dan MAE")

df_melt = df_eval.melt(
    id_vars="Jurusan",
    value_vars=["RMSE", "MAE"],
    var_name="Metrik",
    value_name="Nilai"
)
fig_rmse = px.bar(
    df_melt,
    x="Jurusan",
    y="Nilai",
    color="Metrik",
    barmode="group",
    color_discrete_map={"RMSE": "#636EFA", "MAE": "#EF553B"},
)
fig_rmse.update_layout(xaxis_tickangle=-30)
st.plotly_chart(fig_rmse, use_container_width=True)

st.divider()

# ── Keterangan Kategori ───────────────────────────
st.subheader("📌 Keterangan Kategori Akurasi")
st.markdown("""
| Kategori | Rentang MAPE |
|----------|-------------|
| ✅ Sangat Akurat | < 10% |
| 🟡 Akurat | 10% – 20% |
| 🟠 Cukup Akurat | 20% – 50% |
| 🔴 Kurang Akurat | > 50% |
""")

# ── Sidebar logout ────────────────────────────────
with st.sidebar:
    st.write(f"👤 {st.session_state.get('username', '')}")
    if st.button("🚪 Logout"):
        st.session_state.clear()
        st.rerun()