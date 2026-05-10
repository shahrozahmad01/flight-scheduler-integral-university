from datetime import datetime, timedelta
import random

from app import create_app
from database import db
from models.flight import Flight
from models.passenger import Passenger
from models.booking import Booking
from models.disruption import Disruption


def seed():
    app = create_app()
    with app.app_context():
        db.drop_all()
        db.create_all()

        airports = ['DEL', 'BOM', 'BLR', 'MAA', 'CCU', 'HYD', 'GOI']
        airlines = ['AI', '6E', 'SG', 'UK']
        flights = []
        now = datetime.now()

        sample_routes = [
            ('DEL', 'BOM', 2),
            ('BOM', 'BLR', 2.5),
            ('BLR', 'MAA', 2),
            ('MAA', 'CCU', 2.5),
            ('HYD', 'GOI', 1.5),
            ('DEL', 'HYD', 2),
            ('BOM', 'GOI', 1.75),
        ]

        for idx, route in enumerate(sample_routes[:10]):
            origin, destination, hours = route
            flight_no = f"{airlines[idx % len(airlines)]}-{100 + idx}"
            status = 'ON_TIME'
            delay = 0
            if idx in (2, 5, 8):
                status = 'DELAYED'
                delay = 45
            elif idx in (3, 9):
                status = 'CANCELLED'
            departure = now + timedelta(hours=idx * 2)
            arrival = departure + timedelta(hours=hours)
            available = random.randint(120, 180)
            flight = Flight(
                flight_number=flight_no,
                origin=origin,
                destination=destination,
                departure_time=departure,
                arrival_time=arrival,
                total_seats=180,
                available_seats=available,
                status=status,
                delay_minutes=delay,
                aircraft_type='Boeing 737',
            )
            flights.append(flight)
            db.session.add(flight)

        passengers_data = [
            ('Arjun Sharma', 'arjun.sharma@example.com', '+919876543210'),
            ('Priya Patel', 'priya.patel@example.com', '+919812345678'),
            ('Rohit Kumar', 'rohit.kumar@example.com', '+919898765432'),
            ('Sunita Verma', 'sunita.verma@example.com', '+919987650123'),
            ('Mohammed Iqbal', 'mohammed.iqbal@example.com', '+919945612378'),
            ('Anjali Singh', 'anjali.singh@example.com', '+919976543210'),
            ('Vikram Mehta', 'vikram.mehta@example.com', '+919812347890'),
            ('Kavya Nair', 'kavya.nair@example.com', '+919834567890'),
            ('Rahul Gupta', 'rahul.gupta@example.com', '+919812300456'),
            ('Deepika Rao', 'deepika.rao@example.com', '+919898700123'),
            ('Amit Joshi', 'amit.joshi@example.com', '+919987610234'),
            ('Pooja Mishra', 'pooja.mishra@example.com', '+919876512345'),
            ('Sanjay Chopra', 'sanjay.chopra@example.com', '+919845612378'),
            ('Rekha Sinha', 'rekha.sinha@example.com', '+919812399876'),
            ('Kartik Iyer', 'kartik.iyer@example.com', '+919876509876'),
            ('Meera Pillai', 'meera.pillai@example.com', '+919845678901'),
            ('Suresh Reddy', 'suresh.reddy@example.com', '+919812345901'),
            ('Ananya Bose', 'ananya.bose@example.com', '+919876543901'),
            ('Rajesh Tiwari', 'rajesh.tiwari@example.com', '+919898765901'),
            ('Fatima Khan', 'fatima.khan@example.com', '+919987654321'),
        ]

        passengers = []
        for idx, (name, email, phone) in enumerate(passengers_data):
            passenger = Passenger(
                pnr=Passenger.generate_pnr(),
                name=name,
                email=email,
                phone=phone,
                tier='ECONOMY' if idx % 3 != 0 else 'BUSINESS',
                frequent_flyer=(idx in (1, 4, 7, 12, 18)),
                special_needs=(idx in (3, 11)),
            )
            passengers.append(passenger)
            db.session.add(passenger)

        db.session.commit()

        available_seat_numbers = ['12A', '14B', '22C', '10D', '9F', '18A', '20B', '15C', '7D', '3F']
        seat_classes = ['ECONOMY', 'BUSINESS']

        for idx in range(30):
            passenger = passengers[idx % len(passengers)]
            flight = flights[idx % len(flights)]
            booking = Booking(
                booking_ref=f'BK{1000 + idx}',
                passenger_id=passenger.id,
                flight_id=flight.id,
                seat_number=random.choice(available_seat_numbers),
                seat_class=random.choice(seat_classes),
                status='CONFIRMED',
            )
            flight.available_seats = max(0, flight.available_seats - 1)
            db.session.add(booking)

        disruption1 = Disruption(
            flight_id=flights[3].id,
            disruption_type='CANCELLATION',
            reason='Engine maintenance required',
            passengers_affected=Booking.query.filter_by(flight_id=flights[3].id, status='CONFIRMED').count(),
            resolved=False,
        )
        disruption2 = Disruption(
            flight_id=flights[2].id,
            disruption_type='DELAY',
            reason='Technical issue',
            passengers_affected=Booking.query.filter_by(flight_id=flights[2].id, status='CONFIRMED').count(),
            resolved=False,
        )
        db.session.add(disruption1)
        db.session.add(disruption2)

        db.session.commit()
        print('Database seeded successfully!')


if __name__ == '__main__':
    seed()
