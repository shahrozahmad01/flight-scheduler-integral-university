# 🚀 Hosting Guide for Aircraft Network Flight Scheduler

## Overview
This guide provides step-by-step instructions to host the Aircraft Network Flight Scheduler application on cloud platforms. The application consists of:
- **Frontend**: Static HTML/CSS/JS hosted on Vercel
- **Backend**: Flask API (Python 3.11) hosted on Render
- **Database**: PostgreSQL hosted on Supabase

## Prerequisites
- GitHub repository: https://github.com/shahrozahmad01/flight-scheduler-integral-university.git
- Vercel account
- Render account
- Supabase account

---

## Database Setup: Supabase

### Step 1: Create Supabase Project
1. Go to [Supabase](https://supabase.com).
2. Click **New Project**.
3. Configure:
   - **Name**: flight-scheduler-db
   - **Database Password**: Set a strong password
   - **Region**: Select nearest region
4. Click **Create new project**.

### Step 2: Get Connection Details
1. In Supabase dashboard, go to **Settings** > **Database**.
2. Copy the **Connection string** (it looks like: `postgresql://postgres:[password]@db.[project-ref].supabase.co:5432/postgres`)
3. Note the connection string for later use.

### Step 3: Run Migrations (Optional)
If you want to pre-populate data, you can run the seed script locally against Supabase by setting `DATABASE_URL` environment variable.

---

## Backend Deployment: Render

### Step 1: Prepare Repository
1. Ensure your code is pushed to GitHub.
2. Verify `backend/requirements.txt` includes all dependencies (including `psycopg2-binary`).

### Step 2: Create Render Service
1. Go to [Render Dashboard](https://dashboard.render.com).
2. Click **New** > **Web Service**.
3. Connect your GitHub repo: `shahrozahmad01/flight-scheduler-integral-university`
4. Configure:
   - **Name**: flight-scheduler-backend
   - **Environment**: Python 3
   - **Build Command**: `cd backend && pip install -r requirements.txt`
   - **Start Command**: `cd backend && gunicorn --bind 0.0.0.0:$PORT app:create_app()`

### Step 3: Environment Variables
1. In Render dashboard, add these environment variables:
   - `DATABASE_URL`: Your Supabase connection string
   - `SECRET_KEY`: A random string (e.g., `your-secret-key-here`)
   - `FLASK_ENV`: `production`

### Step 4: Deploy
1. Click **Create Web Service**.
2. Render will build and deploy automatically.
3. Note the backend URL (e.g., `https://flight-scheduler-backend.onrender.com`)

---

## Frontend Deployment: Vercel

### Step 1: Prepare Frontend
The frontend is static files in `frontend/`. We need to configure it to call the Render backend.

1. After Render deployment, get your backend URL (e.g., `https://flight-scheduler-backend.onrender.com`)
2. Update `frontend/js/api.js`:
   - Change `const BASE_URL = 'https://your-render-backend-url.onrender.com/api';` to `const BASE_URL = 'https://your-actual-render-url.onrender.com/api';`
3. Commit and push the change to trigger Vercel redeployment.

### Step 2: Deploy to Vercel
1. Go to [Vercel Dashboard](https://vercel.com).
2. Click **New Project**.
3. Import your GitHub repo: `shahrozahmad01/flight-scheduler-integral-university`
4. Configure:
   - **Framework Preset**: Other
   - **Root Directory**: `frontend`
   - **Build Command**: (leave empty for static)
   - **Output Directory**: `.` (root of frontend)
5. Click **Deploy**.

### Step 3: Update API Calls
After deployment, update `frontend/js/api.js` with the actual Render backend URL and push to GitHub for auto-deployment.

---

## General Deployment Steps

### 1. Environment Variables Summary
- **Supabase**: `DATABASE_URL` (connection string)
- **Render**: `DATABASE_URL`, `SECRET_KEY`, `FLASK_ENV`
- **Vercel**: No env vars needed (static site)

### 2. Database Migration
For production:
1. Supabase handles schema creation.
2. Run seed data locally if needed: `DATABASE_URL=your-supabase-url python backend/seed_data.py`

### 3. CORS Configuration
The Flask app has CORS enabled for all origins. For production, restrict to your Vercel domain.

### 4. HTTPS and Security
- All platforms (Vercel, Render, Supabase) provide HTTPS by default.
- Use environment variables for secrets.
- Configure CORS properly.

### 5. Monitoring
- **Render**: Check logs in Service > Logs tab
- **Vercel**: Check deployments and logs in dashboard
- **Supabase**: Monitor database in dashboard

---

## Troubleshooting

### Common Issues:
1. **Database connection failed**: Check `DATABASE_URL` format and Supabase credentials.
2. **CORS errors**: Ensure backend allows requests from Vercel domain.
3. **Static files not loading**: Vercel serves from `frontend/` directory.
4. **Port issues**: Render assigns `$PORT`, use gunicorn.

### Logs:
- **Render**: Service > Logs
- **Vercel**: Project > Deployments > Logs
- **Supabase**: Project > Database > Logs

---

## Cost Estimation
- **Supabase**: Free tier (500MB DB), paid ~$25/month for more
- **Render**: Free tier (750 hours/month), paid ~$7/month
- **Vercel**: Free tier (unlimited static sites), paid for advanced features

---

## Final Steps
1. Test the full stack: Frontend (Vercel) → Backend (Render) → Database (Supabase)
2. Update DNS if using custom domains.
3. Set up CI/CD for automatic deployments.

For questions, refer to the README.md or contact the development team.