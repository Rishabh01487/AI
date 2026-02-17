"""Project CRUD and start edit endpoint."""
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from .. import models, schemas
from ..database import get_db
from ..workers.celery_app import celery_app

router = APIRouter()


@router.post("/", response_model=schemas.ProjectOut)
def create_project(payload: schemas.ProjectCreate, db: Session = Depends(get_db)):
    proj = models.Project(title=payload.title, prompt=payload.prompt, user_id=1)
    db.add(proj)
    db.commit()
    db.refresh(proj)
    return proj


@router.get("/", response_model=List[schemas.ProjectOut])
def list_projects(db: Session = Depends(get_db)):
    return db.query(models.Project).all()


@router.get("/{project_id}", response_model=schemas.ProjectOut)
def get_project(project_id: int, db: Session = Depends(get_db)):
    proj = db.query(models.Project).filter(models.Project.id == project_id).first()
    if not proj:
        raise HTTPException(status_code=404, detail="Project not found")
    return proj


@router.post("/{project_id}/start", tags=["jobs"])
def start_edit(project_id: int, db: Session = Depends(get_db)):
    proj = db.query(models.Project).filter(models.Project.id == project_id).first()
    if not proj:
        raise HTTPException(status_code=404, detail="Project not found")
    job = models.Job(project_id=project_id, status="pending")
    db.add(job)
    db.commit()
    db.refresh(job)
    # enqueue celery task
    celery_app.send_task("app.workers.tasks.process_edit_job", args=[project_id, job.id])
    proj.status = "processing"
    db.add(proj)
    db.commit()
    return {"job_id": job.id}
