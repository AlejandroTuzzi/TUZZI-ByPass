import os
import shutil

class SaveVideoTUZZI:
    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "video_path": ("STRING", {"forceInput": True}),
            },
        }

    FUNCTION = "save_video"
    RETURN_TYPES = ()
    OUTPUT_NODE = True
    CATEGORY = "TUZZI-ByPass"

    def save_video(self, video_path):
        if not os.path.exists(video_path):
            raise FileNotFoundError(f"🎥 Video file not found: {video_path}")

        ext = os.path.splitext(video_path)[1].lower()
        if ext not in ('.mp4', '.webm', '.mkv'):
            raise ValueError("❌ Only .mp4, .webm, or .mkv formats are supported.")

        os.makedirs("output", exist_ok=True)
        destination = f"output/tuzzi_last_output{ext}"

        shutil.copy(video_path, destination)

        print(f"✅ TUZZI SaveVideo: copied to {destination}")

        return {
            "ui": {
                "videos": [{
                    "filename": destination,
                    "type": "output"
                }]
            }
        }
