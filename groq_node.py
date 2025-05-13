# TUZZI-ByPass - Custom Node
# Author: Alejandro Tuzzi
# Website: https://www.tuzzi.es
# Contact: alejandro@tuzzi.es
# License: GNU General Public License v3.0

import os
import requests

class GroqNode:
    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "user_prompt": ("STRING", {"multiline": True}),
                "system_instruction": ("STRING", {"multiline": True}),
                "should_generate": ("INT", {"default": 1, "min": 0}),
                "model_name": (["mixtral-8x7b-32768", "llama3-8b-8192", "llama3-70b-8192"],),
            }
        }

    RETURN_TYPES = ("STRING",)
    RETURN_NAMES = ("output",)
    FUNCTION = "run"
    CATEGORY = "TUZZI-ByPass"

    def __init__(self):
        # Cargar API key desde archivo
        key_path = os.path.join(os.path.dirname(__file__), "groq_api_key.txt")
        if not os.path.exists(key_path):
            raise FileNotFoundError("groq_api_key.txt not found.")
        with open(key_path, "r", encoding="utf-8") as f:
            self.api_key = f.read().strip().replace("key=", "")

    def run(self, user_prompt, system_instruction, should_generate, model_name):
        if should_generate != 1:
            return (user_prompt + "\u200b",)

        try:
            url = "https://api.groq.com/openai/v1/chat/completions"
            headers = {
                "Authorization": f"Bearer {self.api_key}",
                "Content-Type": "application/json",
            }

            payload = {
                "model": model_name,
                "messages": [
                    {"role": "system", "content": system_instruction},
                    {"role": "user", "content": user_prompt}
                ],
                "temperature": 0.7
            }

            response = requests.post(url, headers=headers, json=payload)
            if response.status_code == 200:
                result = response.json()
                return (result["choices"][0]["message"]["content"].strip(),)
            else:
                return (f"[Groq Error {response.status_code}]: {response.text}",)

        except Exception as e:
            return (f"[Exception]: {str(e)}",)
