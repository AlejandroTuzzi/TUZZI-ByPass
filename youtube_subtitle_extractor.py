# TUZZI-ByPass - Custom Node
# Author: Alejandro Tuzzi
# Website: https://www.tuzzi.es
# Contact: alejandro@tuzzi.es
# License: GNU General Public License v3.0

import os
import re
from youtube_transcript_api import YouTubeTranscriptApi, TranscriptsDisabled, NoTranscriptFound
from urllib.parse import urlparse, parse_qs
import requests

class YouTubeSubtitleExtractor:
    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "youtube_url_or_id": ("STRING", {"multiline": False}),
                "output_subfolder": ("STRING", {"default": "youtube_subtitles"}),
                "preferred_languages": ("STRING", {"default": "en,es"})
            }
        }

    RETURN_TYPES = ("STRING",)
    RETURN_NAMES = ("subtitles",)
    FUNCTION = "extract_subtitles"
    CATEGORY = "TUZZI-ByPass"

    def extract_subtitles(self, youtube_url_or_id, output_subfolder, preferred_languages):
        video_id = self._extract_video_id(youtube_url_or_id)
        if not video_id:
            return ("❌ Could not parse YouTube ID.",)

        languages = [lang.strip() for lang in preferred_languages.split(",") if lang.strip()]
        
        # Usar directamente la carpeta output de ComfyUI
        folder_path = os.path.join("ComfyUI\output", output_subfolder)
        os.makedirs(folder_path, exist_ok=True)

        try:
            # Obtener el título del video
            video_title = self._get_video_title(video_id)
            if not video_title:
                video_title = "youtube_video"
            
            # Obtener transcripción
            transcript = YouTubeTranscriptApi.get_transcript(video_id, languages=languages)
            text_lines = [line['text'] for line in transcript]
            text = "\n".join(text_lines)
            
            # Sanitizar el título para usarlo como nombre de archivo
            sanitized_title = self._sanitize_filename(video_title)[:100]
            output_path = os.path.join(folder_path, f"{sanitized_title}.txt")

            # Guardar el archivo
            with open(output_path, "w", encoding="utf-8") as f:
                f.write(text)
            
            # Devolver directamente los subtítulos
            return (text,)
            
        except (TranscriptsDisabled, NoTranscriptFound):
            error_msg = "Subtitles could not be extracted from this video."
            return (error_msg,)
        except Exception as e:
            error_msg = f"Error while retrieving subtitles: {str(e)}"
            return (error_msg,)

    def _extract_video_id(self, url_or_id):
        if len(url_or_id) == 11 and all(c.isalnum() for c in url_or_id):
            return url_or_id
        try:
            parsed = urlparse(url_or_id)
            if parsed.hostname in ["youtu.be"]:
                return parsed.path.lstrip("/")
            if parsed.hostname and "youtube" in parsed.hostname:
                qs = parse_qs(parsed.query)
                return qs.get("v", [None])[0]
        except:
            pass
        return None
    
    def _get_video_title(self, video_id):
        try:
            # Método básico para obtener el título usando la API de oEmbed de YouTube
            oembed_url = f"https://www.youtube.com/oembed?url=https://www.youtube.com/watch?v={video_id}&format=json"
            response = requests.get(oembed_url)
            
            if response.status_code == 200:
                return response.json().get('title', '')
            return None
        except Exception:
            return None
            
    def _sanitize_filename(self, filename):
        # Eliminar caracteres no permitidos en Windows
        return re.sub(r'[\\/:*?"<>|]', '_', filename.strip())