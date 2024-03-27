import mysql.connector
import pandas as pd
import streamlit as st

# Koneksi ke database
connection = mysql.connector.connect(
    host="localhost", user="root", password="", database="wrpl"
)

cursor = connection.cursor()


# Fungsi untuk menampilkan produk sesuai urutan nama
def display_product_order_by_name():

    # Perform operations here
    cursor.execute("SELECT * FROM products")
    data = cursor.fetchall()

    # Print results.
    df = pd.DataFrame(data, columns=cursor.column_names)

    return df


# Fungsi untuk menerapkan diskon pada produk
def apply_discount_to_product(product_id, discount):
    # Koneksi ke database

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

    cursor.callproc("AddtoCart", [product_id, user_id, quantity])
    connection.commit()

    # Menampilkan hasil
    st.write(
        quantity,
        "produk dengan ID",
        product_id,
        "telah ditambahkan ke keranjang pengguna dengan ID",
        user_id,
    )

    cursor.close()
    connection.close()


# Fungsi untuk mencari produk berdasarkan nama dan urutan
def search_by_product_and_order(product_name, order_direction):
    # Koneksi ke database

    cursor.callproc("SearchbyProductandOrder", [product_name, order_direction])
    connection.commit()

    ini_list = []
    # Menampilkan hasil
    result = cursor.fetchall()
    st.write(
        "Hasil pencarian produk dengan nama",
        product_name,
        "dengan urutan",
        order_direction,
    )
    for result in cursor.stored_results():
        for row in result.fetchall():
            ini_list.append(row)

    df = pd.DataFrame(
        ini_list,
        columns=[
            "ProductID",
            "SellerID",
            "Name",
            "Description",
            "Price",
            "Stock",
            "CategoryID",
        ],
    )
    st.dataframe(df)
    cursor.close()
    connection.close()


# Fungsi untuk menyisipkan pelanggan baru
def insert_customer(
    username, email, password, full_name, address, phone_number, is_active
):
    # Koneksi ke database

    cursor.callproc(
        "InsertCustomer",
        [username, email, password, full_name, address, phone_number, is_active],
    )
    connection.commit()

    # Menampilkan hasil
    st.write("Pelanggan", full_name, "berhasil disisipkan.")

    cursor.close()
    connection.close()


# Fungsi untuk menyisipkan transaksi baru
def insert_transaction(customer_id, shipping_address, total_amount, status):
    # Koneksi ke database

    cursor.callproc(
        "InsertTransaction", [customer_id, shipping_address, total_amount, status]
    )
    connection.commit()

    # Menampilkan hasil
    st.write("Transaksi berhasil disisipkan.")

    cursor.close()
    connection.close()