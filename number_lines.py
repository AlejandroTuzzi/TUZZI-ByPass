# TUZZI-ByPass - Custom Node
# Author: Alejandro Tuzzi
# Website: https://www.tuzzi.es
# Contact: alejandro@tuzzi.es
# License: GNU General Public License v3.0

class NumberLines:
    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "text": ("STRING", {"multiline": True}),
            }
        }

    RETURN_TYPES = ("STRING",)
    RETURN_NAMES = ("numbered_text",)
    FUNCTION = "number_lines"
    CATEGORY = "TUZZI-ByPass"

    def number_lines(self, text):
        lines = text.splitlines()
        numbered = [f"{i + 1}. {line}" for i, line in enumerate(lines)]
        return ("\n".join(numbered),)
