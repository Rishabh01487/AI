"""Celery tasks for processing edit jobs."""
import os
import tempfile
import uuid
from celery.utils.log import get_task_logger
from .celery_app import celery_app
from ..app.database import SessionLocal
from ..app import models
from ..app.config import settings
from ..app.ai_engine import scene_detector, object_tagger, prompt_parser, shot_selector, renderer
import boto3

logger = get_task_logger(__name__)


def s3_client():
    import botocore
    return boto3.client(
        "s3",
        endpoint_url=settings.S3_ENDPOINT,
        aws_access_key_id=settings.S3_ACCESS_KEY,
        aws_secret_access_key=settings.S3_SECRET_KEY,
        config=botocore.client.Config(signature_version="s3v4"),
    )


@celery_app.task(name="app.workers.tasks.process_edit_job", bind=True)
def process_edit_job(self, project_id: int, job_id: int):
    db = SessionLocal()
    try:
        job = db.query(models.Job).get(job_id)
        project = db.query(models.Project).get(project_id)
        if not job or not project:
            logger.error("Job or project not found")
            return
        job.status = "processing"
        db.add(job)
        db.commit()

        assets = db.query(models.Asset).filter(models.Asset.project_id == project_id).all()
        tmpdir = tempfile.mkdtemp()
        local_files = []
        client = s3_client()
        for a in assets:
            local_path = os.path.join(tmpdir, os.path.basename(a.s3_key))
            try:
                client.download_file(settings.S3_BUCKET, a.s3_key, local_path)
                local_files.append({"path": local_path, "s3_key": a.s3_key, "media_type": a.media_type})
            except Exception as e:
                logger.exception("Failed to download asset %s: %s", a.s3_key, e)

        # Analyze assets
        scenes_with_tags = []
        for f in local_files:
            if f["media_type"].startswith("video"):
                scenes = scene_detector.detect_scenes(f["path"]) or []
                tags = object_tagger.tag_video(f["path"]) or []
                scenes_with_tags.append({"file": f, "scenes": scenes, "tags": tags})
            else:
                tags = object_tagger.tag_image(f["path"]) or []
                scenes_with_tags.append({"file": f, "scenes": [(0, None)], "tags": tags})

        directives = prompt_parser.parse(project.prompt or "")
        selected = shot_selector.select_shots(scenes_with_tags, directives.get("duration", 30), directives.get("include", []), directives.get("exclude", []))

        output_path = os.path.join(tmpdir, f"output_{uuid.uuid4().hex}.mp4")
        renderer.render(selected, output_path, directives)

        # upload result
        out_key = f"projects/{project_id}/output/{os.path.basename(output_path)}"
        client.upload_file(output_path, settings.S3_BUCKET, out_key)

        job.status = "completed"
        job.output_key = out_key
        project.status = "completed"
        project.output_video_key = out_key
        db.add(job)
        db.add(project)
        db.commit()

    except Exception as exc:
        logger.exception("Processing failed: %s", exc)
        job = db.query(models.Job).get(job_id)
        if job:
            job.status = "failed"
            job.error = str(exc)
            db.add(job)
            db.commit()
    finally:
        db.close()
