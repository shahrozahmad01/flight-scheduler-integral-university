<<<<<<< HEAD
# Aircraft Network Flight Scheduler

![Python](https://img.shields.io/badge/Python-3.14-blue)
![Flask](https://img.shields.io/badge/Flask-2.3.3-orange)
![HTML5](https://img.shields.io/badge/HTML5-%23E34F26-orange)
![JavaScript](https://img.shields.io/badge/JavaScript-ES6-yellow)

## About the Project
We developed an airline flight scheduler system for the Aircraft Network project. It includes a Flask backend, SQLite database, and a vanilla JavaScript frontend for managing flights, passengers, disruptions, and rebooking.

## Problem Statement
The app helps operations teams handle cancellations and delays, prioritize passengers, and rebook affected travelers on the best available alternative flights.

## Tech Stack
- Frontend: HTML5, CSS3, Vanilla JavaScript
- Backend: Python 3.14, Flask 2.3, SQLAlchemy
- Database: SQLite (development)
- Optional: Java scoring module

## How to Run
1. Open a terminal and navigate to `backend`
2. Install dependencies: `pip install -r requirements.txt`
3. Run seed data: `python seed_data.py`
4. Start the backend: `python app.py`
5. Open `http://localhost:5000/index.html` in your browser

## Cloud Hosting
- **Frontend**: Vercel | **Backend**: Render | **Database**: Supabase
- 📖 See [HOSTING_GUIDE.md](HOSTING_GUIDE.md) for full deployment steps.

## API Endpoints
- `GET /api/flights/` - List all flights
- `POST /api/flights/` - Create new flight
- `GET /api/passengers/` - List all passengers
- `POST /api/bookings/` - Create new booking
- `POST /api/disruptions/trigger` - Trigger disruption handling
- `GET /api/rebook/options/<passenger_id>/<flight_id>` - Get rebooking options

📖 See [ARCHITECTURE.md](ARCHITECTURE.md) for complete API reference.

## Modules
- `flights`
- `passengers`
- `bookings`
- `disruptions`
- `rebooking`
- `rebooking_engine`
- `disruption_handler`
- `notification_service`

## Screenshots
Placeholder for dashboard and disruption pages.

## Team
- Mustafa Siddiqui (2400100150)
- Md Shakib Hussain (2400103975)
- Guide: Mrs. Fareen, Assistant Professor
- Integral University, Lucknow — MCA 2025-26
