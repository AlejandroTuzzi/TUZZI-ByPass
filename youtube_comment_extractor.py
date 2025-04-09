# TUZZI-ByPass - Custom Node
# Author: Alejandro Tuzzi
# Website: https://www.tuzzi.es
# Contact: alejandro@tuzzi.es
# License: GNU General Public License v3.0

import os
import re
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
                "include_description": ("BOOLEAN", {"default": True}),
                "remove_emojis": ("BOOLEAN", {"default": True}),
                "include_replies": ("BOOLEAN", {"default": False}),
                "max_comments": ("INT", {"default": 100, "min": 1, "max": 500}),
            }
        }

    RETURN_TYPES = ("STRING",)
    RETURN_NAMES = ("formatted_output",)
    FUNCTION = "extract"
    CATEGORY = "TUZZI-ByPass"

    def extract(self, youtube_url_or_id, execution_count, include_dates, include_description, remove_emojis, include_replies, max_comments):
        api_key = self._load_api_key()
        if not api_key:
            return ("⚠️ Error: No API key found. Make sure 'youtube_api_key.txt' exists.",)

        video_id = self._extract_video_id(youtube_url_or_id)
        if not video_id:
            return ("⚠️ Error: Could not extract video ID from the input.",)

        cache_dir = os.path.join(os.getcwd(), "youtube_cache")
        os.makedirs(cache_dir, exist_ok=True)
        cache_path = os.path.join(cache_dir, f"{video_id}_{include_dates}_{include_description}_{remove_emojis}_{include_replies}.txt")

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
            
            # Clean text if enabled
            if remove_emojis:
                title = self._remove_emoji(title)
                channel = self._remove_emoji(channel)
                description = self._remove_emoji(description)

            formatted = f" Title: {title}\n"
            if include_dates:
                formatted += f" Date: {published} | Channel: {channel}\n"
            else:
                formatted += f" Channel: {channel}\n"
                
            if include_description:
                formatted += f"\n{description}\n"
                
            formatted += "\n Comments:\n"

            # Fetch comments - Add parameter to only fetch top-level comments when include_replies is False
            comments_url = (
                f"https://www.googleapis.com/youtube/v3/commentThreads"
                f"?part=snippet&videoId={video_id}&maxResults=100&textFormat=plainText"
            )
            
            # If not including replies, we're only interested in top-level comments
            if not include_replies:
                # Set up API to fetch only top-level comments
                comments_url += "&order=relevance"
            
            comments_url += f"&key={api_key}"
            
            total_comments = 0
            next_page = None

            while total_comments < max_comments:
                url = comments_url + (f"&pageToken={next_page}" if next_page else "")
                comment_data = requests.get(url).json()
                
                for item in comment_data.get("items", []):
                    if total_comments >= max_comments:
                        break
                    
                    # Process top-level comment
                    c = item["snippet"]["topLevelComment"]["snippet"]
                    author = c.get("authorDisplayName", "Anonymous")
                    text = c.get("textDisplay", "").replace("\n", " ").strip()
                    date = c.get("publishedAt", "")[:10]
                    
                    # Clean text if enabled
                    if remove_emojis:
                        author = self._remove_emoji(author)
                        text = self._remove_emoji(text)

                    if include_dates:
                        formatted += f"- {author} ({date}): {text}\n"
                    else:
                        formatted += f"- {author}: {text}\n"
                    total_comments += 1
                    
                    # Process replies if requested
                    if include_replies and item["snippet"]["totalReplyCount"] > 0:
                        # Need to make an additional request to get the replies
                        replies_url = (
                            f"https://www.googleapis.com/youtube/v3/comments"
                            f"?part=snippet&parentId={item['id']}&textFormat=plainText&maxResults=50&key={api_key}"
                        )
                        try:
                            replies_data = requests.get(replies_url).json()
                            for reply in replies_data.get("items", []):
                                if total_comments >= max_comments:
                                    break
                                
                                r = reply["snippet"]
                                r_author = r.get("authorDisplayName", "Anonymous")
                                r_text = r.get("textDisplay", "").replace("\n", " ").strip()
                                r_date = r.get("publishedAt", "")[:10]
                                
                                if remove_emojis:
                                    r_author = self._remove_emoji(r_author)
                                    r_text = self._remove_emoji(r_text)
                                
                                if include_dates:
                                    formatted += f"  └ {r_author} ({r_date}): {r_text}\n"
                                else:
                                    formatted += f"  └ {r_author}: {r_text}\n"
                                total_comments += 1
                        except Exception as e:
                            formatted += f"  └ Error fetching replies: {str(e)}\n"

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
        
    def _remove_emoji(self, text):
        if not text:
            return text
            
        # Patrón para detectar emojis y otros caracteres especiales Unicode
        emoji_pattern = re.compile(
            "["
            "\U0001F600-\U0001F64F"  # emoticones
            "\U0001F300-\U0001F5FF"  # símbolos y pictogramas
            "\U0001F680-\U0001F6FF"  # símbolos de transporte y mapas
            "\U0001F700-\U0001F77F"  # símbolos alquímicos
            "\U0001F780-\U0001F7FF"  # símbolos geométricos
            "\U0001F800-\U0001F8FF"  # flechas suplementarias
            "\U0001F900-\U0001F9FF"  # símbolos suplementarios y pictogramas
            "\U0001FA00-\U0001FA6F"  # símbolos de ajedrez
            "\U0001FA70-\U0001FAFF"  # símbolos varios
            "\U00002702-\U000027B0"  # dingbats
            "\U000024C2-\U0001F251" 
            "]+", flags=re.UNICODE)
            
        # Limpiar el texto de emojis
        return emoji_pattern.sub(r'', text)