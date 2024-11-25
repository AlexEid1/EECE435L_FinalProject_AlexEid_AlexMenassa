from flask import Blueprint, request, jsonify

sales_bp = Blueprint('sales', __name__)

# Placeholder for database (to be replaced with actual DB integration)
inventory = [
    {"id": 1, "name": "Laptop", "price": 1200, "quantity": 10},
    {"id": 2, "name": "Phone", "price": 800, "quantity": 5}
]

customer_wallets = {
    "customer1": 1500,  # Example data
}

purchase_history = []

# Display available goods
@sales_bp.route('/display_goods', methods=['GET'])
def display_goods():
    available_goods = [{"name": item["name"], "price": item["price"]} for item in inventory if item["quantity"] > 0]
    return jsonify(available_goods), 200

# Get goods details
@sales_bp.route('/get_goods_details/<int:item_id>', methods=['GET'])
def get_goods_details(item_id):
    item = next((item for item in inventory if item["id"] == item_id), None)
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

    # Validate customer
    if username not in customer_wallets:
        return jsonify({"error": "Customer not found"}), 404

    # Validate item
    item = next((item for item in inventory if item["id"] == item_id), None)
    if not item or item["quantity"] < quantity:
        return jsonify({"error": "Item not available"}), 404

    # Validate funds
    total_cost = item["price"] * quantity
    if customer_wallets[username] < total_cost:
        return jsonify({"error": "Insufficient funds"}), 400

    # Process sale
    customer_wallets[username] -= total_cost
    item["quantity"] -= quantity
    purchase_history.append({"username": username, "item": item["name"], "quantity": quantity, "total": total_cost})

    return jsonify({"message": "Purchase successful", "remaining_balance": customer_wallets[username]}), 200

# Purchase history API
@sales_bp.route('/purchase_history/<string:username>', methods=['GET'])
def purchase_history_api(username):
    history = [record for record in purchase_history if record["username"] == username]
    return jsonify(history), 200
