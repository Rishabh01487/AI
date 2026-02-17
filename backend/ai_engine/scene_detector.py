"""Scene detection using PySceneDetect (ContentDetector)."""
from scenedetect import VideoManager, SceneManager
from scenedetect.detectors import ContentDetector
from typing import List, Tuple


def detect_scenes(video_path: str) -> List[Tuple[float, float]]:
    """Return list of (start_sec, end_sec) scenes."""
    try:
        video_manager = VideoManager([video_path])
        scene_manager = SceneManager()
        scene_manager.add_detector(ContentDetector())
        video_manager.set_downscale_factor()
        video_manager.start()
        scene_manager.detect_scenes(frame_source=video_manager)
        scene_list = scene_manager.get_scene_list()
        out = []
        for s in scene_list:
            start = s[0].get_seconds()
            end = s[1].get_seconds()
            out.append((start, end))
        video_manager.release()
        return out
    except Exception:
        return []
