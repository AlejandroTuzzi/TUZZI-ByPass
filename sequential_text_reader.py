# TUZZI-ByPass - Custom Node
# Author: Alejandro Tuzzi
# Website: https://www.tuzzi.es
# Contact: alejandro@tuzzi.es
# License: GNU General Public License v3.0

class SequentialTextReader:
    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "text_block": ("STRING", {"multiline": True}),
                "line_number": ("INT", {"default": 1, "min": 1, "max": 999}),
            }
        }

    RETURN_TYPES = ("STRING", "INT")
    RETURN_NAMES = ("selected_text", "updated_line_number")
    FUNCTION = "read_line"
    CATEGORY = "TUZZI-ByPass"

    def read_line(self, text_block, line_number):
        lines = [line.strip() for line in text_block.splitlines()]
        total_lines = len(lines)

        # Empezamos a buscar desde la línea actual
        index = line_number - 1

        for offset in range(total_lines):
            i = (index + offset) % total_lines
            if lines[i]:
                new_line_number = i + 1  # Convertimos índice a número (1-based)
                self.INPUT_TYPES()["required"]["line_number"] = ("INT", {"default": new_line_number, "min": 1, "max": 999})
                return (lines[i], new_line_number)

        # Si absolutamente todas las líneas están vacías
        return ("", line_number)
