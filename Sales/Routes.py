import mysql.connector
from flask import Blueprint, request, jsonify

sales_bp = Blueprint('sales', __name__)

# Database connection
def get_db_connection():
    return mysql.connector.connect(
        host="mysql-container",
        user="root",
        password="admin",
        database="ecommerce"
    )

# Display available goods
@sales_bp.route('/display_goods', methods=['GET'])
def display_goods():
    connection = get_db_connection()
    cursor = connection.cursor(dictionary=True)
    cursor.execute("SELECT name, price FROM inventory WHERE quantity > 0")
    goods = cursor.fetchall()
    cursor.close()
    connection.close()
    return jsonify(goods), 200

# Get goods details
@sales_bp.route('/get_goods_details/<int:item_id>', methods=['GET'])
def get_goods_details(item_id):
    connection = get_db_connection()
    cursor = connection.cursor(dictionary=True)
    cursor.execute("SELECT * FROM inventory WHERE id = %s", (item_id,))
    item = cursor.fetchone()
    cursor.close()
    connection.close()
    if item:
        return jsonify(item), 200
    return jsonify({"error": "Item not found"}), 404

# Sale API
@sales_bp.route('/sale', methods=['POST'])
def sale():
    data = request.json
    username = data.get("username")
    item_id = data.get("item_id")
    quantity = data.get("quantity", 1)

    connection = get_db_connection()
    cursor = connection.cursor(dictionary=True)

    # Check if customer exists
    cursor.execute("SELECT wallet FROM customers WHERE username = %s", (username,))
    customer = cursor.fetchone()
    if not customer:
        cursor.close()
        connection.close()
        return jsonify({"error": "Customer not found"}), 404

    # Check if item exists and is available
    cursor.execute("SELECT name, price, quantity FROM inventory WHERE id = %s", (item_id,))
    item = cursor.fetchone()
    if not item or item["quantity"] < quantity:
        cursor.close()
        connection.close()
        return jsonify({"error": "Item not available"}), 404

    # Check customer wallet balance
    total_cost = item["price"] * quantity
    if customer["wallet"] < total_cost:
        cursor.close()
        connection.close()
        return jsonify({"error": "Insufficient funds"}), 400

    # Process sale
    cursor.execute("UPDATE customers SET wallet = wallet - %s WHERE username = %s", (total_cost, username))
    cursor.execute("UPDATE inventory SET quantity = quantity - %s WHERE id = %s", (quantity, item_id))
    cursor.execute(
        "INSERT INTO sales (username, item_name, quantity, total) VALUES (%s, %s, %s, %s)",
        (username, item["name"], quantity, total_cost)
    )
    connection.commit()
    cursor.close()
    connection.close()

    return jsonify({"message": "Purchase successful"}), 200

# Purchase history API
@sales_bp.route('/purchase_history/<string:username>', methods=['GET'])
def purchase_history_api(username):
    connection = get_db_connection()
    cursor = connection.cursor(dictionary=True)
    cursor.execute("SELECT * FROM sales WHERE username = %s", (username,))
    history = cursor.fetchall()
    cursor.close()
    connection.close()
    return jsonify(history), 200
