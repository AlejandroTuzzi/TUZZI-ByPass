# TUZZI-ByPass - Custom Node
# Author: Alejandro Tuzzi
# Website: https://www.tuzzi.es
# Contact: alejandro@tuzzi.es
# License: GNU General Public License v3.0

import os
import re
import tempfile
import numpy as np
from moviepy.editor import AudioFileClip, ImageClip
from PIL import Image
import soundfile as sf

class ImageAudioToVideo:
    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "image": ("IMAGE",),
                "audio": ("AUDIO",),
                "output_subfolder": ("STRING", {"default": "autoVideo"}),
                "fps": ("INT", {"default": 25, "min": 25, "max": 30}),
            }
        }

    RETURN_TYPES = ("STRING",)
    RETURN_NAMES = ("video_path",)
    FUNCTION = "generate"
    CATEGORY = "TUZZI-ByPass"

    def generate(self, image, audio, output_subfolder, fps):
        # Crear carpeta base
        base_path = os.path.join("output", output_subfolder)
        os.makedirs(base_path, exist_ok=True)

        # Crear path incremental estilo ComfyUI
        base_name = "video"
        extension = ".mp4"
        existing = os.listdir(base_path)
        pattern = re.compile(rf"{base_name}_(\d{{5}})_\.mp4")
        max_index = 0
        for f in existing:
            match = pattern.search(f)
            if match:
                max_index = max(max_index, int(match.group(1)))
        new_filename = f"{base_name}_{max_index + 1:05d}_" + extension
        full_output_path = os.path.join(base_path, new_filename)

        # Guardar imagen temporal
        temp_img = os.path.join(tempfile.gettempdir(), "frame_temp.png")
        pil_image = Image.fromarray((image[0].cpu().numpy().clip(0, 1) * 255).astype("uint8"))
        pil_image.save(temp_img)

        # Guardar audio temporal
        temp_audio = os.path.join(tempfile.gettempdir(), "audio_temp.wav")
        waveform = audio["waveform"].squeeze().cpu().numpy()
        sample_rate = audio["sample_rate"]
        sf.write(temp_audio, waveform, sample_rate)

        # Crear el clip de video
        audio_clip = AudioFileClip(temp_audio)
        image_clip = ImageClip(temp_img).set_duration(audio_clip.duration).set_audio(audio_clip)
        image_clip.write_videofile(full_output_path, fps=fps)

        return (full_output_path,)