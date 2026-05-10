from flask import Flask, jsonify
from flask_cors import CORS
import os

from config import DevelopmentConfig
from database import db, init_db
from routes.flights import flights_bp
from routes.passengers import passengers_bp
from routes.bookings import bookings_bp
from routes.disruptions import disruptions_bp
from routes.rebooking import rebooking_bp


def create_app():
    app = Flask(__name__, static_folder='../frontend', static_url_path='')
    app.config.from_object(DevelopmentConfig)
    CORS(app)
    init_db(app)
    app.register_blueprint(flights_bp)
    app.register_blueprint(passengers_bp)
    app.register_blueprint(bookings_bp)
    app.register_blueprint(disruptions_bp)
    app.register_blueprint(rebooking_bp)

    @app.route('/')
    def index():
        return jsonify({
            'message': 'Aircraft Network Flight Scheduler API',
            'version': '1.0',
            'status': 'running'
        })

    @app.errorhandler(404)
    def not_found(error):
        return jsonify({'error': 'Not found'}), 404

    @app.errorhandler(500)
    def server_error(error):
        return jsonify({'error': 'Internal server error'}), 500

    return app


if __name__ == '__main__':
    app = create_app()
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=os.environ.get('FLASK_ENV') != 'production')
