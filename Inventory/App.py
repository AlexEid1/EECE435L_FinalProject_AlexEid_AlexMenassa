from flask import Flask
from Routes import inventory_routes

app = Flask(__name__)

# Register routes for the Inventory service
app.register_blueprint(inventory_routes, url_prefix='/inventory')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5001)