import mysql.connector
from flask import Blueprint, request, jsonify

reviews_bp = Blueprint('reviews', __name__)

# Database connection
def get_db_connection():
    return mysql.connector.connect(
        host="mysql-container",
        user="root",
        password="admin",
        database="ecommerce"
    )

# Submit a new review
@reviews_bp.route('/submit_review', methods=['POST'])
def submit_review():
    data = request.json
    customer_id = data.get("customer_id")
    product_id = data.get("product_id")
    rating = data.get("rating")
    comment = data.get("comment")

    connection = get_db_connection()
    cursor = connection.cursor()

    query = (
        "INSERT INTO reviews (customer_id, product_id, rating, comment) "
        "VALUES (%s, %s, %s, %s)"
    )
    cursor.execute(query, (customer_id, product_id, rating, comment))
    connection.commit()

    cursor.close()
    connection.close()

    return jsonify({'message': 'Review submitted successfully!'}), 201

# Update an existing review
@reviews_bp.route('/update_review/<int:review_id>', methods=['PUT'])
def update_review(review_id):
    data = request.json
    rating = data.get("rating")
    comment = data.get("comment")

    connection = get_db_connection()
    cursor = connection.cursor()

    query = (
        "UPDATE reviews "
        "SET rating = %s, comment = %s "
        "WHERE id = %s"
    )
    cursor.execute(query, (rating, comment, review_id))
    connection.commit()

    cursor.close()
    connection.close()

    return jsonify({'message': f'Review {review_id} updated successfully!'}), 200

# Delete a review
@reviews_bp.route('/delete_review/<int:review_id>', methods=['DELETE'])
def delete_review(review_id):
    connection = get_db_connection()
    cursor = connection.cursor()

    query = "DELETE FROM reviews WHERE id = %s"
    cursor.execute(query, (review_id,))
    connection.commit()

    cursor.close()
    connection.close()

    return jsonify({'message': f'Review {review_id} deleted successfully!'}), 200

# Get all reviews for a product
@reviews_bp.route('/get_product_reviews/<int:product_id>', methods=['GET'])
def get_product_reviews(product_id):
    connection = get_db_connection()
    cursor = connection.cursor(dictionary=True)

    query = "SELECT * FROM reviews WHERE product_id = %s"
    cursor.execute(query, (product_id,))
    reviews = cursor.fetchall()

    cursor.close()
    connection.close()

    return jsonify(reviews), 200

# Get all reviews by a customer
@reviews_bp.route('/get_customer_reviews/<int:customer_id>', methods=['GET'])
def get_customer_reviews(customer_id):
    connection = get_db_connection()
    cursor = connection.cursor(dictionary=True)

    query = "SELECT * FROM reviews WHERE customer_id = %s"
    cursor.execute(query, (customer_id,))
    reviews = cursor.fetchall()

    cursor.close()
    connection.close()

    return jsonify(reviews), 200

# Moderate a review
@reviews_bp.route('/moderate_review/<int:review_id>', methods=['PUT'])
def moderate_review(review_id):
    data = request.json
    flag = data.get("flag")

    connection = get_db_connection()
    cursor = connection.cursor()

    query = (
        "UPDATE reviews "
        "SET flag = %s "
        "WHERE id = %s"
    )
    cursor.execute(query, (flag, review_id))
    connection.commit()

    cursor.close()
    connection.close()

    return jsonify({'message': f'Review {review_id} moderation updated!'}), 200

# Get review details
@reviews_bp.route('/get_review_details/<int:review_id>', methods=['GET'])
def get_review_details(review_id):
    connection = get_db_connection()
    cursor = connection.cursor(dictionary=True)

    query = "SELECT * FROM reviews WHERE id = %s"
    cursor.execute(query, (review_id,))
    review = cursor.fetchone()

    cursor.close()
    connection.close()

    if review:
        return jsonify(review), 200
    return jsonify({'error': 'Review not found'}), 404