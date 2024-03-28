import streamlit as st
from procedures import (
    get_product_order_by_name,
    apply_discount_to_product,
    add_to_cart,
    search_by_product_and_order,
    insert_customer,
    insert_transaction,
)
import time


def sidebar(authenticator):
    if st.session_state.authentication_status:
        st.session_state.menu = [
            "Tampilkan Produk",
            "Terapkan Diskon",
            "Tambahkan ke Keranjang",
            "Cari Produk",
            "Tambahkan Pelanggan",
            "Tambahkan Transaksi",
            "Ubah Password",
            "Ubah Data Profil",
        ]

        st.sidebar.header(f"Welcome, *{st.session_state.name}*")
        st.session_state.choice = st.sidebar.selectbox(
            "Pilih Aksi", st.session_state.menu
        )
        st.sidebar.divider()
        authenticator.logout(location="sidebar")
    else:
        st.session_state.menu = ["Login", "Register"]
        st.session_state.choice = st.sidebar.selectbox(
            "Pilih Aksi", st.session_state.menu
        )


def on_beli_click(name, description, price, product_id):
    st.session_state.title = "Checkout"
    st.session_state.product_choice = {
        "name": name,
        "description": description,
        "price": price,
        "product_id": product_id,
    }


def product_card(name, description, price, product_id):
    with st.container(border=True):
        st.subheader(name)
        st.write(description)
        st.write("$", price)
        st.write("ID: ", product_id)
        st.button(
            "Buy",
            on_click=lambda: on_beli_click(name, description, price, product_id),
            key=name,
        )


def tampilkan_produk():
    data = get_product_order_by_name()
    col1, col2, col3 = st.columns(3)

    data_chunks = [
        data[i : i + int(len(data) / 3)]
        for i in range(0, len(data), int(len(data) / 3))
    ]

    with col1:
        for item in data_chunks[0]:
            product_card(item[2], item[3], item[4], item[1])

    with col2:
        for item in data_chunks[1]:
            product_card(item[2], item[3], item[4], item[1])

    with col3:
        for item in data_chunks[2]:
            product_card(item[2], item[3], item[4], item[1])


def checkout_product():
    st.session_state.title = "Tokomplit"
    time.sleep(3)

    st.success("Thank you for your purchase!")

    time.sleep(1)

    st.session_state.product_choice = None


def cancel():
    st.session_state.title = "Tokomplit"
    st.session_state.product_choice = None


def checkout():
    with st.container(border=True):
        st.subheader(st.session_state.product_choice["name"])
        st.write(st.session_state.product_choice["description"])
        st.write("Price: $", st.session_state.product_choice["price"])
        st.write("ID: ", st.session_state.product_choice["product_id"])
        st.button(
            "Checkout",
            key=st.session_state.product_choice["product_id"],
            on_click=checkout_product,
        )
        st.button("Cancel", key="cancel", on_click=cancel)


def terapkan_diskon():
    product_id = st.number_input("Masukkan ID Produk", min_value=1, step=1)
    discount = st.number_input("Masukkan Diskon", min_value=0.0, step=0.01)
    if st.button("Terapkan Diskon"):
        apply_discount_to_product(product_id, discount)


def tambahkan_ke_keranjang():
    product_id = st.number_input("Masukkan ID Produk", min_value=1, step=1)
    user_id = st.number_input("Masukkan ID Pengguna", min_value=1, step=1)
    quantity = st.number_input("Masukkan Jumlah", min_value=1, step=1)
    if st.button("Tambahkan ke Keranjang"):
        add_to_cart(product_id, user_id, quantity)


def cari_produk():
    product_name = st.text_input("Masukkan Nama Produk")
    order_direction = st.radio("Pilih Arah Urutan", ["Asc", "Desc"])
    if st.button("Cari"):
        search_by_product_and_order(product_name, order_direction.lower())


def tambahkan_pelanggan():
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


def tambahkan_transaksi():
    customer_id = st.number_input("Masukkan ID Pelanggan", min_value=1, step=1)
    shipping_address = st.text_input("Masukkan Alamat Pengiriman")
    total_amount = st.number_input("Masukkan Total Jumlah", min_value=0.0, step=0.01)
    status = st.selectbox("Pilih Status", ["Pending", "Shipped", "Delivered"])
    if st.button("Tambahkan Transaksi"):
        insert_transaction(customer_id, shipping_address, total_amount, status)
