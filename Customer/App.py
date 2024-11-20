from flask import Flask
from routes import customer_routes

app = Flask(__name__)

# Register the routes
app.register_blueprint(customer_routes)

if __name__ == '_main_':
    app.run(host='0.0.0.0', port=5000)