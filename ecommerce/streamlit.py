import streamlit as st
import yaml
from yaml.loader import SafeLoader
import streamlit_authenticator as stauth
import pandas as pd
from utils.components import (
    tampilkan_produk,
    terapkan_diskon,
    tambahkan_ke_keranjang,
    cari_produk,
    tambahkan_pelanggan,
    tambahkan_transaksi,
    checkout,
)
from utils.state import init_state
from utils.components import sidebar


# Membuat aplikasi Streamlit
def main():
    # Initialization
    init_state()

    with open("config.yaml") as file:
        config = yaml.load(file, Loader=SafeLoader)

    authenticator = stauth.Authenticate(
        config["credentials"],
        config["cookie"]["name"],
        config["cookie"]["key"],
        config["cookie"]["expiry_days"],
        config["preauthorized"],
    )

    # Sidebar
    sidebar(authenticator)

    # Main application
    st.title(st.session_state.title)
    st.divider()

    if (
        st.session_state.choice == "Tampilkan Produk"
        and st.session_state.authentication_status
    ):
        if st.session_state.product_choice is not None:
            checkout()
        else:
            tampilkan_produk()

    elif (
        st.session_state.choice == "Terapkan Diskon"
        and st.session_state.authentication_status
    ):
        terapkan_diskon()
    elif (
        st.session_state.choice == "Tambahkan ke Keranjang"
        and st.session_state.authentication_status
    ):
        tambahkan_ke_keranjang()
    elif (
        st.session_state.choice == "Cari Produk"
        and st.session_state.authentication_status
    ):
        cari_produk()
    elif (
        st.session_state.choice == "Tambahkan Pelanggan"
        and st.session_state.authentication_status
    ):
        tambahkan_pelanggan()
    elif (
        st.session_state.choice == "Tambahkan Transaksi"
        and st.session_state.authentication_status
    ):
        tambahkan_transaksi()

    # Authentication Pages
    elif (
        st.session_state.choice == "Ubah Password"
        and st.session_state.authentication_status
    ):
        try:
            if authenticator.reset_password(st.session_state["username"]):
                st.success("Password modified successfully")
                with open("config.yaml", "w") as file:
                    yaml.dump(config, file, default_flow_style=False)
        except Exception as e:
            st.error(e)
    elif (
        st.session_state.choice == "Ubah Data Profil"
        and st.session_state.authentication_status
    ):
        try:
            if authenticator.update_user_details(st.session_state["username"]):
                st.success("Entries updated successfully")
                with open("config.yaml", "w") as file:
                    yaml.dump(config, file, default_flow_style=False)
        except Exception as e:
            st.error(e)
    elif st.session_state.choice == "Login":
        authenticator.login()
        if st.session_state.authentication_status is False:
            st.error("Username/password is incorrect")
        elif st.session_state.authentication_status is None:
            st.warning("Please enter your username and password")
    elif st.session_state.choice == "Register":
        try:
            (
                email_of_registered_user,
                _,
                _,
            ) = authenticator.register_user(pre_authorization=False)
            if email_of_registered_user:
                st.success("User registered successfully")
                with open("config.yaml", "w") as file:
                    yaml.dump(config, file, default_flow_style=False)
        except Exception as e:
            st.error(e)


if __name__ == "__main__":
    main()
