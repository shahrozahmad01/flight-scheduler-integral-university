import logging
from datetime import datetime, timedelta

from database import db
from models.flight import Flight
from models.passenger import Passenger
from models.booking import Booking

logger = logging.getLogger(__name__)


class RebookingEngine:

    @staticmethod
    def find_alternatives(disrupted_flight_id):
        try:
            disrupted = Flight.query.get(disrupted_flight_id)
            if not disrupted:
                return []

            window_end = disrupted.departure_time + timedelta(hours=24)
            return Flight.query.filter(
                Flight.origin == disrupted.origin,
                Flight.destination == disrupted.destination,
                Flight.id != disrupted_flight_id,
                Flight.departure_time >= disrupted.departure_time,
                Flight.departure_time <= window_end,
                Flight.available_seats > 0,
                Flight.status != 'CANCELLED'
            ).all()
        except Exception as exc:
            logger.exception('Unable to find alternatives')
            return []

    @staticmethod
    def score_option(flight, passenger, booking):
        try:
            delay_minutes = max(0, int(flight.delay_minutes or 0))
            if delay_minutes < 60:
                delay_score = 100
            elif delay_minutes < 120:
                delay_score = 70
            elif delay_minutes < 240:
                delay_score = 40
            else:
                delay_score = 10

            connection_score = 100
            complexity_score = 100
            priority_score = 20
            if passenger.special_needs or passenger.frequent_flyer:
                priority_score = 100
            elif passenger.tier == 'BUSINESS':
                priority_score = 70
            elif passenger.tier == 'FIRST':
                priority_score = 60
            elif passenger.tier == 'ECONOMY':
                priority_score = 30

            if booking.seat_class == 'ECONOMY':
                cost_score = 100
            elif booking.seat_class == 'BUSINESS':
                cost_score = 80
            else:
                cost_score = 60
            score = (
                delay_score * 0.40
                + connection_score * 0.25
                + complexity_score * 0.15
                + priority_score * 0.10
                + cost_score * 0.10
            )
            return round(min(max(score, 0), 100), 2)
        except Exception:
            logger.exception('Failed to calculate score')
            return 0.0

    @classmethod
    def get_best_option(cls, passenger_id, disrupted_flight_id):
        try:
            passenger = Passenger.query.get(passenger_id)
            booking = Booking.query.filter_by(passenger_id=passenger_id, flight_id=disrupted_flight_id, status='CONFIRMED').first()
            if not passenger or not booking:
                return []

            alternatives = cls.find_alternatives(disrupted_flight_id)
            scored = []
            for flight in alternatives:
                score = cls.score_option(flight, passenger, booking)
                scored.append({
                    'flight': flight.to_dict(),
                    'score': score,
                })

            scored.sort(key=lambda item: item['score'], reverse=True)
            return scored[:3]
        except Exception:
            logger.exception('Failed to get best options')
            return []

    @staticmethod
    def rebook_passenger(booking_id, new_flight_id):
        try:
            booking = Booking.query.get(booking_id)
            new_flight = Flight.query.get(new_flight_id)
            if not booking or not new_flight:
                raise ValueError('Booking or flight not found')
            if new_flight.available_seats <= 0:
                raise ValueError('No available seats')

            booking.original_flight_id = booking.flight_id
            booking.flight_id = new_flight_id
            booking.status = 'REBOOKED'
            new_flight.available_seats -= 1
            db.session.commit()
            return booking
        except Exception:
            db.session.rollback()
            logger.exception('Rebooking failed')
            return None
