"""Object tagging using YOLOv8-nano (ultralytics) with lightweight fallback."""
from typing import List
import os


MODEL_PATH = os.path.join(os.path.dirname(__file__), "yolov8n.pt")


def _load_model():
    try:
        from ultralytics import YOLO
        if os.path.exists(MODEL_PATH):
            return YOLO(MODEL_PATH)
        # model will be cached to disk when first downloaded
        return YOLO("yolov8n.pt")
    except Exception:
        return None


def tag_image(path: str) -> List[str]:
    model = _load_model()
    if not model:
        return []
    try:
        res = model(path)
        labels = set()
        for r in res:
            for box in r.boxes:
                labels.add(model.names[int(box.cls)])
        return list(labels)
    except Exception:
        return []


def tag_video(path: str, sample_rate: int = 2) -> List[str]:
    # sample frames every `sample_rate` seconds
    model = _load_model()
    if not model:
        return []
    try:
        res = model.track(path, persist=False)
        labels = set()
        for r in res:
            for box in r.boxes:
                labels.add(model.names[int(box.cls)])
        return list(labels)
    except Exception:
        return []
