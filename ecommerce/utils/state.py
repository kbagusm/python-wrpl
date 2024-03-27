import streamlit as st


def init_state():
    if "title" not in st.session_state:
        st.session_state.title = "Tokomplit"

    if "choice" not in st.session_state:
        st.session_state.choice = "Login"

    if "menu" not in st.session_state:
        st.session_state.menu = ["Login", "Register"]

    if "name" not in st.session_state:
        st.session_state.name = None

    if "authentication_status" not in st.session_state:
        st.session_state.authentication_status = None

    if "username" not in st.session_state:
        st.session_state.username = None

    if "product_choice" not in st.session_state:
        st.session_state.product_choice = None

    st.write(st.session_state)
