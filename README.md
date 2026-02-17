# AI Video Editor — Scaffold

This repository is a scaffold for an AI-powered video editor (FastAPI backend, Celery workers, AI engine, React frontend). It includes Dockerfiles and a `docker-compose.yml` for local development and a `railway.json` for deploying to Railway.

Quick start (local, requires Docker):

```powershell
cp .env.example .env
docker compose up --build
```

Backend dev (no Docker):

```powershell
cd backend
python -m venv .venv
.venv\Scripts\Activate.ps1
pip install -r requirements.txt
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

Frontend dev (no Docker):

```powershell
cd frontend
npm ci
npm start
```

Deploying to Railway:

- Create a new project on Railway and connect your GitHub repo.
- Set environment variables from `.env.example` in Railway settings.
- Railway will build using `railway.json` (uses backend Dockerfile).
