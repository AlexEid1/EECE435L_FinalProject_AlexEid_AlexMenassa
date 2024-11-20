import mysql.connector
from mysql.connector import errorcode

DB_CONFIG = {
    'host': 'localhost',
    'user': 'root',
    'password': 'admin',
}

DB_NAME = "ecommerce"

TABLES = {
    "customers": """
        CREATE TABLE IF NOT EXISTS customers (
            id INT AUTO_INCREMENT PRIMARY KEY,
            admin BOOLEAN DEFAULT FALSE,
            full_name VARCHAR(100) NOT NULL,
            username VARCHAR(50) UNIQUE NOT NULL,
            password VARCHAR(100) NOT NULL,
            age INT NOT NULL,
            address TEXT,
            gender ENUM('Male', 'Female'),
            marital_status ENUM('Single', 'Married'),
            wallet_balance DECIMAL(10, 2) DEFAULT 0.00
        );
    """,
    "inventory": """
        CREATE TABLE IF NOT EXISTS inventory (
            id INT AUTO_INCREMENT PRIMARY KEY,
            name VARCHAR(100) NOT NULL,
            category ENUM('food', 'clothes', 'accessories', 'electronics') NOT NULL,
            price DECIMAL(10, 2) NOT NULL,
            description TEXT,
            count INT NOT NULL
        );
    """,
    "sales": """
        CREATE TABLE IF NOT EXISTS sales (
            id INT AUTO_INCREMENT PRIMARY KEY,
            customer_id INT NOT NULL,
            product_id INT NOT NULL,
            sale_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (customer_id) REFERENCES customers(id),
            FOREIGN KEY (product_id) REFERENCES inventory(id)
        );
    """,
    "reviews": """
        CREATE TABLE IF NOT EXISTS reviews (
            id INT AUTO_INCREMENT PRIMARY KEY,
            customer_id INT NOT NULL,
            product_id INT NOT NULL,
            rating INT CHECK (rating BETWEEN 1 AND 5),
            comment TEXT,
            flag BOOLEAN DEFAULT FALSE,
            FOREIGN KEY (customer_id) REFERENCES customers(id),
            FOREIGN KEY (product_id) REFERENCES inventory(id)
        );
    """
}

def create_database(cursor):
    try:
        cursor.execute(f"CREATE DATABASE {DB_NAME}")
        print(f"Database {DB_NAME} created successfully.")
    except mysql.connector.Error as err:
        if err.errno == errorcode.ER_DB_CREATE_EXISTS:
            print(f"Database {DB_NAME} already exists.")
        else:
            print(f"Failed to create database: {err}")

def create_tables(cursor):
    for table_name, table_query in TABLES.items():
        try:
            cursor.execute(table_query)
            print(f"Table {table_name} created successfully.")
        except mysql.connector.Error as err:
            print(f"Failed to create table {table_name}: {err}")

def main():
    try:
        cnx = mysql.connector.connect(**DB_CONFIG)
        cursor = cnx.cursor()

        create_database(cursor)

        cnx.database = DB_NAME

        create_tables(cursor)

    except mysql.connector.Error as err:
        print(f"Error: {err}")
    finally:
        if cursor:
            cursor.close()
        if cnx:
            cnx.close()

if __name__ == "__main__":
    main()
