# TUZZI-ByPass - Custom Node
# Author: Alejandro Tuzzi
# Website: https://www.tuzzi.es
# Contact: alejandro@tuzzi.es
# License: GNU General Public License v3.0

import os
import requests
from datetime import datetime

class RedditPostExtractor:
    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "reddit_url_path": ("STRING", {"multiline": False}),
                "execution_count": ("INT", {"default": 1, "min": 1}),
            }
        }

    RETURN_TYPES = ("STRING",)
    RETURN_NAMES = ("formatted_output",)
    FUNCTION = "extract"
    CATEGORY = "TUZZI-ByPass"

    def extract(self, reddit_url_path, execution_count):
        # Creamos un nombre de archivo cache basado en la URL
        cache_dir = os.path.join(os.getcwd(), "reddit_cache")
        os.makedirs(cache_dir, exist_ok=True)

        safe_filename = reddit_url_path.replace("/", "_").replace("?", "").replace("=", "")
        cache_path = os.path.join(cache_dir, safe_filename + ".txt")

        # Si ya hay resultado en caché y no es la primera ejecución
        if execution_count > 1 and os.path.exists(cache_path):
            with open(cache_path, "r", encoding="utf-8") as f:
                return (f.read(),)

        # Si es la primera ejecución o no hay caché aún
        base_url = "https://www.reddit.com/"
        full_url = base_url + reddit_url_path.strip().rstrip("/") + ".json"
        headers = {"User-Agent": "TUZZI-ByPass/1.0"}

        try:
            response = requests.get(full_url, headers=headers)
            if response.status_code != 200:
                return (f" Error: Post not found or invalid URL. ({response.status_code})",)

            data = response.json()
            post_info = data[0]["data"]["children"][0]["data"]
            title = post_info["title"]
            author = post_info["author"]
            created_utc = datetime.utcfromtimestamp(post_info["created_utc"]).strftime("%Y-%m-%d")
            selftext = post_info.get("selftext", "").strip()

            formatted = f" Title: {title}\n Date: {created_utc} | Author: {author}\n\n{selftext}\n\n Comments:\n"

            comments = data[1]["data"]["children"]
            for c in comments:
                if c["kind"] != "t1":
                    continue
                comment_data = c["data"]
                comment_author = comment_data.get("author", "[deleted]")
                comment_date = datetime.utcfromtimestamp(comment_data["created_utc"]).strftime("%Y-%m-%d")
                comment_body = comment_data.get("body", "").strip()
                formatted += f"- {comment_author} ({comment_date}): {comment_body}\n"

            # Guardamos en caché
            with open(cache_path, "w", encoding="utf-8") as f:
                f.write(formatted)

            return (formatted,)
        except Exception as e:
            return (f" Failed to fetch or parse Reddit post: {str(e)}",)
