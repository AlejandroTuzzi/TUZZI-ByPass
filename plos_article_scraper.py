# TUZZI-ByPass - Custom Node
# Author: Alejandro Tuzzi
# Website: https://www.tuzzi.es
# Contact: alejandro@tuzzi.es
# License: GNU General Public License v3.0

import os
import re
import requests
from bs4 import BeautifulSoup

class PlosArticleScraper:
    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "url": ("STRING", {"multiline": False}),
                "execute": ("INT", {"default": 1, "min": 0})
            },
        }

    RETURN_TYPES = ("STRING",)
    RETURN_NAMES = ("article_text",)
    FUNCTION = "scrape"
    CATEGORY = "TUZZI-ByPass"

    def scrape(self, url, execute):
        cache_dir = "plos_cache"
        os.makedirs(cache_dir, exist_ok=True)
        safe_name = re.sub(r'[^a-zA-Z0-9_-]', '_', url)
        filename = os.path.join(cache_dir, f"{safe_name}.html")

        # Si ya existe el archivo y no queremos ejecutar, devolvemos lo que ya tenemos
        if execute != 1:
            if os.path.exists(filename):
                with open(filename, "r", encoding="utf-8") as f:
                    html = f.read()
            else:
                return ("[Execution Skipped - No cache available]",)
        else:
            response = requests.get(url)
            if response.status_code != 200:
                return (f"Error downloading article: {response.status_code}",)
            html = response.text
            with open(filename, "w", encoding="utf-8") as f:
                f.write(html)

        soup = BeautifulSoup(html, "html.parser")

        def get_meta(name):
            tag = soup.find("meta", {"name": name})
            return tag["content"].strip() if tag else None

        title = get_meta("citation_title") or "Unknown title"
        date = get_meta("citation_date") or "Unknown date"
        authors = [meta["content"] for meta in soup.find_all("meta", {"name": "citation_author"})]
        authors_str = ", ".join(authors) if authors else "Unknown authors"
        abstract = get_meta("citation_abstract") or ""

        # Extraer cuerpo completo del artículo desde <div id="artText"> o similar
        full_text = ""
        main_container = soup.find("div", id="artText") or soup.find("div", class_="article-text")
        if main_container:
            for elem in main_container.find_all(recursive=False):
                section_id = elem.get("id", "").lower()
                if any(skip in section_id for skip in ["references", "acknowledgments", "supporting", "figures", "tables"]):
                    continue
                if elem.name in ["h2", "h3", "p", "div", "section"]:
                    clean = elem.get_text(separator="\n", strip=True)
                    if clean:
                        full_text += clean + "\n\n"

        result = f"Title: {title}\nDate: {date}\nAuthors: {authors_str}\n\n"
        result += abstract + "\n\n" if abstract else ""
        result += full_text.strip()
        result += f"\n\nYou can consult the sources and attached documentation at the URL of the scientific journal: {url}"

        return (result,)