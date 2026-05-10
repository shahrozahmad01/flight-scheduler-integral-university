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
The application is designed for a modern cloud architecture:

- **Frontend**: Hosted on Vercel (static site)
- **Backend**: Hosted on Render (Flask API)
- **Database**: Hosted on Supabase (PostgreSQL)

### Quick Setup:
1. **Database**: Create Supabase project and get connection string
2. **Backend**: Deploy to Render with `DATABASE_URL` env var
3. **Frontend**: Deploy to Vercel, update API base URL to Render backend

📖 **Detailed Hosting Guide**: See [HOSTING_GUIDE.md](HOSTING_GUIDE.md) for comprehensive step-by-step instructions.

## API Endpoints
- `GET /api/flights/`
- `POST /api/flights/`
- `GET /api/passengers/`
- `POST /api/bookings/`
- `POST /api/disruptions/trigger`
- `GET /api/rebook/options/<passenger_id>/<flight_id>`
- `POST /api/rebook/confirm`

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
=======
# flight-scheduler-integral-university
>>>>>>> 0a1382e51ee52cfccf36d1cca5af5f8240b70bd8
