# TUZZI-ByPass - Custom Node
# Author: Alejandro Tuzzi
# Website: https://www.tuzzi.es
# Contact: alejandro@tuzzi.es
# License: GNU General Public License v3.0

import os
import requests
import tempfile
from datetime import datetime

class ElevenLabsTTS:
    ELEVENLABS_LANGUAGES = {
        "en": "English",
        "es": "Spanish",
        "de": "German",
        "fr": "French",
        "it": "Italian",
        "pt": "Portuguese",
        "pl": "Polish",
        "tr": "Turkish",
        "sv": "Swedish",
        "nl": "Dutch",
        "ro": "Romanian",
        "ar": "Arabic",
        "zh": "Chinese",
        "ja": "Japanese",
        "ko": "Korean",
        "hi": "Hindi",
        "fil": "Filipino",
        "id": "Indonesian",
        "uk": "Ukrainian",
        "el": "Greek",
        "cs": "Czech",
        "da": "Danish",
        "fi": "Finnish",
        "no": "Norwegian",
        "ru": "Russian",
        "sk": "Slovak",
        "hu": "Hungarian",
        "th": "Thai",
        "vi": "Vietnamese",
        "ms": "Malay",
        "ca": "Catalan",
        "hr": "Croatian",
        "bg": "Bulgarian",
        "he": "Hebrew",
        "fa": "Persian",
        "sw": "Swahili",
        "lv": "Latvian",
        "lt": "Lithuanian",
        "et": "Estonian",
        "is": "Icelandic",
        "sq": "Albanian",
        "sr": "Serbian",
        "mk": "Macedonian",
        "sl": "Slovenian",
        "bn": "Bengali",
        "ta": "Tamil",
        "te": "Telugu",
        "ml": "Malayalam",
        "kn": "Kannada",
        "mr": "Marathi",
        "pa": "Punjabi",
        "gu": "Gujarati",
        "or": "Odia",
        "as": "Assamese",
        "mn": "Mongolian",
        "ne": "Nepali",
        "km": "Khmer",
        "la": "Lao",
        "my": "Burmese",
        "tl": "Tagalog",
        "jv": "Javanese",
        "su": "Sundanese"
    }

    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "text": ("STRING", {"multiline": True}),
                "voice_id": ("STRING", {"default": ""}),
                "language_code": (list(cls.ELEVENLABS_LANGUAGES.keys()), {"default": "es"}),
                "output_path": ("STRING", {"default": "output/tts_audio"}),
                "file_name": ("STRING", {"default": "voz"}),
                "stability": ("FLOAT", {"default": 0.5, "min": 0.0, "max": 1.0, "step": 0.05, "display": "slider"}),
                "similarity_boost": ("FLOAT", {"default": 0.75, "min": 0.0, "max": 1.0, "step": 0.05, "display": "slider"}),
                "style_exaggeration": ("FLOAT", {"default": 0.0, "min": 0.0, "max": 1.0, "step": 0.05, "display": "slider"}),
            }
        }

    RETURN_TYPES = ("STRING",)
    RETURN_NAMES = ("full_path",)
    FUNCTION = "synthesize"
    CATEGORY = "TUZZI-ByPass"

    def __init__(self):
        key_path = os.path.join(os.path.dirname(__file__), "elevenlabs_api_key.txt")
        try:
            with open(key_path, "r", encoding="utf-8") as f:
                self.api_key = f.read().strip()
            if self.api_key.startswith("key="):
                self.api_key = self.api_key[4:]
        except FileNotFoundError:
            raise FileNotFoundError(f"No se encontró el archivo: {key_path}. Asegúrate de que 'elevenlabs_api_key.txt' existe en la misma carpeta que este nodo y contiene tu API key.")
        except Exception as e:
            raise Exception(f"Error al leer la API key: {e}")

    def synthesize(self, text, voice_id, language_code, output_path, file_name, stability, similarity_boost, style_exaggeration):
        headers = {
            "xi-api-key": self.api_key,
            "Content-Type": "application/json"
        }

        payload = {
            "text": text,
            "model_id": "eleven_multilingual_v2",
            "voice_settings": {
                "stability": stability,
                "similarity_boost": similarity_boost,
                "style_exaggeration": style_exaggeration,
            },
            "language_id": language_code
        }

        os.makedirs(output_path, exist_ok=True)

        # Búsqueda de nombre incremental
        base = os.path.join(output_path, file_name)
        index = 1
        while True:
            filename = f"{base}_{index:05d}.mp3"
            if not os.path.exists(filename):
                break
            index += 1

        response = requests.post(
            f"https://api.elevenlabs.io/v1/text-to-speech/{voice_id}/stream",
            headers=headers,
            json=payload
        )

        if response.status_code != 200:
            return (f"[Error]: {response.status_code} - {response.text}",)

        with open(filename, "wb") as f:
            f.write(response.content)

        return (os.path.abspath(filename),)

    @classmethod
    def IS_CHANGED(cls, **kwargs):
        import time
        return time.time()


NODE_CLASS_MAPPINGS = {
    "TUZZI-ElevenLabsTTS": ElevenLabsTTS
}

NODE_DISPLAY_NAME_MAPPINGS = {
    "TUZZI-ElevenLabsTTS": "🗣️ ElevenLabs TTS Generator"
}