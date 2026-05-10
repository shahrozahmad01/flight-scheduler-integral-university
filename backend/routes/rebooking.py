from flask import Blueprint, request, jsonify
from services.rebooking_engine import RebookingEngine
from services.notification_service import NotificationService
from models.booking import Booking
from models.flight import Flight

rebooking_bp = Blueprint('rebooking_bp', __name__, url_prefix='/api/rebook')


@rebooking_bp.route('/options/<int:passenger_id>/<int:flight_id>', methods=['GET'])
def get_options(passenger_id, flight_id):
    options = RebookingEngine.get_best_option(passenger_id, flight_id)
    return jsonify(options)


@rebooking_bp.route('/confirm', methods=['POST'])
def confirm_rebooking():
    data = request.get_json() or {}
    required = ['booking_id', 'new_flight_id']
    if not all(key in data for key in required):
        return jsonify({'error': 'Missing required fields'}), 400

    booking = RebookingEngine.rebook_passenger(data['booking_id'], data['new_flight_id'])
    if not booking:
        return jsonify({'error': 'Unable to rebook passenger'}), 500

    old_flight = Flight.query.get(booking.original_flight_id)
    new_flight = Flight.query.get(booking.flight_id)
    passenger = booking.passenger
    NotificationService.send_rebooking_confirmation(passenger, old_flight, new_flight, booking)
    return jsonify({
        'booking': booking.to_dict(),
        'new_flight': new_flight.to_dict() if new_flight else None,
    })


@rebooking_bp.route('/history/<int:passenger_id>', methods=['GET'])
def rebooking_history(passenger_id):
    bookings = Booking.query.filter_by(passenger_id=passenger_id, status='REBOOKED').all()
    return jsonify([booking.to_dict() for booking in bookings])
