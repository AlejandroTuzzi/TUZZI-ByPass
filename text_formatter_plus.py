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
                "remove_patterns": ("STRING", {"default": ""}),
            }
        }

    RETURN_TYPES = ("STRING",)
    RETURN_NAMES = ("formatted_text",)
    FUNCTION = "format_text"
    CATEGORY = "TUZZI-ByPass"

    def format_text(self, text, enable_word_wrap=False, words_per_line=12, minimum_tail_words=0, remove_patterns=""):
        # Eliminar patrones indeseados definidos por el usuario
        if remove_patterns.strip():
            for pattern in [p.strip() for p in remove_patterns.split(",") if p.strip()]:
                text = text.replace(pattern, "")

        # Reemplaza punto y espacio por punto + salto de línea
        base_text = text.replace(". ", ".\n")

        if not enable_word_wrap:
            # Limpia líneas vacías, pero conserva los saltos reales
            lines = [line.strip() for line in base_text.splitlines() if line.strip()]
            return ("\n".join(lines),)

        # Si el word wrap está activo, procesamos línea por línea
        final_lines = []
        for line in base_text.splitlines():
            stripped = line.strip()
            if not stripped:
                continue

            words = stripped.split()
            current = []

            for word in words:
                current.append(word)
                if len(current) == words_per_line:
                    final_lines.append(" ".join(current))
                    current = []

            # Manejo del fragmento restante
            if current:
                if minimum_tail_words > 0 and final_lines:
                    if len(current) < minimum_tail_words:
                        final_lines[-1] += " " + " ".join(current)
                    else:
                        final_lines.append(" ".join(current))
                else:
                    final_lines.append(" ".join(current))

        return ("\n".join(final_lines),)