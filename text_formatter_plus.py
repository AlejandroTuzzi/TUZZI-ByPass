# TUZZI-ByPass - Custom Node
# Author: Alejandro Tuzzi
# Website: https://www.tuzzi.es
# Contact: alejandro@tuzzi.es
# License: GNU General Public License v3.0

class TextFormatterPlus:
    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "text": ("STRING", {"multiline": True}),
                "enable_word_wrap": ("BOOLEAN", {"default": False}),
                "words_per_line": ("INT", {"default": 12, "min": 1, "max": 999}),
                "minimum_tail_words": ("INT", {"default": 0, "min": 0, "max": 999}),
            }
        }

    RETURN_TYPES = ("STRING",)
    RETURN_NAMES = ("formatted_text",)
    FUNCTION = "format_text"
    CATEGORY = "TUZZI-ByPass"

    def format_text(self, text, enable_word_wrap=False, words_per_line=12, minimum_tail_words=0):
        # Reemplaza punto y espacio por punto y salto de línea
        base_text = text.replace(". ", ".\n")

        # Elimina líneas vacías y junta el texto
        lines = [line.strip() for line in base_text.splitlines() if line.strip()]
        joined = " ".join(lines)  # Todo el texto en una sola línea

        if not enable_word_wrap:
            return ("\n".join(lines),)

        # Separar por palabras
        words = joined.split()
        fragments = []
        current = []

        for word in words:
            current.append(word)
            if len(current) == words_per_line:
                fragments.append(" ".join(current))
                current = []

        # Agregar cualquier fragmento restante
        if current:
            if minimum_tail_words > 0 and fragments:
                if len(current) < minimum_tail_words:
                    # Une el resto con el último fragmento
                    fragments[-1] += " " + " ".join(current)
                else:
                    fragments.append(" ".join(current))
            else:
                fragments.append(" ".join(current))

        return ("\n".join(fragments),)
