# TUZZI-ByPass - Custom Node
# Author: Alejandro Tuzzi
# Website: https://www.tuzzi.es
# Contact: alejandro@tuzzi.es
# License: GNU General Public License v3.0

class RangedSelectorTitleURL10:
    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "index": ("INT", {"default": 1, "min": 0}),
                "title1": ("STRING", {"multiline": False}), "url1": ("STRING", {"multiline": False}), "range1": ("INT", {"default": 5, "min": 0}),
                "title2": ("STRING", {"multiline": False}), "url2": ("STRING", {"multiline": False}), "range2": ("INT", {"default": 10, "min": 0}),
                "title3": ("STRING", {"multiline": False}), "url3": ("STRING", {"multiline": False}), "range3": ("INT", {"default": 15, "min": 0}),
                "title4": ("STRING", {"multiline": False}), "url4": ("STRING", {"multiline": False}), "range4": ("INT", {"default": 20, "min": 0}),
                "title5": ("STRING", {"multiline": False}), "url5": ("STRING", {"multiline": False}), "range5": ("INT", {"default": 25, "min": 0}),
                "title6": ("STRING", {"multiline": False}), "url6": ("STRING", {"multiline": False}), "range6": ("INT", {"default": 30, "min": 0}),
                "title7": ("STRING", {"multiline": False}), "url7": ("STRING", {"multiline": False}), "range7": ("INT", {"default": 35, "min": 0}),
                "title8": ("STRING", {"multiline": False}), "url8": ("STRING", {"multiline": False}), "range8": ("INT", {"default": 40, "min": 0}),
                "title9": ("STRING", {"multiline": False}), "url9": ("STRING", {"multiline": False}), "range9": ("INT", {"default": 45, "min": 0}),
                "title10": ("STRING", {"multiline": False}), "url10": ("STRING", {"multiline": False}), "range10": ("INT", {"default": 50, "min": 0})
            }
        }

    RETURN_TYPES = ("STRING", "STRING", "INT")
    RETURN_NAMES = ("title", "url", "offset")
    FUNCTION = "select"
    CATEGORY = "TUZZI-ByPass"

    def select(self, index, **kwargs):
        entries = []
        for i in range(1, 11):
            title = kwargs.get(f"title{i}", "")
            url = kwargs.get(f"url{i}", "")
            rng = kwargs.get(f"range{i}", 0)
            entries.append((title, url, rng))

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
