import streamlit as st
import mysql.connector
import pandas as pd

# Fungsi untuk menampilkan produk sesuai urutan nama
def display_product_order_by_name():
    try:
        # Koneksi ke database
        connection = mysql.connector.connect(
            host='localhost',
            user='root',
            password='',
            database='db_ecommerce'
        )

        # cursor = connection.cursor()
        # cursor.callproc("DisplayProductOrderbyName")

        # # Menampilkan hasil
        # result = cursor.fetchall()
        # if not result:
        #     st.write("Tidak ada produk yang tersedia.")
        # else:
        #     st.write("Daftar Produk (Urutan Nama):")
        #     for row in result:
        #         st.write(row)

        # cursor.close()
        # connection.close()

        cursor = connection.cursor()

        # cursor.callproc("DisplayProductOrderbyName")

        # # Menampilkan hasil
        # data = cursor.fetchall()
        #Perform operations here

        cursor.execute("SELECT * FROM products")
        data = cursor.fetchall()

        # Print results.
        df = pd.DataFrame(data, columns=cursor.column_names)
        st.dataframe(df)

    except mysql.connector.Error as error:
        st.error("Terjadi kesalahan saat mengambil data produk: {}".format(error))


# Fungsi untuk menerapkan diskon pada produk
def apply_discount_to_product(product_id, discount):
    # Koneksi ke database
    connection = mysql.connector.connect(
        host='localhost',
        user='root',
        password='',
        database='db_ecommerce'
    )

    cursor = connection.cursor()
    cursor.callproc("ApplyDiscountToProduct", [product_id, discount])
    connection.commit()

    # Menampilkan hasil
    result = cursor.fetchall()
    st.write("Diskon berhasil diterapkan pada produk dengan ID", product_id)

    cursor.close()
    connection.close()

# Fungsi untuk menambahkan produk ke keranjang
def add_to_cart(product_id, user_id, quantity):
    # Koneksi ke database
    connection = mysql.connector.connect(
        host='localhost',
        user='root',
        password='',
        database='db_ecommerce'
    )

    cursor = connection.cursor()
    cursor.callproc("AddtoCart", [product_id, user_id, quantity])
    connection.commit()

    # Menampilkan hasil
    result = cursor.fetchall()
    st.write(quantity, "produk dengan ID", product_id, "telah ditambahkan ke keranjang pengguna dengan ID", user_id)

    cursor.close()
    connection.close()

# Fungsi untuk mencari produk berdasarkan nama dan urutan
def search_by_product_and_order(product_name, order_direction):
    # Koneksi ke database
    connection = mysql.connector.connect(
        host='localhost',
        user='root',
        password='',
        database='db_ecommerce'
    )

    cursor = connection.cursor()
    cursor.callproc("SearchbyProductandOrder", [product_name, order_direction])
    connection.commit()
    
    ini_list = []
    # Menampilkan hasil
    result = cursor.fetchall()
    st.write("Hasil pencarian produk dengan nama", product_name, "dengan urutan", order_direction)
    for result in cursor.stored_results():
        for row in result.fetchall():
            ini_list.append(row)

    df = pd.DataFrame(ini_list, columns=['ProductID', 'SellerID', 'Name', 'Description', 'Price', 'Stock', 'CategoryID'])
    st.dataframe(df)
    cursor.close()
    connection.close()

# Fungsi untuk menyisipkan pelanggan baru
def insert_customer(username, email, password, full_name, address, phone_number, is_active):
    # Koneksi ke database
    connection = mysql.connector.connect(
        host='localhost',
        user='root',
        password='',
        database='db_ecommerce'
    )

    cursor = connection.cursor()
    cursor.callproc("InsertCustomer", [username, email, password, full_name, address, phone_number, is_active])
    connection.commit()

    # Menampilkan hasil
    st.write("Pelanggan", full_name, "berhasil disisipkan.")

    cursor.close()
    connection.close()

# Fungsi untuk menyisipkan transaksi baru
def insert_transaction(customer_id, shipping_address, total_amount, status):
    # Koneksi ke database
    connection = mysql.connector.connect(
        host='localhost',
        user='root',
        password='',
        database='db_ecommerce'
    )

    cursor = connection.cursor()
    cursor.callproc("InsertTransaction", [customer_id, shipping_address, total_amount, status])
    connection.commit()

    # Menampilkan hasil
    st.write("Transaksi berhasil disisipkan.")

    cursor.close()
    connection.close()

# Membuat aplikasi Streamlit
def main():
    st.title("Aplikasi Web untuk Interaksi dengan Stored Procedure")

    menu = ["Tampilkan Produk", "Terapkan Diskon", "Tambahkan ke Keranjang", "Cari Produk", "Tambahkan Pelanggan", "Tambahkan Transaksi"]
    choice = st.sidebar.selectbox("Pilih Aksi", menu)

    if choice == "Tampilkan Produk":
        display_product_order_by_name()
    elif choice == "Terapkan Diskon":
        product_id = st.number_input("Masukkan ID Produk", min_value=1, step=1)
        discount = st.number_input("Masukkan Diskon", min_value=0.0, step=0.01)
        if st.button("Terapkan Diskon"):
            apply_discount_to_product(product_id, discount)
    elif choice == "Tambahkan ke Keranjang":
        product_id = st.number_input("Masukkan ID Produk", min_value=1, step=1)
        user_id = st.number_input("Masukkan ID Pengguna", min_value=1, step=1)
        quantity = st.number_input("Masukkan Jumlah", min_value=1, step=1)
        if st.button("Tambahkan ke Keranjang"):
            add_to_cart(product_id, user_id, quantity)
    elif choice == "Cari Produk":
        product_name = st.text_input("Masukkan Nama Produk")
        order_direction = st.radio("Pilih Arah Urutan", ["Asc", "Desc"])
        if st.button("Cari"):
            search_by_product_and_order(product_name, order_direction.lower())
    elif choice == "Tambahkan Pelanggan":
        username = st.text_input("Masukkan Username")
        email = st.text_input("Masukkan Email") 
        password = st.text_input("Masukkan Password", type="password")
        full_name = st.text_input("Masukkan Nama Lengkap")
        address = st.text_input("Masukkan Alamat")
        phone_number = st.text_input("Masukkan Nomor Telepon")
        is_active = st.checkbox("Aktifkan Akun?")
        if st.button("Tambahkan Pelanggan"):
            insert_customer(username, email, password, full_name, address, phone_number, is_active)
    elif choice == "Tambahkan Transaksi":
        customer_id = st.number_input("Masukkan ID Pelanggan", min_value=1, step=1)
        shipping_address = st.text_input("Masukkan Alamat Pengiriman")
        total_amount = st.number_input("Masukkan Total Jumlah", min_value=0.0, step=0.01)
        status = st.selectbox("Pilih Status", ["Pending", "Shipped", "Delivered"])
        if st.button("Tambahkan Transaksi"):
            insert_transaction(customer_id, shipping_address, total_amount, status)

if __name__ == "__main__":
    main()