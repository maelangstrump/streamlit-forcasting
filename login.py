import streamlit as st

USERS = {
    "admin": "smkn1sakra",
    "kepsek": "ppdb2025"
}


def show_login():

    # 🔒 Sembunyikan sidebar & menu navigasi saat di halaman login
    st.markdown(
        """
        <style>
            [data-testid="stSidebar"] {
                display: none;
            }
            [data-testid="collapsedControl"] {
                display: none;
            }
        </style>
        """,
        unsafe_allow_html=True
    )

    col1, col2, col3 = st.columns([2, 1, 2])
    with col2:
        st.image("assets/logo_smkn1sakra.png", width=150)

    st.markdown(
        """
        <h2 style='text-align:center'>
        🔐 Login Sistem Forecasting
        </h2>

        <p style='text-align:center;color:gray'>
        SMKN 1 Sakra
        </p>
        """,
        unsafe_allow_html=True
    )

    with st.form("login"):

        username = st.text_input("Username")

        password = st.text_input(
            "Password",
            type="password"
        )

        login = st.form_submit_button(
            "Masuk",
            use_container_width=True
        )

    if login:

        if username in USERS and USERS[username] == password:

            st.session_state.logged_in = True
            st.session_state.username = username

            st.success("Login berhasil...")

            st.switch_page("pages/Dashboard.py")

        else:

            st.error("Username atau Password salah")


if __name__ == "__main__":
    show_login()