# TUZZI-ByPass - Custom Node
# Author: Alejandro Tuzzi
# Website: https://www.tuzzi.es
# Contact: alejandro@tuzzi.es
# License: MIT

from .bypasser import Bypasser
from .line_counter import LineCounter
from .text_formatter import TextFormatter  
from .text_formatter_plus import TextFormatterPlus  
from .sequential_text_reader import SequentialTextReader
from .reddit_post_extractor import RedditPostExtractor

NODE_CLASS_MAPPINGS = {
    "TUZZI-Bypasser": Bypasser,
    "TUZZI-LineCounter": LineCounter,
    "TUZZI-TextFormatter": TextFormatter,
    "TUZZI-TextFormatterPlus": TextFormatterPlus,
    "TUZZI-SequentialTextReader": SequentialTextReader,
    "TUZZI-RedditPostExtractor": RedditPostExtractor,
}

NODE_DISPLAY_NAME_MAPPINGS = {
    "TUZZI-Bypasser": "Bypasser Switch",
    "TUZZI-LineCounter": "Count Lines in String",
    "TUZZI-TextFormatter": "Add Line Breaks to Text",
    "TUZZI-TextFormatterPlus": "Smart Line Breaks (by Word Count)",
    "TUZZI-SequentialTextReader": "Sequential Text Reader",
    "TUZZI-RedditPostExtractor": "Reddit Post Extractor",
}