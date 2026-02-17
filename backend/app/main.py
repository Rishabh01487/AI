"""FastAPI application entrypoint."""
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from .config import settings
from .database import Base, engine
from .auth import routes as auth_routes
from .projects import routes as project_routes
from .assets import routes as asset_routes
from .jobs import routes as job_routes

Base.metadata.create_all(bind=engine)

app = FastAPI(title="AI Video Editor Platform")

origins = [o.strip() for o in settings.CORS_ORIGINS.split(",")] if settings.CORS_ORIGINS else ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth_routes.router, prefix="/auth", tags=["auth"])
app.include_router(project_routes.router, prefix="/projects", tags=["projects"])
app.include_router(asset_routes.router, prefix="/assets", tags=["assets"])
app.include_router(job_routes.router, prefix="/jobs", tags=["jobs"])


@app.get("/")
def read_root():
    return {"status": "ok", "service": "ai-video-editor"}
