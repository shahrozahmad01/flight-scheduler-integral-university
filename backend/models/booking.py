from datetime import datetime
from database import db


class Booking(db.Model):
    __tablename__ = 'bookings'

    id = db.Column(db.Integer, primary_key=True)
    booking_ref = db.Column(db.String(8), unique=True, nullable=False)
    passenger_id = db.Column(db.Integer, db.ForeignKey('passengers.id'), nullable=False)
    flight_id = db.Column(db.Integer, db.ForeignKey('flights.id'), nullable=False)
    seat_number = db.Column(db.String(5))
    seat_class = db.Column(db.String(20), default='ECONOMY')
    status = db.Column(db.String(20), default='CONFIRMED')
    original_flight_id = db.Column(db.Integer, nullable=True)
    booking_date = db.Column(db.DateTime, default=datetime.utcnow)
    check_in = db.Column(db.Boolean, default=False)

    def to_dict(self):
        return {
            'id': self.id,
            'booking_ref': self.booking_ref,
            'passenger_id': self.passenger_id,
            'flight_id': self.flight_id,
            'seat_number': self.seat_number,
            'seat_class': self.seat_class,
            'status': self.status,
            'original_flight_id': self.original_flight_id,
            'booking_date': self.booking_date.isoformat(),
            'check_in': self.check_in,
            'passenger_name': self.passenger.name if self.passenger else None,
            'flight_number': self.flight.flight_number if self.flight else None,
        }

    def __repr__(self):
        return f'<Booking {self.booking_ref} passenger={self.passenger_id} flight={self.flight_id}>'
