
# TUZZI-ByPass - Custom Node
# Author: Alejandro Tuzzi
# Website: https://www.tuzzi.es
# Contact: alejandro@tuzzi.es
# License: GNU General Public License v3.0

import os
import tempfile
import shutil
from moviepy.editor import VideoFileClip, concatenate_videoclips

class AppendToMasterVideo:
    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "video_path": ("STRING", {"multiline": False}),
                "master_video_name": ("STRING", {"default": "final_output"}),
                "output_folder": ("STRING", {"default": "output/final_video"}),
                "trim_start_frames": ("INT", {"default": 0, "min": 0}),
                "trim_end_frames": ("INT", {"default": 0, "min": 0}),
            }
        }

    RETURN_TYPES = ("STRING",)
    RETURN_NAMES = ("final_video_path",)
    FUNCTION = "append"
    CATEGORY = "TUZZI-ByPass"

    def append(self, video_path, master_video_name, output_folder, trim_start_frames, trim_end_frames):
        os.makedirs(output_folder, exist_ok=True)
        master_video_path = os.path.join(output_folder, f"{master_video_name}.mp4")

        clips = []

        if os.path.exists(master_video_path):
            clips.append(VideoFileClip(master_video_path))

        new_clip = VideoFileClip(video_path)
        fps = new_clip.fps
        duration = new_clip.duration
        start_time = trim_start_frames / fps
        end_time = duration - (trim_end_frames / fps)

        trimmed = new_clip.subclip(start_time, end_time)
        clips.append(trimmed)

        final_clip = concatenate_videoclips(clips, method="compose")

        with tempfile.NamedTemporaryFile(delete=False, suffix=".mp4") as tmpfile:
            temp_output = tmpfile.name

        final_clip.write_videofile(temp_output, codec="libx264", audio_codec="aac")
        final_clip.close()

        try:
            shutil.copy2(temp_output, master_video_path)
            os.remove(temp_output)
        except Exception as e:
            return (f"[ERROR al mover video]: {str(e)}",)

        return (os.path.abspath(master_video_path),)
