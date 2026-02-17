"""Asset endpoints: generate presigned URLs and confirm upload."""
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
import boto3
from botocore.client import Config
from ..database import get_db
from .. import models, schemas
from ..config import settings
import uuid

router = APIRouter()


def s3_client():
    return boto3.client(
        "s3",
        endpoint_url=settings.S3_ENDPOINT,
        aws_access_key_id=settings.S3_ACCESS_KEY,
        aws_secret_access_key=settings.S3_SECRET_KEY,
        config=Config(signature_version="s3v4"),
    )


@router.post("/presign")
def presign(filename: str, content_type: str = "application/octet-stream"):
    key = f"uploads/{uuid.uuid4().hex}_{filename}"
    client = s3_client()
    try:
        url = client.generate_presigned_url(
            ClientMethod="put_object",
            Params={"Bucket": settings.S3_BUCKET, "Key": key, "ContentType": content_type},
            ExpiresIn=3600,
        )
        return {"url": url, "key": key}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/confirm", response_model=schemas.AssetOut)
def confirm_asset(payload: schemas.AssetCreate, db: Session = Depends(get_db)):
    proj = db.query(models.Project).filter(models.Project.id == payload.project_id).first()
    if not proj:
        raise HTTPException(status_code=404, detail="Project not found")
    asset = models.Asset(project_id=payload.project_id, s3_key=payload.s3_key, media_type=payload.media_type or "video")
    db.add(asset)
    db.commit()
    db.refresh(asset)
    return asset
