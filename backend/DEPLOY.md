Deployment notes (Vercel / Heroku)
=================================

Environment variables
- `DATABASE_URL`: full database URL for production (e.g., Supabase). The app handles `postgres://`→`postgresql://` conversion.
- `SECRET_KEY`: Flask secret key.
- `FLASK_ENV`: `production` or `development` (defaults to `development`).
- `CORS_ORIGINS`: comma-separated allowed origins for CORS.

Vercel
- Build: Vercel runs on Node by default; to deploy this Flask app use the "Vercel for Git" setup with a Python runtime, or deploy only the frontend and host the backend separately (recommended).
- If deploying as a Serverless Function, adapt `app.py` into an entrypoint supported by the platform.

Heroku
- Set `buildpacks`: `heroku/python`.
- Add env vars (`DATABASE_URL`, `SECRET_KEY`, `FLASK_ENV=production`).
- Procfile example:
```
web: gunicorn app:app
```

Notes
- For simple demos you may omit `DATABASE_URL` and the app will use the local SQLite fallback (not suitable for production).
- Ensure you set `DATABASE_URL` to a valid Postgres URL in production.
