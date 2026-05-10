from datetime import datetime
from flask import Blueprint, request, jsonify
from database import db
from models.flight import Flight

flights_bp = Blueprint('flights_bp', __name__, url_prefix='/api/flights')


def parse_datetime(value):
    if isinstance(value, datetime):
        return value
    if not value:
        return None
    if isinstance(value, str):
        try:
            return datetime.fromisoformat(value)
        except ValueError:
            raise ValueError('Invalid datetime format')
    raise ValueError('Invalid datetime value')


@flights_bp.route('/', methods=['GET'])
def list_flights():
    status = request.args.get('status')
    query = Flight.query
    if status:
        query = query.filter_by(status=status.upper())
    flights = query.all()
    return jsonify([flight.to_dict() for flight in flights])


@flights_bp.route('/<int:flight_id>', methods=['GET'])
def get_flight(flight_id):
    flight = Flight.query.get(flight_id)
    if not flight:
        return jsonify({'error': 'Flight not found'}), 404
    return jsonify(flight.to_dict())


@flights_bp.route('/', methods=['POST'])
def create_flight():
    data = request.get_json() or {}
    required = ['flight_number', 'origin', 'destination', 'departure_time', 'arrival_time']
    if not all(key in data for key in required):
        return jsonify({'error': 'Missing required flight fields'}), 400

    try:
        departure_time = parse_datetime(data['departure_time'])
        arrival_time = parse_datetime(data['arrival_time'])
    except ValueError as exc:
        return jsonify({'error': str(exc)}), 400

    flight = Flight(
        flight_number=data['flight_number'],
        origin=data['origin'],
        destination=data['destination'],
        departure_time=departure_time,
        arrival_time=arrival_time,
        total_seats=data.get('total_seats', 180),
        available_seats=data.get('available_seats', 180),
        status=data.get('status', 'ON_TIME'),
        delay_minutes=data.get('delay_minutes', 0),
        aircraft_type=data.get('aircraft_type', 'Boeing 737'),
    )
    db.session.add(flight)
    db.session.commit()
    return jsonify(flight.to_dict()), 201


@flights_bp.route('/<int:flight_id>', methods=['PUT'])
def update_flight(flight_id):
    flight = Flight.query.get(flight_id)
    if not flight:
        return jsonify({'error': 'Flight not found'}), 404
    data = request.get_json() or {}
    for key in ['flight_number', 'origin', 'destination', 'departure_time', 'arrival_time', 'total_seats', 'available_seats', 'status', 'delay_minutes', 'aircraft_type']:
        if key in data:
            if key in ('departure_time', 'arrival_time'):
                try:
                    setattr(flight, key, parse_datetime(data[key]))
                except ValueError as exc:
                    return jsonify({'error': str(exc)}), 400
            else:
                setattr(flight, key, data[key])
    db.session.commit()
    return jsonify(flight.to_dict())


@flights_bp.route('/route/<origin>/<destination>', methods=['GET'])
def route_flights(origin, destination):
    flights = Flight.query.filter_by(origin=origin.upper(), destination=destination.upper()).all()
    return jsonify([flight.to_dict() for flight in flights])


@flights_bp.route('/stats/summary', methods=['GET'])
def flight_summary():
    flights = Flight.query.all()
    total = len(flights)
    on_time = sum(1 for f in flights if f.status == 'ON_TIME')
    delayed = sum(1 for f in flights if f.status == 'DELAYED')
    cancelled = sum(1 for f in flights if f.status == 'CANCELLED')
    total_seats = sum(f.total_seats for f in flights)
    available_seats = sum(f.available_seats for f in flights)
    return jsonify({
        'total_flights': total,
        'on_time_count': on_time,
        'delayed_count': delayed,
        'cancelled_count': cancelled,
        'total_seats': total_seats,
        'available_seats': available_seats,
    })
