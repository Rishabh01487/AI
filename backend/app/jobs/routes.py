"""Job endpoints: get status and latest job for project."""
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from ..database import get_db
from .. import models, schemas

router = APIRouter()


@router.get("/project/{project_id}", response_model=schemas.JobOut)
def latest_job(project_id: int, db: Session = Depends(get_db)):
    job = db.query(models.Job).filter(models.Job.project_id == project_id).order_by(models.Job.created_at.desc()).first()
    if not job:
        raise HTTPException(status_code=404, detail="No job found")
    return job


@router.get("/{job_id}", response_model=schemas.JobOut)
def get_job(job_id: int, db: Session = Depends(get_db)):
    job = db.query(models.Job).filter(models.Job.id == job_id).first()
    if not job:
        raise HTTPException(status_code=404, detail="Job not found")
    return job
