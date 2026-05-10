from models.booking import Booking
from models.flight import Flight
from models.passenger import Passenger
from models.disruption import Disruption


class NotificationService:
    notifications_log = []

    @classmethod
    def send_disruption_alert(cls, passenger, flight, disruption):
        status_text = 'CANCELLED' if disruption.disruption_type == 'CANCELLATION' else f'DELAYED by {flight.delay_minutes} mins'
        message = (
            f"Dear {passenger.name}, your flight {flight.flight_number} from {flight.origin} "
            f"to {flight.destination} scheduled at {flight.departure_time.strftime('%Y-%m-%d %H:%M')} "
            f"has been {status_text}. Our team is working to rebook you. PNR: {passenger.pnr}"
        )
        print(message)
        cls.notifications_log.append(message)
        return message

    @classmethod
    def send_rebooking_confirmation(cls, passenger, old_flight, new_flight, booking):
        message = (
            f"Dear {passenger.name}, you have been rebooked on flight {new_flight.flight_number} "
            f"departing {new_flight.origin} at {new_flight.departure_time.strftime('%Y-%m-%d %H:%M')}. "
            f"New seat: {booking.seat_number}. Booking ref: {booking.booking_ref}"
        )
        print(message)
        cls.notifications_log.append(message)
        return message

    @classmethod
    def send_bulk_notifications(cls, flight_id, disruption):
        messages = []
        flight = Flight.query.get(flight_id)
        if not flight:
            return messages

        bookings = Booking.query.filter_by(flight_id=flight_id, status='CONFIRMED').all()
        for booking in bookings:
            msg = cls.send_disruption_alert(booking.passenger, flight, disruption)
            messages.append(msg)
        return messages

    @classmethod
    def get_log(cls):
        return cls.notifications_log
