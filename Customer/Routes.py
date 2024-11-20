from flask import Blueprint, request, jsonify
import mysql.connector

customer_routes = Blueprint('customers', __name__)

# Database connection config
db_config = {
    'host': 'mysql-container',  
    'user': 'root',
    'password': 'yourpassword',
    'database': 'ecommerce'
}

def get_db_connection():
    """Establish a connection to the database."""
    return mysql.connector.connect(**db_config)

# 1 Customer Registration
@customer_routes.route('/register', methods=['POST'])
def register_customer():
    data = request.json
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        query = """
            INSERT INTO customers (full_name, username, password, age, address, gender, marital_status, wallet_balance, admin)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
        """
        cursor.execute(query, (
            data['full_name'], data['username'], data['password'], data['age'],
            data['address'], data['gender'], data['marital_status'], 0.00, data.get('admin', False)
        ))
        conn.commit()
        return jsonify({"message": "Customer registered successfully!"}), 201
    except mysql.connector.Error as e:
        return jsonify({"error": str(e)}), 500
    finally:
        cursor.close()
        conn.close()

# 2 Delete Customer
@customer_routes.route('/delete/<username>', methods=['DELETE'])
def delete_customer(username):
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        query = "DELETE FROM customers WHERE username = %s"
        cursor.execute(query, (username,))
        conn.commit()
        if cursor.rowcount == 0:
            return jsonify({"message": "Customer not found"}), 404
        return jsonify({"message": "Customer deleted successfully"}), 200
    except mysql.connector.Error as e:
        return jsonify({"error": str(e)}), 500
    finally:
        cursor.close()
        conn.close()

# 3 Update Customer Information
@customer_routes.route('/update/<username>', methods=['PUT'])
def update_customer(username):
    data = request.json
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        updates = ", ".join([f"{key} = %s" for key in data.keys()])
        query = f"UPDATE customers SET {updates} WHERE username = %s"
        values = list(data.values()) + [username]
        cursor.execute(query, values)
        conn.commit()
        if cursor.rowcount == 0:
            return jsonify({"message": "Customer not found or no changes made"}), 404
        return jsonify({"message": "Customer updated successfully"}), 200
    except mysql.connector.Error as e:
        return jsonify({"error": str(e)}), 500
    finally:
        cursor.close()
        conn.close()

# 4 Get All Customers
@customer_routes.route('/all', methods=['GET'])
def get_all_customers():
    try:
        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)
        query = "SELECT * FROM customers"
        cursor.execute(query)
        customers = cursor.fetchall()
        return jsonify(customers), 200
    except mysql.connector.Error as e:
        return jsonify({"error": str(e)}), 500
    finally:
        cursor.close()
        conn.close()

# 5 Get Customer by Username
@customer_routes.route('/<username>', methods=['GET'])
def get_customer_by_username(username):
    try:
        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)
        query = "SELECT * FROM customers WHERE username = %s"
        cursor.execute(query, (username,))
        customer = cursor.fetchone()
        if not customer:
            return jsonify({"message": "Customer not found"}), 404
        return jsonify(customer), 200
    except mysql.connector.Error as e:
        return jsonify({"error": str(e)}), 500
    finally:
        cursor.close()
        conn.close()

# 6 Charge Customer Wallet
@customer_routes.route('/charge/<username>', methods=['POST'])
def charge_wallet(username):
    data = request.json
    amount = data.get('amount')
    if amount is None or amount <= 0:
        return jsonify({"message": "Invalid amount"}), 400
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        query = "UPDATE customers SET wallet_balance = wallet_balance + %s WHERE username = %s"
        cursor.execute(query, (amount, username))
        conn.commit()
        if cursor.rowcount == 0:
            return jsonify({"message": "Customer not found"}), 404
        return jsonify({"message": f"${amount} charged to wallet"}), 200
    except mysql.connector.Error as e:
        return jsonify({"error": str(e)}), 500
    finally:
        cursor.close()
        conn.close()

# 7 Deduct Money from Wallet
@customer_routes.route('/deduct/<username>', methods=['POST'])
def deduct_wallet(username):
    data = request.json
    amount = data.get('amount')
    if amount is None or amount <= 0:
        return jsonify({"message": "Invalid amount"}), 400
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        #This is to check if our customer has enough money 
        query = "SELECT wallet_balance FROM customers WHERE username = %s"
        cursor.execute(query, (username,))
        result = cursor.fetchone()
        if not result or result[0] < amount:
            return jsonify({"message": "Insufficient balance or customer not found"}), 400

        #And if he does, we deduct the amount needed for the purchase
        update_query = "UPDATE customers SET wallet_balance = wallet_balance - %s WHERE username = %s"
        cursor.execute(update_query, (amount, username))
        conn.commit()
        return jsonify({"message": f"${amount} deducted from wallet"}), 200
    except mysql.connector.Error as e:
        return jsonify({"error": str(e)}), 500
    finally:
        cursor.close()
        conn.close()