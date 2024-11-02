from flask import Flask, jsonify
from flask_cors import CORS
from app.routes.user_routes import auth_bp
from app.routes.nids_routes import nids_bp
import os


app = Flask(__name__)

CORS(app)

app.secret_key = os.urandom(24).hex()

@app.route('/', methods=['GET'])
def home():
    return jsonify({"server_status": "running"})

app.register_blueprint(auth_bp, url_prefix='/api/auth')
app.register_blueprint(nids_bp, url_prefix='/api/nids')


if __name__ == '__main__':
    app.run(port=5000)
