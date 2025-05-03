# TUZZI-ByPass - Custom Node (versión mejorada)
# Author: Alejandro Tuzzi
# Website: https://www.tuzzi.es
# Contact: alejandro@tuzzi.es
# License: GNU General Public License v3.0

import os
import random
import json
from PIL import Image

class DirectoryImagePromptReader:
    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "image_directory": ("STRING", {"default": "input_images"}),
                "allow_subfolders": ("BOOLEAN", {"default": False}),
                "random_order": ("BOOLEAN", {"default": False}),
                "manual_filename": ("STRING", {"default": ""}),
            }
        }

    RETURN_TYPES = ("IMAGE", "STRING", "STRING")
    RETURN_NAMES = ("image", "prompt", "filename")
    FUNCTION = "load_image_and_prompt"
    CATEGORY = "TUZZI-ByPass"

    def __init__(self):
        self.cache_file = os.path.join(os.getcwd(), "tuzzi_cache", "directory_image_prompt_plus.json")
        os.makedirs(os.path.dirname(self.cache_file), exist_ok=True)
        self.state = {"index": 0, "last_dir": "", "shuffled": []}
        self._load_state()

    def _load_state(self):
        if os.path.exists(self.cache_file):
            try:
                with open(self.cache_file, "r", encoding="utf-8") as f:
                    self.state = json.load(f)
            except:
                pass

    def _save_state(self):
        with open(self.cache_file, "w", encoding="utf-8") as f:
            json.dump(self.state, f)

    def _collect_images(self, path, recursive):
        valid_ext = (".jpg", ".jpeg", ".png", ".webp")
        file_list = []
        for root, _, files in os.walk(path):
            for f in files:
                if f.lower().endswith(valid_ext):
                    file_list.append(os.path.join(root, f))
            if not recursive:
                break
        return sorted(file_list)

    def _find_prompt(self, image_path):
        folder = os.path.dirname(image_path)
        name = os.path.basename(image_path)
        txt_file = os.path.join(folder, "prompts.txt")
        if not os.path.exists(txt_file):
            return "image without text description"
        with open(txt_file, "r", encoding="utf-8") as f:
            for line in f:
                if line.lower().startswith(name.lower() + ":"):
                    return line.split(":", 1)[1].strip() or "image without text description"
        return "image without text description"

    def load_image_and_prompt(self, image_directory, allow_subfolders, random_order, manual_filename):
        image_paths = self._collect_images(image_directory, allow_subfolders)
        if not image_paths:
            return (None, "No images found", "")

        if self.state["last_dir"] != image_directory:
            self.state = {"index": 0, "last_dir": image_directory, "shuffled": []}

        # Si manual_filename está escrito, forzar usarlo
        if manual_filename:
            selected = os.path.join(image_directory, manual_filename)
            if not os.path.exists(selected):
                return (None, f"Manual file not found: {manual_filename}", manual_filename)
        else:
            if random_order:
                if not self.state["shuffled"]:
                    self.state["shuffled"] = random.sample(image_paths, len(image_paths))
                selected = self.state["shuffled"][self.state["index"] % len(self.state["shuffled"])]
            else:
                selected = image_paths[self.state["index"] % len(image_paths)]

            self.state["index"] = (self.state["index"] + 1) % len(image_paths)
            self._save_state()

        image = Image.open(selected).convert("RGB")
        image_tensor = image_to_tensor(image)
        prompt = self._find_prompt(selected)
        filename = os.path.basename(selected)

        return (image_tensor, prompt, filename)

    @classmethod
    def IS_CHANGED(cls, **kwargs):
        import time
        return time.time()


def image_to_tensor(pil_image):
    import numpy as np
    import torch
    array = np.asarray(pil_image).astype(np.float32) / 255.0
    tensor = torch.from_numpy(array).unsqueeze(0)
    return tensor
