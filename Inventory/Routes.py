from flask import Blueprint, request, jsonify
import mysql.connector

inventory_routes = Blueprint('inventory', __name__)

# Database connection configuration
db_config = {
    'host': 'mysql-container',  # Change to 'localhost' if not using Docker
    'user': 'root',
    'password': 'admin',
    'database': 'ecommerce'
}

def get_db_connection():
    """Establish a connection to the database."""
    return mysql.connector.connect(**db_config)

# 1. Add Goods
@inventory_routes.route('/add', methods=['POST'])
def add_goods():
    data = request.json
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        query = """
            INSERT INTO inventory (name, category, price, description, count)
            VALUES (%s, %s, %s, %s, %s)
        """
        cursor.execute(query, (
            data['name'], data['category'], data['price'],
            data['description'], data['count']
        ))
        conn.commit()
        return jsonify({"message": "Goods added successfully!"}), 201
    except mysql.connector.Error as e:
        return jsonify({"error": str(e)}), 500
    finally:
        cursor.close()
        conn.close()

# 2. Deduct Goods
@inventory_routes.route('/deduct/<int:item_id>', methods=['POST'])
def deduct_goods(item_id):
    data = request.json
    quantity = data.get('quantity', 1)  # Default to 1 item
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        # Check if item exists and has sufficient stock
        query = "SELECT count FROM inventory WHERE id = %s"
        cursor.execute(query, (item_id,))
        result = cursor.fetchone()
        if not result or result[0] < quantity:
            return jsonify({"message": "Item not found or insufficient stock"}), 400
        # Deduct the quantity
        update_query = "UPDATE inventory SET count = count - %s WHERE id = %s"
        cursor.execute(update_query, (quantity, item_id))
        conn.commit()
        return jsonify({"message": f"{quantity} items deducted from inventory"}), 200
    except mysql.connector.Error as e:
        return jsonify({"error": str(e)}), 500
    finally:
        cursor.close()
        conn.close()

# 3. Update Goods
@inventory_routes.route('/update/<int:item_id>', methods=['PUT'])
def update_goods(item_id):
    data = request.json
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        updates = ", ".join([f"{key} = %s" for key in data.keys()])
        query = f"UPDATE inventory SET {updates} WHERE id = %s"
        values = list(data.values()) + [item_id]
        cursor.execute(query, values)
        conn.commit()
        if cursor.rowcount == 0:
            return jsonify({"message": "Item not found or no changes made"}), 404
        return jsonify({"message": "Item updated successfully"}), 200
    except mysql.connector.Error as e:
        return jsonify({"error": str(e)}), 500
    finally:
        cursor.close()
        conn.close()

# 4. Get All Goods
@inventory_routes.route('/all', methods=['GET'])
def get_all_goods():
    try:
        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)
        query = "SELECT * FROM inventory"
        cursor.execute(query)
        goods = cursor.fetchall()
        return jsonify(goods), 200
    except mysql.connector.Error as e:
        return jsonify({"error": str(e)}), 500
    finally:
        cursor.close()
        conn.close()

# 5. Get Goods by ID
@inventory_routes.route('/<int:item_id>', methods=['GET'])
def get_goods_by_id(item_id):
    try:
        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)
        query = "SELECT * FROM inventory WHERE id = %s"
        cursor.execute(query, (item_id,))
        item = cursor.fetchone()
        if not item:
            return jsonify({"message": "Item not found"}), 404
        return jsonify(item), 200
    except mysql.connector.Error as e:
        return jsonify({"error": str(e)}), 500
    finally:
        cursor.close()
        conn.close()
