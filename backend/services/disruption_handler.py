import logging

from database import db
from models.flight import Flight
from models.booking import Booking
from models.disruption import Disruption

logger = logging.getLogger(__name__)


class DisruptionHandler:

    @staticmethod
    def trigger_disruption(flight_id, disruption_type, reason, delay_minutes=0):
        try:
            flight = Flight.query.get(flight_id)
            if not flight:
                raise ValueError('Flight not found')

            if disruption_type == 'CANCELLATION':
                flight.status = 'CANCELLED'
                flight.delay_minutes = 0
            else:
                flight.status = 'DELAYED'
                flight.delay_minutes = delay_minutes

            affected = Booking.query.filter_by(flight_id=flight_id, status='CONFIRMED').all()
            disruption = Disruption(
                flight_id=flight_id,
                disruption_type=disruption_type,
                reason=reason,
                passengers_affected=len(affected)
            )
            db.session.add(disruption)
            db.session.commit()
            return disruption
        except Exception:
            db.session.rollback()
            logger.exception('Could not trigger disruption')
            return None

    @staticmethod
    def get_affected_passengers(flight_id):
        try:
            bookings = Booking.query.filter_by(flight_id=flight_id, status='CONFIRMED').all()
            results = []
            for booking in bookings:
                passenger = booking.passenger
                results.append({
                    'booking_id': booking.id,
                    'name': passenger.name,
                    'email': passenger.email,
                    'pnr': passenger.pnr,
                    'seat_class': booking.seat_class,
                    'seat_number': booking.seat_number,
                })
            return results
        except Exception:
            logger.exception('Unable to get affected passengers')
            return []

    @staticmethod
    def resolve_disruption(disruption_id):
        try:
            disruption = Disruption.query.get(disruption_id)
            if not disruption:
                raise ValueError('Disruption not found')

            resolved_count = Booking.query.filter_by(flight_id=disruption.flight_id, status='REBOOKED').count()
            disruption.resolved = True
            disruption.passengers_rebooked = resolved_count
            db.session.commit()
            return disruption
        except Exception:
            db.session.rollback()
            logger.exception('Could not resolve disruption')
            return None
