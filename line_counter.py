# TUZZI-ByPass - Custom Node
# Author: Alejandro Tuzzi
# Website: https://www.tuzzi.es
# Contact: alejandro@tuzzi.es
# License: GNU General Public License v3.0

class LineCounter:
    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "text": ("STRING", {"multiline": True}),
            }
        }

    RETURN_TYPES = ("INT",)
    RETURN_NAMES = ("line_count",)
    FUNCTION = "count_lines"
    CATEGORY = "TUZZI-ByPass"

    def count_lines(self, text):
        line_count = len([line for line in text.splitlines() if line.strip() != ""])
        return (line_count,)