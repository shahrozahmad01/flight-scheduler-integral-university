# Flight Scheduler

A simple flight management application built with Flask and Vanilla JavaScript.

## Features

- **Flights Management** - View, create, and manage flights
- **Passenger Management** - Manage passenger information  
- **Bookings** - Create and cancel flight bookings
- **Dashboard** - Quick overview of flights, passengers, and bookings

## Tech Stack

- **Frontend**: HTML5, CSS3, Vanilla JavaScript
- **Backend**: Python 3.11, Flask 2.3, SQLAlchemy
- **Database**: SQLite (local development)

## Quick Start

### Prerequisites
- Python 3.11 or higher
- Git

### Setup & Run (Windows)

```bash
# Run the automated setup script
run-local.bat
```

### Setup & Run (macOS/Linux)

```bash
# Make the script executable and run it
chmod +x run-local.sh
./run-local.sh
```

### Manual Setup

1. **Create virtual environment**
   ```bash
   python -m venv .venv
   .venv\Scripts\activate  # Windows
   source .venv/bin/activate  # macOS/Linux
   ```

2. **Install dependencies**
   ```bash
   pip install -r backend/requirements-dev.txt
   ```

3. **Initialize database**
   ```bash
   cd backend
   python seed_data.py
   cd ..
   ```

4. **Start server**
   ```bash
   cd backend
   python app.py
   cd ..
   ```

5. **Open in browser**
   ```
   http://localhost:5000/index.html
   ```

## API Endpoints

- `GET /api/flights/` - List all flights
- `POST /api/flights/` - Create a flight
- `GET /api/passengers/` - List all passengers
- `POST /api/passengers/` - Create a passenger
- `GET /api/bookings/` - List all bookings
- `POST /api/bookings/` - Create a booking

## Project Structure

```
flight-scheduler/
├── backend/                    # Flask API
│   ├── app.py                 # Main app
│   ├── config.py              # Configuration
│   ├── database.py            # Database setup
│   ├── seed_data.py           # Sample data
│   ├── requirements-dev.txt   # Dev dependencies
│   ├── models/                # Database models
│   ├── routes/                # API routes
│   └── instance/              # Local database
│
├── frontend/                   # Web interface
│   ├── index.html             # Login page
│   ├── pages/dashboard.html   # Dashboard
│   ├── js/api.js              # API client
│   └── css/                   # Styles
│
└── run-local.bat/.sh          # Quick start scripts
```

## Troubleshooting

- **Port in use**: Change `PORT=5001 python app.py`
- **Database errors**: Delete `backend/instance/flight_scheduler.db` and re-run `seed_data.py`
- **Module errors**: Reinstall dependencies: `pip install -r backend/requirements-dev.txt`

## License

Open source project for educational purposes.


## Screenshots
Placeholder for dashboard and disruption pages.

## Team
- Mustafa Siddiqui (2400100150)
- Md Shakib Hussain (2400103975)
- Guide: Mrs. Fareen, Assistant Professor
- Integral University, Lucknow — MCA 2025-26
