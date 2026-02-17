"""Rendering pipeline using MoviePy and ffmpeg."""
from moviepy.editor import VideoFileClip, concatenate_videoclips, AudioFileClip, vfx
from typing import List, Dict
import os

def apply_filter(clip, filt):
    if not filt:
        return clip
    if filt in ("bw", "b&w"):
        return clip.fx(vfx.blackwhite)
    if filt == "sepia":
        # simple color transform
        return clip.fx(vfx.colorx, 0.9)
    return clip

def apply_speed(clip, speed):
    if speed == "slow":
        return clip.fx(vfx.speedx, 0.6)
    if speed == "fast":
        return clip.fx(vfx.speedx, 1.5)
    return clip

def render(selected_shots: List[Dict], output_path: str, directives: Dict):
    clips = []
    for s in selected_shots:
        try:
            clip = VideoFileClip(s["file"]["path"]).subclip(s["start"], s["end"] if s["end"] else s["start"] + 5)
            clip = apply_filter(clip, directives.get("filter"))
            clip = apply_speed(clip, directives.get("speed"))
            clips.append(clip)
        except Exception:
            continue

    if not clips:
        # fallback: create a 5s blank clip from first file
        raise RuntimeError("No clips to render")

    final = concatenate_videoclips(clips, method="compose")

    # add music if requested
    music = directives.get("music")
    assets_dir = os.path.join(os.path.dirname(__file__), "assets")
    music_file = os.path.join(assets_dir, "upbeat.mp3")
    if music and os.path.exists(music_file):
        try:
            audio = AudioFileClip(music_file).volumex(0.6)
            final = final.set_audio(audio.set_duration(final.duration))
        except Exception:
            pass

    final.write_videofile(output_path, codec="libx264", audio_codec="aac", threads=2, logger=None)
