# TUZZI-ByPass - Custom Node
# Author: Alejandro Tuzzi
# Website: https://www.tuzzi.es
# Contact: alejandro@tuzzi.es
# License: GNU General Public License v3.0

class RangedSelectorTitleURL5:
    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "index": ("INT", {"default": 1, "min": 0}),
                "title1": ("STRING", {"multiline": False}),
                "url1": ("STRING", {"multiline": False}),
                "range1": ("INT", {"default": 5, "min": 0}),
                "title2": ("STRING", {"multiline": False}),
                "url2": ("STRING", {"multiline": False}),
                "range2": ("INT", {"default": 10, "min": 0}),
                "title3": ("STRING", {"multiline": False}),
                "url3": ("STRING", {"multiline": False}),
                "range3": ("INT", {"default": 15, "min": 0}),
                "title4": ("STRING", {"multiline": False}),
                "url4": ("STRING", {"multiline": False}),
                "range4": ("INT", {"default": 20, "min": 0}),
                "title5": ("STRING", {"multiline": False}),
                "url5": ("STRING", {"multiline": False}),
                "range5": ("INT", {"default": 25, "min": 0})
            }
        }

    RETURN_TYPES = ("STRING", "STRING", "INT")
    RETURN_NAMES = ("title", "url", "offset")
    FUNCTION = "select"
    CATEGORY = "TUZZI-ByPass"

    def select(self, index, title1, url1, range1, title2, url2, range2,
               title3, url3, range3, title4, url4, range4, title5, url5, range5):

        entries = [
            (title1, url1, range1),
            (title2, url2, range2),
            (title3, url3, range3),
            (title4, url4, range4),
            (title5, url5, range5)
        ]

        previous_max = 0
        for i, (title, url, max_val) in enumerate(entries):
            if max_val == 0:
                continue
            if max_val <= previous_max:
                return (f"⚠️ Error: range{i+1} ({max_val}) debe ser mayor que range{i} ({previous_max})", "", 0)
            if previous_max < index <= max_val:
                return (title, url, previous_max)
            previous_max = max_val

        return ("", "", 0)
