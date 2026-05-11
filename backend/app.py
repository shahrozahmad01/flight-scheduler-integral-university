# backend/app.py
import os
from flask import Flask, jsonify
from flask_cors import CORS
from database import db
from config import get_config

# Import all blueprints
from routes.flights import flights_bp
from routes.passengers import passengers_bp
from routes.bookings import bookings_bp
from routes.disruptions import disruptions_bp
from routes.rebooking import rebooking_bp

def create_app():
    app = Flask(__name__)

    # Load config based on FLASK_ENV
    app.config.from_object(get_config())

    # ─── CHANGE THIS AFTER VERCEL DEPLOY ──────────────────────────────
    # Replace the URL below with your actual Vercel URL once you have it
    vercel_url = os.environ.get(
        'CORS_ORIGINS',
        'http://localhost:5500,http://127.0.0.1:5500,http://localhost:3000'
    )
    allowed_origins = [url.strip() for url in vercel_url.split(',')]
    CORS(app, origins=allowed_origins)
    # ──────────────────────────────────────────────────────────────────

    # Initialize database
    db.init_app(app)

    # Register blueprints
    app.register_blueprint(flights_bp)
    app.register_blueprint(passengers_bp)
    app.register_blueprint(bookings_bp)
    app.register_blueprint(disruptions_bp)
    app.register_blueprint(rebooking_bp)

    # Create tables on first run
    with app.app_context():
        db.create_all()

    @app.route('/')
    def index():
        return jsonify({
            'message': 'Aircraft Network Flight Scheduler API',
            'version': '1.0',
            'status': 'running'
        })

    @app.errorhandler(404)
    def not_found(e):
        return jsonify({'error': 'Not found'}), 404

    @app.errorhandler(500)
    def server_error(e):
        app.logger.exception('Unhandled exception:')
        return jsonify({'error': 'Internal server error'}), 500

    return app

if __name__ == '__main__':
    app = create_app()
    port = int(os.environ.get('PORT', 5000))
    # Disable the reloader here to avoid repeated restarts (OneDrive file watches)
    app.run(host='0.0.0.0', port=port, debug=app.config.get('DEBUG', False), use_reloader=False)
