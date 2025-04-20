# TUZZI-ByPass - Custom Node
# Author: Alejandro Tuzzi
# Website: https://www.tuzzi.es
# Contact: alejandro@tuzzi.es
# License: GNU General Public License v3.0

import os
import google.generativeai as genai
import hashlib
import json

class GeminiFlash25:
    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "prompt_instruction": ("STRING", {"multiline": True}),
                "user_input": ("STRING", {"multiline": True}),
                "should_generate": ("INT", {"default": 1, "min": 0})
            }
        }

    RETURN_TYPES = ("STRING",)
    RETURN_NAMES = ("output",)
    FUNCTION = "run"
    CATEGORY = "TUZZI-ByPass"

    def __init__(self):
        key_file = os.path.join(os.path.dirname(__file__), "gemini_api_key.txt")
        if not os.path.exists(key_file):
            raise FileNotFoundError("gemini_api_key.txt not found.")
        with open(key_file, "r", encoding="utf-8") as f:
            self.api_key = f.read().strip().replace("key=", "")

        genai.configure(api_key=self.api_key)
        self.model = genai.GenerativeModel("gemini-2.5-flash-preview-04-17")

        self.cache_dir = os.path.join(os.getcwd(), "gemini_cache")
        os.makedirs(self.cache_dir, exist_ok=True)

    def _get_cache_filename(self, prompt_text):
        digest = hashlib.md5(prompt_text.encode("utf-8")).hexdigest()
        return os.path.join(self.cache_dir, f"gemini_{digest}.json")

    def run(self, prompt_instruction, user_input, should_generate):
        prompt_text = prompt_instruction + "\n" + user_input
        cache_file = self._get_cache_filename(prompt_text)

        if should_generate != 1:
            if os.path.exists(cache_file):
                with open(cache_file, "r", encoding="utf-8") as f:
                    cached = json.load(f)
                    return (cached.get("response", user_input),)
            else:
                return (user_input,)

        try:
            response = self.model.generate_content([
                {"role": "user", "parts": [prompt_text]}
            ])
            output_text = response.text

            with open(cache_file, "w", encoding="utf-8") as f:
                json.dump({"prompt": prompt_text, "response": output_text}, f, ensure_ascii=False, indent=2)

            return (output_text,)

        except Exception as e:
            return (f"[Error]: {str(e)}",)
