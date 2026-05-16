from datetime import datetime
from database import db


class Flight(db.Model):
    __tablename__ = 'flights'

    id = db.Column(db.Integer, primary_key=True)
    flight_number = db.Column(db.String(10), unique=True, nullable=False)
    origin = db.Column(db.String(3), nullable=False)
    destination = db.Column(db.String(3), nullable=False)
    departure_time = db.Column(db.DateTime, nullable=False)
    arrival_time = db.Column(db.DateTime, nullable=False)
    total_seats = db.Column(db.Integer, default=180)
    available_seats = db.Column(db.Integer, default=180)
    status = db.Column(db.String(20), default='ON_TIME')
    delay_minutes = db.Column(db.Integer, default=0)
    aircraft_type = db.Column(db.String(20), default='Boeing 737')

    bookings = db.relationship('Booking', backref='flight', lazy=True)

    def to_dict(self):
        return {
            'id': self.id,
            'flight_number': self.flight_number,
            'origin': self.origin,
            'destination': self.destination,
            'departure_time': self.departure_time.isoformat(),
            'arrival_time': self.arrival_time.isoformat(),
            'total_seats': self.total_seats,
            'available_seats': self.available_seats,
            'status': self.status,
            'delay_minutes': self.delay_minutes,
            'aircraft_type': self.aircraft_type,
        }

    def __repr__(self):
        return f'<Flight {self.flight_number} {self.origin}-{self.destination}>'

    @classmethod
    def get_by_flight_number(cls, num):
        return cls.query.filter_by(flight_number=num).first()
