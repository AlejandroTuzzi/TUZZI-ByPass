# TUZZI-ByPass - Custom Node
# Author: Alejandro Tuzzi
# Website: https://www.tuzzi.es
# Contact: alejandro@tuzzi.es
# License: GNU General Public License v3.0

import os
import requests
from datetime import datetime
from urllib.parse import urlparse, parse_qs

class YouTubeCommentExtractor:
    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "youtube_url_or_id": ("STRING", {"multiline": False}),
                "execution_count": ("INT", {"default": 1, "min": 1}),
                "include_dates": ("BOOLEAN", {"default": True}),
                "max_comments": ("INT", {"default": 100, "min": 1, "max": 500}),
            }
        }

    RETURN_TYPES = ("STRING",)
    RETURN_NAMES = ("formatted_output",)
    FUNCTION = "extract"
    CATEGORY = "TUZZI-ByPass"

    def extract(self, youtube_url_or_id, execution_count, include_dates, max_comments):
        api_key = self._load_api_key()
        if not api_key:
            return ("⚠️ Error: No API key found. Make sure 'youtube_api_key.txt' exists.",)

        video_id = self._extract_video_id(youtube_url_or_id)
        if not video_id:
            return ("⚠️ Error: Could not extract video ID from the input.",)

        cache_dir = os.path.join(os.getcwd(), "youtube_cache")
        os.makedirs(cache_dir, exist_ok=True)
        cache_path = os.path.join(cache_dir, f"{video_id}.txt")

        if execution_count > 1 and os.path.exists(cache_path):
            with open(cache_path, "r", encoding="utf-8") as f:
                return (f.read(),)

        try:
            video_url = f"https://www.googleapis.com/youtube/v3/videos?part=snippet&id={video_id}&key={api_key}"
            video_data = requests.get(video_url).json()
            if not video_data["items"]:
                return ("⚠️ Error: Video not found or invalid ID.",)

            snippet = video_data["items"][0]["snippet"]
            title = snippet["title"]
            channel = snippet["channelTitle"]
            published = snippet["publishedAt"][:10]
            description = snippet.get("description", "").strip()

            formatted = f" Title: {title}\n"
            if include_dates:
                formatted += f" Date: {published} | Channel: {channel}\n"
            else:
                formatted += f" Channel: {channel}\n"
            formatted += f"\n{description}\n\n Comments:\n"

            # Fetch comments
            comments_url = (
                f"https://www.googleapis.com/youtube/v3/commentThreads"
                f"?part=snippet&videoId={video_id}&maxResults=100&textFormat=plainText&key={api_key}"
            )
            total_comments = 0
            next_page = None

            while total_comments < max_comments:
                url = comments_url + (f"&pageToken={next_page}" if next_page else "")
                comment_data = requests.get(url).json()
                for item in comment_data.get("items", []):
                    if total_comments >= max_comments:
                        break
                    c = item["snippet"]["topLevelComment"]["snippet"]
                    author = c.get("authorDisplayName", "Anonymous")
                    text = c.get("textDisplay", "").replace("\n", " ").strip()
                    date = c.get("publishedAt", "")[:10]

                    if include_dates:
                        formatted += f"- {author} ({date}): {text}\n"
                    else:
                        formatted += f"- {author}: {text}\n"
                    total_comments += 1

                next_page = comment_data.get("nextPageToken")
                if not next_page:
                    break

            with open(cache_path, "w", encoding="utf-8") as f:
                f.write(formatted)

            return (formatted,)
        except Exception as e:
            return (f"❌ Failed to fetch or parse YouTube data: {str(e)}",)

    def _extract_video_id(self, url_or_id):
        if len(url_or_id) == 11 and url_or_id.isalnum():
            return url_or_id  # already ID
        try:
            parsed = urlparse(url_or_id)
            if parsed.hostname in ["youtu.be"]:
                return parsed.path.lstrip("/")
            if "youtube" in parsed.hostname:
                qs = parse_qs(parsed.query)
                return qs.get("v", [None])[0]
        except:
            pass
        return None

    def _load_api_key(self):
        key_path = os.path.join(os.path.dirname(__file__), "youtube_api_key.txt")
        if not os.path.exists(key_path):
            return None
        with open(key_path, "r") as f:
            for line in f:
                if line.startswith("key="):
                    return line.split("=", 1)[1].strip()
        return None
