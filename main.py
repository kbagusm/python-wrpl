import streamlit as st
import mysql.connector
import pandas as pd

# Establish a connection to the MySQL server
connection = mysql.connector.connect(
    host="127.0.0.1",
    port=3306,
    user="root",
    password="",
    database="db_ecomm"
)

cursor = connection.cursor()

# Perform operations here
cursor.execute("SELECT * FROM products")
data = cursor.fetchall()


st.title("Data from MySQL")

# Print results.
df = pd.DataFrame(data, columns=cursor.column_names)
st.dataframe(df)
