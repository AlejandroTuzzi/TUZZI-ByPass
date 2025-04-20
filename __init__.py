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
from .youtube_comment_extractor import YouTubeCommentExtractor
from .youtube_subtitle_extractor import YouTubeSubtitleExtractor
from .text_truncator_plus import TextTruncatorPlus
from .sequential_text_reader_auto import SequentialTextReaderAuto
from .link_suppressor import LinkSuppressor
from .image_extractor_saver import ImageExtractorSaver
from .directory_image_prompt_reader import DirectoryImagePromptReader
from .text_translator_exporter import TextTranslatorExporter
from .gemini_25_flash_node import GeminiFlash25
from .plos_article_scraper import PlosArticleScraper


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
    "TUZZI-YouTubeCommentExtractor": YouTubeCommentExtractor,
    "TUZZI-YouTubeSubtitleExtractor": YouTubeSubtitleExtractor,
    "TUZZI-TextTruncatorPlus": TextTruncatorPlus,
    "TUZZI-SequentialTextReaderAuto": SequentialTextReaderAuto,
    "TUZZI-LinkSuppressor": LinkSuppressor,
    "TUZZI-ImageExtractorSaver": ImageExtractorSaver,
    "TUZZI-DirectoryImagePromptReader": DirectoryImagePromptReader,
    "TUZZI-TextTranslatorExporter": TextTranslatorExporter,
    "TUZZI-GeminiFlash25": GeminiFlash25,
    "TUZZI-PlosArticleScraper": PlosArticleScraper,
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
    "TUZZI-YouTubeCommentExtractor": "YouTube Comment Extractor",
    "TUZZI-YouTubeSubtitleExtractor": "YouTube Subtitle Extractor",
    "TUZZI-TextTruncatorPlus": "✂️ Text Truncator Plus",
    "TUZZI-SequentialTextReaderAuto": "🪜 Sequential Text Reader (Auto)",
    "TUZZI-LinkSuppressor": "🔗 Link Suppressor",
    "TUZZI-ImageExtractorSaver": "🖼️ Image Extractor & Saver",
    "TUZZI-DirectoryImagePromptReader": "🗂️ Image + Prompt Loader (Sequential/Random)",
    "TUZZI-TextTranslatorExporter": "🌍 Text Translator + Exporter (GPT-4)",
    "TUZZI-GeminiFlash25": "⚡ Gemini 2.5 Flash (Text)",
    "TUZZI-PlosArticleScraper": "📖 PLOS Article Scraper",
}