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

Continuous Integration (GitHub Actions):

- This repo includes a workflow at `.github/workflows/ci-deploy.yml` which builds and pushes backend and frontend Docker images to GitHub Container Registry (GHCR) on push to `main`.
- To enable automatic Railway deploys, add the following repository secrets in GitHub: `RAILWAY_API_KEY` and `RAILWAY_PROJECT_ID`. The workflow will attempt to install the Railway CLI and run `railway up` when `RAILWAY_API_KEY` is present.

Required GitHub secrets for full CI->Railway:
- `RAILWAY_API_KEY` — Railway API key with deploy permissions.
- `RAILWAY_PROJECT_ID` — Railway project ID for the target project.

If you prefer Railway to build directly from the repository, connect the repo in the Railway UI and set environment variables there instead of using the CLI deploy step.

Deploying to Render

- This repository includes `render.yaml` which defines a `web` service (backend), a `worker` service (Celery worker), and a `static` site for the frontend. You can deploy using the Render dashboard by connecting your GitHub repository and selecting "Use render.yaml" during service creation.
- Render steps (UI):
	1. Go to https://render.com and sign in.
	2. Click "New" → "Web Service" and choose the repo — Render will detect `render.yaml` and offer to create services from it.
	3. For each service (backend/worker/static), add environment variables in Render (match `.env.example`) and create secrets (DATABASE_URL, REDIS_URL, S3_*, SECRET_KEY, etc.).
	4. Trigger a deploy — Render will build and run the Docker images or static build as defined.

Notes:
- For the backend and worker services Render will use `backend/Dockerfile` from the repo; make sure any large model artifacts (YOLO weights) are downloaded at runtime or provided via object storage.
- For the static site, Render will run the `buildCommand` in `render.yaml` which builds the frontend inside Render.

