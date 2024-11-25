from flask import Flask

app = Flask(__name__)

# Import routes
from Routes import sales_bp

# Register routes
app.register_blueprint(sales_bp)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5002)
