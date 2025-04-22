# TUZZI-ByPass - Custom Node
# Author: Alejandro Tuzzi
# Website: https://www.tuzzi.es
# Contact: alejandro@tuzzi.es
# License: GNU General Public License v3.0

import os
import re
import requests
from bs4 import BeautifulSoup

class DataloungeScraper:
    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "url": ("STRING", {"multiline": False}),
                "execute": ("INT", {"default": 1, "min": 0, "max": 1}),
            },
        }

    RETURN_TYPES = ("STRING",)
    RETURN_NAMES = ("thread_text",)
    FUNCTION = "scrape"
    CATEGORY = "TUZZI-ByPass"

    def scrape(self, url, execute):
        cache_dir = "datalounge_cache"
        os.makedirs(cache_dir, exist_ok=True)
        safe_name = re.sub(r'[^a-zA-Z0-9_-]', '_', url)
        filename = os.path.join(cache_dir, f"{safe_name}.html")

        # Si ya existe el archivo y no se debe ejecutar, devolver el cache
        if execute != 1 and os.path.exists(filename):
            with open(filename, "r", encoding="utf-8") as f:
                html = f.read()
        elif execute == 1:
            response = requests.get(url)
            if response.status_code != 200:
                return (f"Error downloading thread: {response.status_code}",)
            html = response.text
            with open(filename, "w", encoding="utf-8") as f:
                f.write(html)
        else:
            return ("[Execution Skipped]",)

        soup = BeautifulSoup(html, "html.parser")

        title_tag = soup.find("title")
        title = title_tag.text.strip() if title_tag else "Unknown Title"

        posts = soup.find_all("div", class_="post")
        if not posts:
            return ("No posts found.",)

        thread = f"Thread: {title}\n\n"

        for post in posts:
            body = post.find("div", class_="post-body")
            author = post.find("span", class_="poster")
            author_name = author.text.strip() if author else "Anonymous"

            if not body:
                continue

            paragraphs = body.find_all("p")
            full_post = "\n".join(p.get_text(strip=True) for p in paragraphs if p.get_text(strip=True))

            if full_post:
                if author_name.lower() == "anonymous":
                    thread += f"** NEXT COMMENT **\n{full_post}\n\n"
                else:
                    thread += f"Comment by: {author_name}\n{full_post}\n\n"

        thread += f"Original thread: {url}"
        return (thread,)
