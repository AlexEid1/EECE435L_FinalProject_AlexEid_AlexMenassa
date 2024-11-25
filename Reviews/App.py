from flask import Flask
from Routes import reviews_bp

app = Flask(__name__)

app.register_blueprint(reviews_bp)

if __name__ == '_main_':
    app.run(host='0.0.0.0', port=5003)