# TUZZI-ByPass - Custom Node
# Author: Alejandro Tuzzi
# Website: https://www.tuzzi.es
# Contact: alejandro@tuzzi.es
# License: GNU General Public License v3.0

class TextTruncatorPlus:
    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "text": ("STRING", {"multiline": True}),
                "cut_after_char": ("INT", {"default": 40, "min": 1, "max": 1000}),
                "suffix": ("STRING", {"default": "(...)"})
            }
        }

    RETURN_TYPES = ("STRING",)
    RETURN_NAMES = ("truncated_text",)
    FUNCTION = "truncate"
    CATEGORY = "TUZZI-ByPass"

    def truncate(self, text, cut_after_char, suffix):
        if len(text) <= cut_after_char:
            return (text,)

        truncated = text[:cut_after_char].rstrip()
        result = truncated + suffix
        return (result,)
