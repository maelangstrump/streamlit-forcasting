# pages/3_Prediksi.py
import streamlit as st
import pandas as pd
import plotly.express as px
from io import BytesIO
from utils import load_data, load_model, get_daftar_jurusan, cek_login

st.set_page_config(page_title="Prediksi", page_icon="", layout="wide")
cek_login()

st.title("Prediksi Minat Jurusan")
st.caption("Hasil forecasting ARIMA untuk tahun yang dipilih")
st.divider()

# ── Sesuaikan nama kolom ──────────────────────────
COL_TAHUN   = "Tahun"
COL_JURUSAN = "Jurusan"
COL_JUMLAH  = "Jumlah"
TAHUN_MULAI = 2026
# ──────────────────────────────────────────────────

df = load_data()
daftar_jurusan = get_daftar_jurusan()

# ── Pilih Jurusan ─────────────────────────────────
pilih_jurusan = st.selectbox("Pilih Jurusan", daftar_jurusan)

# ── Slider Jumlah Tahun Prediksi ──────────────────
jumlah_tahun = st.slider(
    "Jumlah Tahun Prediksi",
    min_value=1,
    max_value=5,
    value=3
)

TAHUN_PRED = list(range(TAHUN_MULAI, TAHUN_MULAI + jumlah_tahun))

# ── Tombol Prediksi ───────────────────────────────
prediksi_btn = st.button(
    "Prediksi",
    use_container_width=True
)

if prediksi_btn:
    with st.spinner("Sedang menghitung prediksi..."):

        model = load_model(pilih_jurusan)

        if model is None:
            st.error(f"❌ Model untuk jurusan **{pilih_jurusan}** tidak ditemukan. Pastikan file .pkl tersedia di folder `models/`.")
            st.stop()

        # ── Info Orde ARIMA ───────────────────────
        try:
            st.info(f"Model ARIMA : {model.model.order}")
        except:
            pass

        # ── Data Historis ─────────────────────────
        df_hist = df[df[COL_JURUSAN] == pilih_jurusan][[COL_TAHUN, COL_JUMLAH]].copy()
        df_hist = df_hist.sort_values(COL_TAHUN).reset_index(drop=True)

        # ── Prediksi ──────────────────────────────
        try:
            forecast = model.forecast(steps=len(TAHUN_PRED))
            forecast = forecast.tolist()
            forecast = [max(0, int(round(x))) for x in forecast]

        except Exception as e:
            st.error(f"Gagal melakukan prediksi: {e}")
            st.stop()

        df_pred = pd.DataFrame({
            COL_TAHUN: TAHUN_PRED,
            COL_JUMLAH: forecast,
            "Tipe": ["Prediksi"] * len(TAHUN_PRED)
        })

        df_hist["Tipe"] = "Historis"

        df_gabung = pd.concat([df_hist, df_pred], ignore_index=True)

        # ── Ringkasan Prediksi (Metrik Dinamis) ───
        st.subheader("📊 Ringkasan Prediksi")

        cols = st.columns(len(forecast))
        for i, nilai in enumerate(forecast):
            cols[i].metric(
                f"Tahun {TAHUN_PRED[i]}",
                f"{nilai:,} siswa"
            )

        st.divider()

        # ── Grafik Forecasting ────────────────────
        st.subheader("📈 Grafik Forecasting")

        fig = px.line(
            df_gabung,
            x=COL_TAHUN,
            y=COL_JUMLAH,
            color="Tipe",
            markers=True,
            color_discrete_map={"Historis": "#1f77b4", "Prediksi": "#ff7f0e"},
            labels={COL_TAHUN: "Tahun", COL_JUMLAH: "Jumlah Pendaftar"},
        )

        fig.update_layout(
            hovermode="x unified",
            legend_title="Keterangan",
            template="plotly_white",
            height=520,
            title=f"Forecast Jurusan {pilih_jurusan}",
            xaxis_title="Tahun",
            yaxis_title="Jumlah Pendaftar",
            legend_title_text="Data"
        )

        # Garis pemisah historis vs prediksi
        fig.add_vline(
            x=TAHUN_MULAI - 0.5,
            line_dash="dash",
            line_color="gray",
            annotation_text="Mulai Prediksi",
            annotation_position="top left"
        )

        st.plotly_chart(fig, use_container_width=True)

        st.divider()

        # ── Tabel Hasil Forecasting ───────────────
        st.subheader("Hasil Forecasting")
        st.dataframe(
            df_pred[[COL_TAHUN, COL_JUMLAH]].rename(
                columns={COL_TAHUN: "Tahun", COL_JUMLAH: "Prediksi Pendaftar"}
            ),
            use_container_width=True,
            hide_index=True,
        )

        # ── Expander Data Historis ────────────────
        with st.expander("📂 Lihat Data Historis"):
            st.dataframe(
                df_hist[[COL_TAHUN, COL_JUMLAH]],
                use_container_width=True,
                hide_index=True
            )

        # ── Download Excel ────────────────────────
        output = BytesIO()
        with pd.ExcelWriter(output, engine="openpyxl") as writer:
            df_hist[[COL_TAHUN, COL_JUMLAH]].rename(
                columns={COL_JUMLAH: "Historis"}
            ).to_excel(writer, sheet_name="Historis", index=False)
            df_pred[[COL_TAHUN, COL_JUMLAH]].rename(
                columns={COL_JUMLAH: "Prediksi"}
            ).to_excel(writer, sheet_name="Prediksi", index=False)

        st.download_button(
            label="⬇️ Download Hasil Excel",
            data=output.getvalue(),
            file_name=f"prediksi_{pilih_jurusan.replace(' ', '_')}.xlsx",
            mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
        )

# ── Sidebar logout ────────────────────────────────
with st.sidebar:
    st.write(f"👤 {st.session_state.get('username', '')}")
    if st.button("Logout"):
        st.session_state.clear()
        st.rerun()