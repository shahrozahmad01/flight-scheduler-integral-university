# 🚀 Hosting Guide for Aircraft Network Flight Scheduler

## Overview
This guide provides step-by-step instructions to host the Aircraft Network Flight Scheduler application on cloud platforms. The application consists of:
- **Backend**: Flask API (Python 3.14)
- **Frontend**: Static HTML/CSS/JS served by Flask
- **Database**: SQLite (development) or PostgreSQL (production recommended)

## Prerequisites
- GitHub repository: https://github.com/shahrozahmad01/flight-scheduler-integral-university.git
- Python 3.14 environment
- Cloud account (Azure, Render, etc.)

---

## Option 1: Azure App Service (Recommended)

### Step 1: Prepare Your Repository
1. Ensure your code is pushed to GitHub.
2. Verify `backend/requirements.txt` includes all dependencies.
3. The Flask app is configured to serve static files from `frontend/`.

### Step 2: Create Azure App Service
1. Go to [Azure Portal](https://portal.azure.com).
2. Click **Create a resource** > **Web App**.
3. Configure:
   - **Subscription**: Your Azure subscription
   - **Resource Group**: Create new or select existing
   - **Name**: Unique app name (e.g., `flight-scheduler-2025`)
   - **Publish**: Code
   - **Runtime stack**: Python 3.14
   - **Operating System**: Linux
   - **Region**: Select nearest region
4. Click **Next: Deployment**.
5. Enable **Continuous deployment** and connect to your GitHub repo.
6. Select repository: `shahrozahmad01/flight-scheduler-integral-university`
7. Branch: `master`
8. Click **Next: Networking** (leave defaults).
9. Click **Review + create** > **Create**.

### Step 3: Configure App Service
1. Go to your App Service in Azure Portal.
2. Under **Settings** > **Configuration**:
   - Add application settings if needed (e.g., environment variables).
3. Under **Deployment** > **Deployment Center**:
   - Ensure GitHub integration is set up.
4. Under **Settings** > **General settings**:
   - **Startup Command**: `python backend/app.py`
   - **Stack settings**: Python 3.14

### Step 4: Deploy
1. Push any changes to GitHub (deployment is automatic).
2. Monitor deployment logs in **Deployment Center** > **Logs**.
3. Once deployed, visit `https://<your-app-name>.azurewebsites.net/index.html`

### Step 5: Database Setup (Production)
For production, switch to PostgreSQL:
1. Create Azure Database for PostgreSQL.
2. Update `backend/config.py` to use PostgreSQL URI.
3. Add connection string to App Service environment variables.

---

## Option 2: Render (Free Tier Available)

### Step 1: Prepare Repository
1. Ensure code is on GitHub.
2. Create a `render.yaml` file in root (optional for advanced config).

### Step 2: Create Render Service
1. Go to [Render Dashboard](https://dashboard.render.com).
2. Click **New** > **Web Service**.
3. Connect your GitHub repo: `shahrozahmad01/flight-scheduler-integral-university`
4. Configure:
   - **Name**: flight-scheduler
   - **Environment**: Python 3
   - **Build Command**: `cd backend && pip install -r requirements.txt`
   - **Start Command**: `cd backend && python app.py`

### Step 3: Environment Variables
1. In Render dashboard, add environment variables if needed.
2. For production DB, add DATABASE_URL.

### Step 4: Deploy
1. Click **Create Web Service**.
2. Render will build and deploy automatically.
3. Visit the provided URL + `/index.html`

---

## Option 3: Railway

### Step 1: Connect Repository
1. Go to [Railway](https://railway.app).
2. Click **New Project** > **Deploy from GitHub**.
3. Connect repo: `shahrozahmad01/flight-scheduler-integral-university`

### Step 2: Configure
1. Railway auto-detects Python.
2. Set **Root Directory**: `backend`
3. **Start Command**: `python app.py`
4. Add environment variables if needed.

### Step 3: Deploy
1. Railway deploys automatically.
2. Get the domain and visit `/index.html`

---

## General Deployment Steps

### 1. Environment Variables
Add these in your cloud platform:
- `FLASK_ENV=production`
- `SECRET_KEY=<random-string>`
- `DATABASE_URL=<if using external DB>`

### 2. Database Migration
For production:
1. Use PostgreSQL instead of SQLite.
2. Run migrations: `flask db upgrade` (if using Flask-Migrate).

### 3. Static Files
The Flask app serves frontend files. Ensure `static_url_path=''` in `app.py`.

### 4. HTTPS and Security
- Enable HTTPS in your cloud provider.
- Use environment variables for secrets.
- Configure CORS if needed.

### 5. Monitoring
- Check logs in Azure/Render dashboard.
- Set up alerts for errors.

---

## Troubleshooting

### Common Issues:
1. **Module not found**: Ensure all dependencies in `requirements.txt`.
2. **Port issues**: Flask runs on port 5000, but cloud may assign different.
3. **Static files not loading**: Check `static_folder` path in `app.py`.
4. **Database errors**: Ensure DB URI is correct.

### Logs:
- Azure: App Service > Logs
- Render: Service > Logs tab

---

## Cost Estimation
- **Azure App Service**: ~$10-50/month (Basic tier)
- **Render**: Free tier available, paid ~$7/month
- **Railway**: Free tier, paid ~$5/month

---

## Final Steps
1. Test the deployed app.
2. Update DNS if using custom domain.
3. Set up CI/CD for automatic deployments.

For questions, refer to the README.md or contact the development team.