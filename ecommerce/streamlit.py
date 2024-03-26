import streamlit as st
import yaml
from yaml.loader import SafeLoader
import streamlit_authenticator as stauth
from procedures import (
    display_product_order_by_name,
    apply_discount_to_product,
    add_to_cart,
    search_by_product_and_order,
    insert_customer,
    insert_transaction,
)


# Membuat aplikasi Streamlit
def main():
    st.title("Tokomplit")

    with open("config.yaml") as file:
        config = yaml.load(file, Loader=SafeLoader)

    authenticator = stauth.Authenticate(
        config["credentials"],
        config["cookie"]["name"],
        config["cookie"]["key"],
        config["cookie"]["expiry_days"],
        config["preauthorized"],
    )

    name, authentication_status, username = authenticator.login()

    choice = None
    if authentication_status:
        menu = [
            "Tampilkan Produk",
            "Terapkan Diskon",
            "Tambahkan ke Keranjang",
            "Cari Produk",
            "Tambahkan Pelanggan",
            "Tambahkan Transaksi",
            "Ubah Password",
            "Ubah Data Profil",
        ]

        st.sidebar.header(f"Welcome, *{name}*")
        choice = st.sidebar.selectbox("Pilih Aksi", menu)
        st.sidebar.divider()
        authenticator.logout("Logout", "sidebar", key="unique_key")

    if choice == "Tampilkan Produk" and authentication_status:
        display_product_order_by_name()
    elif choice == "Terapkan Diskon" and authentication_status:
        product_id = st.number_input("Masukkan ID Produk", min_value=1, step=1)
        discount = st.number_input("Masukkan Diskon", min_value=0.0, step=0.01)
        if st.button("Terapkan Diskon"):
            apply_discount_to_product(product_id, discount)
    elif choice == "Tambahkan ke Keranjang" and authentication_status:
        product_id = st.number_input("Masukkan ID Produk", min_value=1, step=1)
        user_id = st.number_input("Masukkan ID Pengguna", min_value=1, step=1)
        quantity = st.number_input("Masukkan Jumlah", min_value=1, step=1)
        if st.button("Tambahkan ke Keranjang"):
            add_to_cart(product_id, user_id, quantity)
    elif choice == "Cari Produk" and authentication_status:
        product_name = st.text_input("Masukkan Nama Produk")
        order_direction = st.radio("Pilih Arah Urutan", ["Asc", "Desc"])
        if st.button("Cari"):
            search_by_product_and_order(product_name, order_direction.lower())
    elif choice == "Tambahkan Pelanggan" and authentication_status:
        username = st.text_input("Masukkan Username")
        email = st.text_input("Masukkan Email")
        password = st.text_input("Masukkan Password", type="password")
        full_name = st.text_input("Masukkan Nama Lengkap")
        address = st.text_input("Masukkan Alamat")
        phone_number = st.text_input("Masukkan Nomor Telepon")
        is_active = st.checkbox("Aktifkan Akun?")
        if st.button("Tambahkan Pelanggan"):
            insert_customer(
                username, email, password, full_name, address, phone_number, is_active
            )
    elif choice == "Tambahkan Transaksi" and authentication_status:
        customer_id = st.number_input("Masukkan ID Pelanggan", min_value=1, step=1)
        shipping_address = st.text_input("Masukkan Alamat Pengiriman")
        total_amount = st.number_input(
            "Masukkan Total Jumlah", min_value=0.0, step=0.01
        )
        status = st.selectbox("Pilih Status", ["Pending", "Shipped", "Delivered"])
        if st.button("Tambahkan Transaksi"):
            insert_transaction(customer_id, shipping_address, total_amount, status)
    elif choice == "Ubah Password" and authentication_status:
        if st.session_state["authentication_status"]:
            try:
                if authenticator.reset_password(st.session_state["username"]):
                    st.success("Password modified successfully")
            except Exception as e:
                st.error(e)
    elif choice == "Ubah Data Profil" and authentication_status:
        if st.session_state["authentication_status"]:
            try:
                if authenticator.update_user_details(st.session_state["username"]):
                    st.success("Entries updated successfully")
            except Exception as e:
                st.error(e)
    else:
        if authentication_status is False:
            st.error("Username/password is incorrect")
        elif authentication_status is None:
            st.warning("Please enter your username and password")

        try:
            (
                email_of_registered_user,
                username_of_registered_user,
                name_of_registered_user,
            ) = authenticator.register_user(preauthorization=False)
            if email_of_registered_user:
                st.success("User registered successfully")
                with open("config.yaml", "w") as file:
                    yaml.dump(config, file, default_flow_style=False)
        except Exception as e:
            st.error(e)


if __name__ == "__main__":
    main()
