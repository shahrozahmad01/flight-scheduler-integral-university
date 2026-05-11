import os
from flask import Flask, jsonify
from flask_cors import CORS
from database import db
from config import get_config
from routes.flights import flights_bp
from routes.passengers import passengers_bp
from routes.bookings import bookings_bp
from routes.disruptions import disruptions_bp
from routes.rebooking import rebooking_bp

def create_app():
    app = Flask(__name__)
    app.config.from_object(get_config())

    cors_origins = os.environ.get(
        'CORS_ORIGINS',
        'http://localhost:5500,http://127.0.0.1:5500,http://localhost:3000'
    )
    allowed_origins = [url.strip() for url in cors_origins.split(',')]
    CORS(app, origins=allowed_origins)

    db.init_app(app)
    app.register_blueprint(flights_bp)
    app.register_blueprint(passengers_bp)
    app.register_blueprint(bookings_bp)
    app.register_blueprint(disruptions_bp)
    app.register_blueprint(rebooking_bp)

    with app.app_context():
        db.create_all()

    @app.route('/')
    def index():
        return jsonify({'message': 'Flight Scheduler API', 'status': 'running'})

    @app.errorhandler(404)
    def not_found(e):
        return jsonify({'error': 'Not found'}), 404

    @app.errorhandler(500)
    def server_error(e):
        return jsonify({'error': 'Internal server error'}), 500

    return app

if __name__ == '__main__':
    app = create_app()
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=True)
