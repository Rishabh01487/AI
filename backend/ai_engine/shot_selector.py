"""Select shots to match a target duration with simple scoring."""
from typing import List, Dict


def score_scene(scene, tags):
    # basic heuristic: more tags -> higher score
    return len(tags)


def select_shots(scenes_with_tags: List[Dict], target_duration: int, include_tags: List[str], exclude_tags: List[str]) -> List[Dict]:
    """Greedy selection of scenes until target_duration reached."""
    candidates = []
    for entry in scenes_with_tags:
        file = entry["file"]
        for s in entry.get("scenes", []):
            start, end = s
            duration = (end - start) if end else 5
            tags = entry.get("tags", [])
            # filter include/exclude
            if include_tags and not any(t in tags for t in include_tags):
                continue
            if exclude_tags and any(t in tags for t in exclude_tags):
                continue
            candidates.append({"file": file, "start": start, "end": end, "duration": duration, "score": score_scene(s, tags)})

    # sort by score descending
    candidates.sort(key=lambda x: x["score"], reverse=True)
    selected = []
    total = 0
    for c in candidates:
        if total >= target_duration:
            break
        selected.append(c)
        total += c["duration"]
    return selected
