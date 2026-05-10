from flask import Blueprint, request, jsonify
from database import db
from models.passenger import Passenger
from models.booking import Booking

passengers_bp = Blueprint('passengers_bp', __name__, url_prefix='/api/passengers')


@passengers_bp.route('/', methods=['GET'])
def list_passengers():
    passengers = Passenger.query.all()
    return jsonify([p.to_dict() for p in passengers])


@passengers_bp.route('/<int:passenger_id>', methods=['GET'])
def get_passenger(passenger_id):
    passenger = Passenger.query.get(passenger_id)
    if not passenger:
        return jsonify({'error': 'Passenger not found'}), 404
    return jsonify(passenger.to_dict())


@passengers_bp.route('/', methods=['POST'])
def create_passenger():
    data = request.get_json() or {}
    required = ['name', 'email']
    if not all(key in data for key in required):
        return jsonify({'error': 'Missing required fields'}), 400

    passenger = Passenger(
        pnr=data.get('pnr', Passenger.generate_pnr()),
        name=data['name'],
        email=data['email'],
        phone=data.get('phone'),
        tier=data.get('tier', 'ECONOMY'),
        frequent_flyer=data.get('frequent_flyer', False),
        special_needs=data.get('special_needs', False),
    )
    db.session.add(passenger)
    db.session.commit()
    return jsonify(passenger.to_dict()), 201


@passengers_bp.route('/<int:passenger_id>/bookings', methods=['GET'])
def passenger_bookings(passenger_id):
    passenger = Passenger.query.get(passenger_id)
    if not passenger:
        return jsonify({'error': 'Passenger not found'}), 404
    return jsonify([booking.to_dict() for booking in passenger.bookings])
