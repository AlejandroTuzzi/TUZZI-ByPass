# TUZZI-ByPass - Custom Node
# Author: Alejandro Tuzzi
# Website: https://www.tuzzi.es
# Contact: alejandro@tuzzi.es
# License: GNU General Public License v3.0

import os
import re
import requests
from bs4 import BeautifulSoup

class TVTropesScraper:
    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "url": ("STRING", {"multiline": False}),
                "execute": ("INT", {"default": 1, "min": 0, "max": 1}),
            },
        }

    RETURN_TYPES = ("STRING",)
    RETURN_NAMES = ("article_text",)
    FUNCTION = "scrape"
    CATEGORY = "TUZZI-ByPass"

    def scrape(self, url, execute):
        if execute != 1:
            return ("[Execution Skipped]",)

        cache_dir = "tvtropes_cache"
        os.makedirs(cache_dir, exist_ok=True)
        safe_name = re.sub(r'[^a-zA-Z0-9_-]', '_', url)
        filename = os.path.join(cache_dir, f"{safe_name}.html")

        if os.path.exists(filename):
            with open(filename, "r", encoding="utf-8") as f:
                html = f.read()
        else:
            response = requests.get(url)
            if response.status_code != 200:
                return (f"Error downloading article: {response.status_code}",)
            html = response.text
            with open(filename, "w", encoding="utf-8") as f:
                f.write(html)

        soup = BeautifulSoup(html, "html.parser")

        title_tag = soup.find("meta", {"property": "og:title"})
        title = title_tag["content"] if title_tag else "Unknown Title"

        main = soup.find("div", class_="article-content")
        if not main:
            return (f"❌ Could not find main content in {url}",)

        sections = []
        for elem in main.find_all(["p", "h2", "h3"], recursive=True):
            text = elem.get_text(strip=True, separator=" ")
            if text and not text.lower().startswith("advertisement"):
                sections.append(text)

        content = f"Trope: {title}\n\n" + "\n\n".join(sections)
        content += f"\n\nOriginal article: {url}"
        return (content,)
