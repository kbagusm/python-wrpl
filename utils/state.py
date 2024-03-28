import streamlit as st


def init_state():
    if "title" not in st.session_state:
        st.session_state.title = "Tokomplit"

    if "choice" not in st.session_state:
        st.session_state.choice = "Login"

    if "menu" not in st.session_state:
        st.session_state.menu = ["Login", "Register"]

    if "product_choice" not in st.session_state:
        st.session_state.product_choice = None
