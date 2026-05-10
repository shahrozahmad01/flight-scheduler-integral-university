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
You can deploy this app on a Python cloud host such as Azure App Service or Render.

### Azure App Service
1. Push the project to a GitHub repository.
2. Create a Linux Web App with Python 3.14.
3. In App Service settings, set the Startup Command to:
   `python app.py`
4. App Service will install `backend/requirements.txt` and use the Flask app as the API server.
5. Open `https://<your-app-name>.azurewebsites.net/index.html` to access the frontend.

### Render or Similar Python Host
1. Point the service to the repo branch.
2. Set the build command to:
   `cd backend && pip install -r requirements.txt`
3. Set the start command to:
   `cd backend && python app.py`
4. Visit `/index.html` on the deployed domain to load the frontend.

This project now serves the UI from the Flask app static folder and works from the same origin for API calls.

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
