# TUZZI-ByPass - Custom Node
# Author: Alejandro Tuzzi
# Website: https://www.tuzzi.es
# Contact: alejandro@tuzzi.es
# License: GNU General Public License v3.0

import os
import re
import requests
from urllib.parse import urlparse

class ImageExtractorSaver:
    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "text": ("STRING", {"multiline": True}),
                "download_path": ("STRING", {"default": "images"}),
                "should_extract": ("INT", {"default": 1, "min": 0, "max": 1})
            }
        }

    RETURN_TYPES = ("STRING",)
    RETURN_NAMES = ("processed_text",)
    FUNCTION = "extract_and_save"
    CATEGORY = "TUZZI-ByPass"

    def extract_and_save(self, text, download_path, should_extract):
        if should_extract != 1:
            return (text,)

        target_dir = os.path.join(os.getcwd(), download_path)
        os.makedirs(target_dir, exist_ok=True)

        processed_text = text
        processed_urls = set()

        comment_pattern = r'- ([^:(\n]+)(?:\s*\([^)]*\))?\s*:(.*?)(?=(?:- [^:(\n]+(?:\s*\([^)]*\))?\s*:|\Z))'
        image_pattern = r'(https?://[^\s]+?\.(?:png|jpg|jpeg|gif|webp)(?:\?[^\s]*)?)'

        matches = re.finditer(comment_pattern, text, re.DOTALL)

        for match in enumerate(matches):
            author = match[1].group(1).strip()
            comment_text = match[1].group(2)
            image_urls = re.findall(image_pattern, comment_text)
            comment_processed = comment_text

            for img_idx, url in enumerate(image_urls):
                if url in processed_urls:
                    comment_processed = comment_processed.replace(url, f"[image by {author}]")
                    continue
                processed_urls.add(url)
                try:
                    response = requests.get(url, timeout=10)
                    if response.status_code == 200:
                        ext = os.path.splitext(urlparse(url).path)[1].split("?")[0]
                        if not ext:
                            ext = ".jpg"
                        safe_author = re.sub(r'[\\/*?:"<>|]', "", author).replace(' ', '_')
                        filename = f"image_by_{safe_author}_{img_idx+1}{ext}"
                        save_path = os.path.join(target_dir, filename)
                        with open(save_path, "wb") as f:
                            f.write(response.content)
                        comment_processed = comment_processed.replace(url, f"[image by {author}]")
                except Exception as e:
                    print(f"❌ Error downloading {url}: {str(e)}")

            processed_comment = f"- {author}{match[1].group(0)[len(author)+1:].replace(comment_text, comment_processed)}"
            processed_text = processed_text.replace(match[1].group(0), processed_comment)

        remaining_urls = re.findall(image_pattern, processed_text)
        for idx, url in enumerate(remaining_urls):
            if url in processed_urls:
                processed_text = processed_text.replace(url, "[image by unknown]")
                continue
            processed_urls.add(url)
            try:
                if url in processed_text:
                    response = requests.get(url, timeout=10)
                    if response.status_code == 200:
                        ext = os.path.splitext(urlparse(url).path)[1].split("?")[0]
                        if not ext:
                            ext = ".jpg"
                        filename = f"image_by_unknown_{idx+1}{ext}"
                        save_path = os.path.join(target_dir, filename)
                        with open(save_path, "wb") as f:
                            f.write(response.content)
                        processed_text = processed_text.replace(url, "[image by unknown]")
            except Exception as e:
                print(f"❌ Error downloading {url}: {str(e)}")

        return (processed_text,)
