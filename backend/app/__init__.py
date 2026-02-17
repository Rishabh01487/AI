"""Backend application package initializer."""
from fastapi import FastAPI

def create_app() -> FastAPI:
    app = FastAPI(title="AI Video Editor Platform")
    return app
