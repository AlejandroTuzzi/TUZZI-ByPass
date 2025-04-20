# TUZZI-ByPass - Custom Node
# Author: Alejandro Tuzzi
# Website: https://www.tuzzi.es
# Contact: alejandro@tuzzi.es
# License: GNU General Public License v3.0

class RangedSelectorText5:
    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "index": ("INT", {"default": 1, "min": 0}),
                "text1": ("STRING", {"multiline": True}),
                "range1": ("INT", {"default": 5, "min": 0}),
                "text2": ("STRING", {"multiline": True}),
                "range2": ("INT", {"default": 10, "min": 0}),
                "text3": ("STRING", {"multiline": True}),
                "range3": ("INT", {"default": 15, "min": 0}),
                "text4": ("STRING", {"multiline": True}),
                "range4": ("INT", {"default": 20, "min": 0}),
                "text5": ("STRING", {"multiline": True}),
                "range5": ("INT", {"default": 25, "min": 0})
            }
        }

    RETURN_TYPES = ("STRING", "INT")
    RETURN_NAMES = ("selected_text", "offset")
    FUNCTION = "select"
    CATEGORY = "TUZZI-ByPass"

    def select(self, index, text1, range1, text2, range2, text3, range3, text4, range4, text5, range5):
        entries = [
            (text1, range1),
            (text2, range2),
            (text3, range3),
            (text4, range4),
            (text5, range5)
        ]

        previous_max = 0
        for i, (text, max_val) in enumerate(entries):
            if max_val == 0:
                continue
            if max_val <= previous_max:
                return (f"⚠️ Error: range{i+1} ({max_val}) must be greater than range{i} ({previous_max})", 0)
            if previous_max < index <= max_val:
                return (text, previous_max)
            previous_max = max_val

        return ("", 0)
