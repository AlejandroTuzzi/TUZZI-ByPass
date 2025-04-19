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
                "download_path": ("STRING", {"default": "images"})
            }
        }

    RETURN_TYPES = ("STRING",)
    RETURN_NAMES = ("processed_text",)
    FUNCTION = "extract_and_save"
    CATEGORY = "TUZZI-ByPass"

    def extract_and_save(self, text, download_path):
        # Crear carpeta si no existe
        target_dir = os.path.join(os.getcwd(), download_path)
        os.makedirs(target_dir, exist_ok=True)

        # Vamos a buscar patrones de comentarios y asociar las imágenes con autores
        processed_text = text
        
        # Mantener un registro de URLs ya procesadas para evitar duplicados
        processed_urls = set()
        
        # Patrón para identificar líneas de comentarios con autor
        comment_pattern = r'- ([^:(\n]+)(?:\s*\([^)]*\))?\s*:(.*?)(?=(?:- [^:(\n]+(?:\s*\([^)]*\))?\s*:|\Z))'
        
        # Patrón para buscar enlaces de imágenes
        image_pattern = r'(https?://[^\s]+?\.(?:png|jpg|jpeg|gif|webp)(?:\?[^\s]*)?)'
        
        # Buscar todos los comentarios
        matches = re.finditer(comment_pattern, text, re.DOTALL)
        
        # Para cada comentario, procesar las URLs de imágenes
        for match in enumerate(matches):
            author = match[1].group(1).strip()
            comment_text = match[1].group(2)
            
            # Buscar URLs de imágenes en este comentario
            image_urls = re.findall(image_pattern, comment_text)
            
            comment_processed = comment_text
            
            # Procesar cada URL de imagen encontrada
            for img_idx, url in enumerate(image_urls):
                # Saltarse URLs duplicadas
                if url in processed_urls:
                    # Reemplazar la URL con "image by [Autor]" para mantener consistencia
                    comment_processed = comment_processed.replace(url, f"[image by {author}]")
                    continue
                
                processed_urls.add(url)
                
                try:
                    # Descargar la imagen
                    response = requests.get(url, timeout=10)
                    if response.status_code == 200:
                        # Crear un nombre de archivo coincidente con el texto de reemplazo
                        ext = os.path.splitext(urlparse(url).path)[1].split("?")[0]
                        if not ext:
                            ext = ".jpg"  # Extensión por defecto si no se puede determinar
                        
                        # Sanitizar el nombre del autor para el nombre de archivo
                        safe_author = re.sub(r'[\\/*?:"<>|]', "", author)
                        safe_author = safe_author.replace(' ', '_')
                        
                        # Usar un índice para evitar sobrescribir archivos si un autor tiene múltiples imágenes
                        filename = f"image_by_{safe_author}_{img_idx+1}{ext}"
                        save_path = os.path.join(target_dir, filename)
                        
                        # Guardar la imagen
                        with open(save_path, "wb") as f:
                            f.write(response.content)
                        
                        # Reemplazar la URL con "image by [Autor]"
                        comment_processed = comment_processed.replace(url, f"[image by {author}]")
                        
                except Exception as e:
                    print(f"❌ Error downloading {url}: {str(e)}")
            
            # Reemplazar el comentario original con el procesado
            processed_comment = f"- {author}{match[1].group(0)[len(author)+1:].replace(comment_text, comment_processed)}"
            processed_text = processed_text.replace(match[1].group(0), processed_comment)
        
        # Manejar las URLs de imágenes que aparecen fuera del patrón de comentarios
        remaining_urls = re.findall(image_pattern, processed_text)
        for idx, url in enumerate(remaining_urls):
            # Saltarse URLs duplicadas
            if url in processed_urls:
                processed_text = processed_text.replace(url, "[image by unknown]")
                continue
                
            processed_urls.add(url)
            
            try:
                # Verificar si la URL todavía está en el texto y no ha sido reemplazada
                if url in processed_text:
                    # Descargar la imagen
                    response = requests.get(url, timeout=10)
                    if response.status_code == 200:
                        ext = os.path.splitext(urlparse(url).path)[1].split("?")[0]
                        if not ext:
                            ext = ".jpg"
                        filename = f"image_by_unknown_{idx+1}{ext}"
                        save_path = os.path.join(target_dir, filename)
                        
                        with open(save_path, "wb") as f:
                            f.write(response.content)
                        
                        # Reemplazar la URL con un texto genérico
                        processed_text = processed_text.replace(url, "[image by unknown]")
            except Exception as e:
                print(f"❌ Error downloading {url}: {str(e)}")

        return (processed_text,)