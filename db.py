import mysql.connector

# Replace these values with your MySQL server information
host = 'localhost'
user = 'root'
password = ''
database = 'db_ecommerce'

def select_all_products():
    cursor = connection.cursor()

    cursor.execute("SELECT * FROM products")

    results = cursor.fetchall()
    for row in results:
        print(row)

    cursor.close()


def call_procedure(procedure_name):
    cursor.callproc(procedure_name)

    results = cursor.stored_results()
    for result in results:
        for row in result.fetchall():
            print(row)


# Establish a connection to the MySQL server
try:
    connection = mysql.connector.connect(
        host=host,
        user=user,
        password=password,
        database=database
    )

    if connection.is_connected():
        print("Connected to MySQL database")

        # Perform operations here
        cursor = connection.cursor()

        cursor.callproc("DisplayProductOrderbyName")

        results = cursor.stored_results()
        for result in results:
            for row in result.fetchall():
                print(row)

        # cursor.callproc("ApplyDiscountToProduct", (2, 20.00))

        # connection.commit()

        cursor.close()

except mysql.connector.Error as e:
    print(f"Error: {e}")

finally:
    # Close the connection when done
    if 'connection' in locals() and connection.is_connected():
        connection.close()
        print("Connection closed")
