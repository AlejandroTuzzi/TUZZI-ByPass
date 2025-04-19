# TUZZI-ByPass - Custom Node
# Author: Alejandro Tuzzi
# Website: https://www.tuzzi.es
# Contact: alejandro@tuzzi.es
# License: GNU General Public License v3.0

import os
import textwrap
from openai import OpenAI

class TextTranslatorExporter:
    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "text": ("STRING", {"multiline": True}),
                "should_translate": ("INT", {"default": 1, "min": 0, "max": 1}),
                "output_path": ("STRING", {"default": "translations/output.txt"}),
                "model": (["gpt-4", "gpt-4o", "gpt-3.5-turbo"],)
            }
        }

    RETURN_TYPES = ("STRING",)
    RETURN_NAMES = ("translated_text",)
    FUNCTION = "translate"
    CATEGORY = "TUZZI-ByPass"

    def __init__(self):
        key_file = os.path.join(os.path.dirname(__file__), "openai_api_key.txt")
        if not os.path.exists(key_file):
            raise FileNotFoundError("openai_api_key.txt not found.")
        with open(key_file, "r", encoding="utf-8") as f:
            key_line = f.read().strip()
            if key_line.startswith("key="):
                self.api_key = key_line.split("=", 1)[1]
            else:
                self.api_key = key_line

        self.client = OpenAI(api_key=self.api_key)

    def translate(self, text, should_translate, output_path, model):
        if should_translate != 1:
            return (text,)

        os.makedirs(os.path.dirname(output_path), exist_ok=True)

        chunks = self._chunk_text(text, max_tokens=3000)
        translated_chunks = []

        for chunk in chunks:
            try:
                response = self.client.chat.completions.create(
                    model=model,
                    messages=[
                        {"role": "system", "content": "You are a professional translator. Translate the following text to Spanish."},
                        {"role": "user", "content": chunk}
                    ],
                    temperature=0.2
                )
                translated = response.choices[0].message.content.strip()
                translated_chunks.append(translated)
            except Exception as e:
                translated_chunks.append(f"[Error translating chunk: {str(e)}]")

        full_translation = "\n\n".join(translated_chunks)

        with open(output_path, "w", encoding="utf-8") as f:
            f.write(full_translation)

        return (full_translation,)

    def _chunk_text(self, text, max_tokens=3000):
        paragraphs = text.split("\n\n")
        current_chunk = ""
        chunks = []

        for para in paragraphs:
            if len((current_chunk + para).split()) > max_tokens:
                if current_chunk:
                    chunks.append(current_chunk.strip())
                    current_chunk = ""
            current_chunk += para + "\n\n"

        if current_chunk:
            chunks.append(current_chunk.strip())

        return chunks
