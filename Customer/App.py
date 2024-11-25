from flask import Flask
from Routes import customer_routes

app = Flask(__name__)

# Register the routes
app.register_blueprint(customer_routes)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)