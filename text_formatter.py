# TUZZI-ByPass - Custom Node
# Author: Alejandro Tuzzi
# Website: https://www.tuzzi.es
# Contact: alejandro@tuzzi.es
# License: MIT

class TextFormatter:
    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "text": ("STRING", {"multiline": True}),
            }
        }

    RETURN_TYPES = ("STRING",)
    RETURN_NAMES = ("formatted_text",)
    FUNCTION = "format_text"
    CATEGORY = "TUZZI-ByPass"

    def format_text(self, text):
        # Inserta un salto de línea después de cada punto seguido de un espacio
        text = text.replace(". ", ".\n")

        # Divide en líneas, elimina líneas vacías y espacios innecesarios
        lines = [line.strip() for line in text.splitlines() if line.strip()]

        # Junta las líneas en un solo string con saltos de línea
        formatted = "\n".join(lines)

        return (formatted,)
