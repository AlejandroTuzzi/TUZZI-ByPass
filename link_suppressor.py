# TUZZI-ByPass - Custom Node
# Author: Alejandro Tuzzi
# Website: https://www.tuzzi.es
# Contact: alejandro@tuzzi.es
# License: MIT

import re
import inspect
import time
import os

# Activar registro de depuración
DEBUG = True

def debug_log(message):
    if DEBUG:
        timestamp = time.strftime("%Y-%m-%d %H:%M:%S")
        log_dir = os.path.join(os.getcwd(), "tuzzi_logs")
        os.makedirs(log_dir, exist_ok=True)
        log_file = os.path.join(log_dir, "link_suppressor_debug.log")
        with open(log_file, "a", encoding="utf-8") as f:
            f.write(f"[{timestamp}] {message}\n")

class LinkSuppressor:
    """
    Nodo que detecta y reemplaza enlaces en texto con un texto personalizado.
    """

    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "text_input": ("STRING", {"multiline": True}),
                "replacement_text": ("STRING", {"default": "(Link Deleted)"}),
            }
        }

    RETURN_TYPES = ("STRING",)
    RETURN_NAMES = ("cleaned_text",)
    FUNCTION = "suppress_links"
    CATEGORY = "TUZZI-ByPass"

    def suppress_links(self, text_input, replacement_text="(Link Deleted)"):
        debug_log(f"Texto de entrada recibido: '{text_input[:100]}...' (primeros 100 caracteres)")

        if text_input is None:
            debug_log("Entrada es None, devolviendo texto vacío")
            return ("",)

        if not isinstance(text_input, str):
            text_input = str(text_input)
            debug_log(f"Entrada convertida a string: {type(text_input)}")

        if not text_input.strip():
            debug_log("Entrada está vacía, devolviendo la misma entrada")
            return (text_input,)

        # Detectar URLs hasta el primer espacio o fin de línea
        url_pattern = r'https?://[^\s)>"]+'
        markdown_pattern = r'\[([^\]]+)\]\(([^)]+)\)'
        html_pattern = r'<a\s+(?:[^>]*?\s+)?href="([^"]*)"(?:\s+[^>]*)?>(.*?)</a>'

        url_count = len(re.findall(url_pattern, text_input))
        markdown_count = len(re.findall(markdown_pattern, text_input))
        html_count = len(re.findall(html_pattern, text_input))

        debug_log(f"Enlaces encontrados - URLs: {url_count}, Markdown: {markdown_count}, HTML: {html_count}")

        # Reemplaza cualquier URL completa, incluso con parámetros y extensiones
        cleaned_text = re.sub(url_pattern, replacement_text, text_input)
        cleaned_text = re.sub(markdown_pattern, lambda m: f"{m.group(1)} {replacement_text}", cleaned_text)
        cleaned_text = re.sub(html_pattern, lambda m: f"{m.group(2)} {replacement_text}", cleaned_text)

        debug_log(f"Texto de salida: '{cleaned_text[:100]}...' (primeros 100 caracteres)")

        if not cleaned_text.strip() and text_input.strip():
            debug_log("¡ADVERTENCIA! El texto procesado quedó vacío pero el original no lo era. Devolviendo original.")
            return (text_input,)

        return (cleaned_text,)

    @classmethod
    def IS_CHANGED(cls, **kwargs):
        return time.time()

    @classmethod
    def VALIDATE_INPUTS(cls, **kwargs):
        return True

NODE_CLASS_MAPPINGS = {
    "LinkSuppressor": LinkSuppressor
}

NODE_DISPLAY_NAME_MAPPINGS = {
    "LinkSuppressor": "🔗 Link Suppressor"
}
