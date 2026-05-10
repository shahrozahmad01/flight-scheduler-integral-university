from flask import Blueprint, request, jsonify
from database import db
from models.booking import Booking
from models.flight import Flight
from models.passenger import Passenger

bookings_bp = Blueprint('bookings_bp', __name__, url_prefix='/api/bookings')


@bookings_bp.route('/', methods=['GET'])
def list_bookings():
    bookings = Booking.query.all()
    return jsonify([b.to_dict() for b in bookings])


@bookings_bp.route('/<int:booking_id>', methods=['GET'])
def get_booking(booking_id):
    booking = Booking.query.get(booking_id)
    if not booking:
        return jsonify({'error': 'Booking not found'}), 404
    return jsonify(booking.to_dict())


@bookings_bp.route('/', methods=['POST'])
def create_booking():
    data = request.get_json() or {}
    required = ['booking_ref', 'passenger_id', 'flight_id', 'seat_number']
    if not all(key in data for key in required):
        return jsonify({'error': 'Missing required booking fields'}), 400

    flight = Flight.query.get(data['flight_id'])
    if not flight:
        return jsonify({'error': 'Flight not found'}), 404
    if flight.available_seats <= 0:
        return jsonify({'error': 'No available seats'}), 400

    booking = Booking(
        booking_ref=data['booking_ref'],
        passenger_id=data['passenger_id'],
        flight_id=data['flight_id'],
        seat_number=data['seat_number'],
        seat_class=data.get('seat_class', 'ECONOMY'),
        status='CONFIRMED'
    )
    flight.available_seats -= 1
    db.session.add(booking)
    db.session.commit()
    return jsonify(booking.to_dict()), 201


@bookings_bp.route('/<int:booking_id>/cancel', methods=['PUT'])
def cancel_booking(booking_id):
    booking = Booking.query.get(booking_id)
    if not booking:
        return jsonify({'error': 'Booking not found'}), 404
    if booking.status == 'CANCELLED':
        return jsonify({'message': 'Booking already cancelled'}), 200

    booking.status = 'CANCELLED'
    if booking.flight:
        booking.flight.available_seats += 1
    db.session.commit()
    return jsonify(booking.to_dict())
