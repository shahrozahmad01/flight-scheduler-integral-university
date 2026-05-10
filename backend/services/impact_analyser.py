import logging
from datetime import timedelta
from math import ceil

from models.flight import Flight
from models.booking import Booking
from models.passenger import Passenger

logger = logging.getLogger(__name__)


class ImpactAnalyser:

    @staticmethod
    def analyse_passenger(booking_id):
        try:
            booking = Booking.query.get(booking_id)
            if not booking:
                return {}

            passenger = booking.passenger
            flight = booking.flight
            has_connection = False
            next_booking = Booking.query.filter(
                Booking.passenger_id == passenger.id,
                Booking.id != booking.id,
                Booking.status == 'CONFIRMED'
            ).join(Flight, Booking.flight).filter(
                Flight.departure_time >= flight.arrival_time,
                Flight.departure_time <= flight.arrival_time + timedelta(hours=3)
            ).first()
            if next_booking:
                has_connection = True

            priority_score = 1
            if passenger.special_needs or passenger.frequent_flyer or has_connection:
                priority_score = 10
            elif passenger.tier == 'BUSINESS':
                priority_score = 7
            elif passenger.tier == 'FIRST':
                priority_score = 6
            else:
                priority_score = 3

            if passenger.special_needs or passenger.frequent_flyer or has_connection:
                impact_level = 'HIGH'
            elif passenger.tier in ('BUSINESS', 'FIRST'):
                impact_level = 'MEDIUM'
            else:
                impact_level = 'LOW'

            recommended_action = 'WAIT'
            if impact_level == 'HIGH':
                recommended_action = 'IMMEDIATE_REBOOK'
            elif impact_level == 'MEDIUM':
                recommended_action = 'REBOOK_AVAILABLE'

            return {
                'passenger': passenger.to_dict(),
                'booking': booking.to_dict(),
                'flight': flight.to_dict(),
                'impact_level': impact_level,
                'has_connection': has_connection,
                'priority_score': priority_score,
                'recommended_action': recommended_action,
            }
        except Exception:
            logger.exception('Error analysing passenger')
            return {}

    @staticmethod
    def analyse_flight_disruption(flight_id):
        try:
            bookings = Booking.query.filter_by(flight_id=flight_id, status='CONFIRMED').all()
            passenger_analyses = []
            counts = {'HIGH': 0, 'MEDIUM': 0, 'LOW': 0}
            for booking in bookings:
                data = ImpactAnalyser.analyse_passenger(booking.id)
                if data:
                    passenger_analyses.append(data)
                    counts[data['impact_level']] += 1

            total = len(bookings)
            return {
                'flight_number': bookings[0].flight.flight_number if bookings else None,
                'total_affected': total,
                'high_priority': counts['HIGH'],
                'medium_priority': counts['MEDIUM'],
                'low_priority': counts['LOW'],
                'estimated_recovery_time_mins': ceil(total * 1.5),
                'passengers': passenger_analyses,
            }
        except Exception:
            logger.exception('Error analysing flight disruption')
            return {}
