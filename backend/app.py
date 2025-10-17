from flask import Flask, jsonify, request
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy
from dotenv import load_dotenv
import os

load_dotenv()

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URL', 'sqlite:///rpg_characters.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

CORS(app)
db = SQLAlchemy(app)

# Import routes
from api import character_routes, export_routes

app.register_blueprint(character_routes.bp)
app.register_blueprint(export_routes.bp)

@app.route('/')
def index():
    return jsonify({
        'message': 'RPG Character Builder API',
        'version': '1.0.0',
        'endpoints': [
            '/api/characters',
            '/api/classes',
            '/api/skills',
            '/api/export'
        ]
    })

@app.route('/health')
def health():
    return jsonify({'status': 'healthy'})

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True, host='0.0.0.0', port=5000)
