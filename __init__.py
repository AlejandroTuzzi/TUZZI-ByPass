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
from .number_lines import NumberLines
from .image_audio_to_video import ImageAudioToVideo
from .save_video_tuzzi import SaveVideoTUZZI

NODE_CLASS_MAPPINGS = {
    "TUZZI-Bypasser": Bypasser,
    "TUZZI-LineCounter": LineCounter,
    "TUZZI-TextFormatter": TextFormatter,
    "TUZZI-TextFormatterPlus": TextFormatterPlus,
    "TUZZI-SequentialTextReader": SequentialTextReader,
    "TUZZI-RedditPostExtractor": RedditPostExtractor,
    "TUZZI-NumberLines": NumberLines,
    "TUZZI-ImageAudioToVideo": ImageAudioToVideo,
    "TUZZI-SaveVideo": SaveVideoTUZZI,
}

NODE_DISPLAY_NAME_MAPPINGS = {
    "TUZZI-Bypasser": "Bypasser Switch",
    "TUZZI-LineCounter": "Count Lines in String",
    "TUZZI-TextFormatter": "Add Line Breaks to Text",
    "TUZZI-TextFormatterPlus": "Smart Line Breaks (by Word Count)",
    "TUZZI-SequentialTextReader": "Sequential Text Reader",
    "TUZZI-RedditPostExtractor": "Reddit Post Extractor",
    "TUZZI-NumberLines": "Number Each Line",
    "TUZZI-ImageAudioToVideo": "Image + Audio to Video",
    "TUZZI-SaveVideo": "💾 TUZZI Save Video (UI Output)",
}