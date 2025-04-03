# TUZZI-ByPass - Custom Node
# Author: Alejandro Tuzzi
# Website: https://www.tuzzi.es
# Contact: alejandro@tuzzi.es
# License: MIT

from .bypasser import Bypasser
from .line_counter import LineCounter
from .text_formatter import TextFormatter  # ⬅️ NUEVO
from .text_formatter_plus import TextFormatterPlus  # ⬅️ NUEVO

NODE_CLASS_MAPPINGS = {
    "TUZZI-Bypasser": Bypasser,
    "TUZZI-LineCounter": LineCounter,
    "TUZZI-TextFormatter": TextFormatter,
    "TUZZI-TextFormatterPlus": TextFormatterPlus,  # ⬅️ NUEVO
}

NODE_DISPLAY_NAME_MAPPINGS = {
    "TUZZI-Bypasser": "Bypasser Switch",
    "TUZZI-LineCounter": "Count Lines in String",
    "TUZZI-TextFormatter": "Add Line Breaks to Text",
    "TUZZI-TextFormatterPlus": "Smart Line Breaks (by Word Count)",  # ⬅️ NUEVO
}