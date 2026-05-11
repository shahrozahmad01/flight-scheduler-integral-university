Backend installation notes
=========================

If you're developing on Windows, `psycopg2-binary` may fail to build because the `pg_config` executable is missing.

Options to resolve locally:

- Use SQLite locally (the app falls back to SQLite when `DATABASE_URL` is not set).
- Install PostgreSQL (developer package) so `pg_config` is available on PATH, then install requirements.
- Use WSL (Ubuntu) or a Linux/macOS environment where binary wheels are available.

Quick commands:

Windows (use SQLite, no extra steps):
```
python -m pip install --user -r requirements.txt
```

Windows (if you want PostgreSQL client libs):
1. Install PostgreSQL from https://www.postgresql.org/download/windows/ (include developer headers).
2. Ensure `pg_config` is on your PATH.
3. Then run:
```
python -m pip install --user -r requirements.txt
```

Alternative (install only binary wheel if available):
```
python -m pip install --user --only-binary :all: psycopg2-binary
```

Deployment notes:
- For production with Postgres (e.g., Supabase), set `DATABASE_URL` in your environment. The app handles `postgres://` → `postgresql://` conversion.
- On Vercel, add the `DATABASE_URL` environment variable or let the app fall back to the bundled SQLite for simple demos (not recommended for production).
