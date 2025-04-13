# TUZZI-ByPass - Custom Node
# Author: Alejandro Tuzzi
# Website: https://www.tuzzi.es
# Contact: alejandro@tuzzi.es
# License: GNU General Public License v3.0

import os
import hashlib
import json
import inspect
import time
import re

# Variable global para debug
DEBUG = True

def debug_log(message):
    if DEBUG:
        timestamp = time.strftime("%Y-%m-%d %H:%M:%S")
        log_dir = os.path.join(os.getcwd(), "tuzzi_logs")
        os.makedirs(log_dir, exist_ok=True)
        log_file = os.path.join(log_dir, "sequential_reader_debug.log")
        with open(log_file, "a", encoding="utf-8") as f:
            f.write(f"[{timestamp}] {message}\n")

class SequentialTextReaderAuto:
    # Mantenemos los datos del estado en variables de clase estáticas
    _current_digest = None
    _line_index = 0
    _force_reset = False
    
    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "text_block": ("STRING", {"multiline": True}),
            }
        }

    RETURN_TYPES = ("STRING", "INT")
    RETURN_NAMES = ("selected_text", "line_number")
    FUNCTION = "read_line"
    CATEGORY = "TUZZI-ByPass"

    def __init__(self):
        self.cache_dir = os.path.join(os.getcwd(), "tuzzi_cache")
        os.makedirs(self.cache_dir, exist_ok=True)
        self.cache_file = os.path.join(self.cache_dir, "sequential_text_reader.json")
        
        # Cargar el estado desde el archivo de caché al inicializar
        self._load_state()
        
        debug_log(f"Inicializado nodo. Estado actual: digest={SequentialTextReaderAuto._current_digest}, índice={SequentialTextReaderAuto._line_index}")

    def _normalize_text(self, text):
        """Normaliza el texto para eliminar espacios en blanco, saltos de línea y otros caracteres que pueden variar sin cambiar el contenido real"""
        # Eliminar espacios extra, tabs, etc.
        text = re.sub(r'\s+', ' ', text)
        # Eliminar caracteres no visibles
        text = ''.join(char for char in text if char.isprintable())
        # Convertir a minúsculas para ignorer diferencias de mayúsculas/minúsculas
        text = text.lower()
        return text.strip()
    
    def _calculate_digest(self, text_block):
        """Calcula un digest basado en el contenido normalizado"""
        # Extraer solo las líneas para calcular un digest basado en el contenido real
        lines = [line.strip() for line in text_block.splitlines() if line.strip()]
        
        # Crear un digest basado en las primeras 5 líneas y el total de líneas
        digest_text = ""
        for i in range(min(5, len(lines))):
            digest_text += self._normalize_text(lines[i])[:50]  # Primeros 50 caracteres de cada línea
        
        digest_text += f"|total_lines:{len(lines)}"
        
        return hashlib.md5(digest_text.encode("utf-8")).hexdigest()
    
    def _load_state(self):
        if os.path.exists(self.cache_file):
            try:
                with open(self.cache_file, "r", encoding="utf-8") as f:
                    state = json.load(f)
                    SequentialTextReaderAuto._current_digest = state.get("digest")
                    SequentialTextReaderAuto._line_index = state.get("index", 0)
                    debug_log(f"Estado cargado desde caché: digest={SequentialTextReaderAuto._current_digest}, índice={SequentialTextReaderAuto._line_index}")
            except Exception as e:
                debug_log(f"Error al cargar estado: {str(e)}")
                # Si hay un error, mantenemos los valores predeterminados
                pass

    def _save_state(self):
        state = {
            "digest": SequentialTextReaderAuto._current_digest,
            "index": SequentialTextReaderAuto._line_index
        }
        try:
            with open(self.cache_file, "w", encoding="utf-8") as f:
                json.dump(state, f)
            debug_log(f"Estado guardado en caché: digest={state['digest']}, índice={state['index']}")
        except Exception as e:
            debug_log(f"Error al guardar estado: {str(e)}")

    def read_line(self, text_block):
        # Información para debug
        caller_frame = inspect.currentframe().f_back
        caller_info = f"llamado desde {caller_frame.f_code.co_filename}:{caller_frame.f_lineno}" if caller_frame else "origen desconocido"
        debug_log(f"read_line llamado ({caller_info})")
        
        # Preparar las líneas
        lines = [line.strip() for line in text_block.splitlines() if line.strip()]
        debug_log(f"Total de líneas: {len(lines)}")
        
        if not lines:
            debug_log("No hay líneas válidas, retornando vacío")
            return ("", 0)

        # Calcular el digest del texto actual
        current_digest = self._calculate_digest(text_block)
        debug_log(f"Digest del texto actual: {current_digest}")
        debug_log(f"Digest guardado anteriormente: {SequentialTextReaderAuto._current_digest}")

        # Si el texto cambió significativamente (digest diferente), reiniciamos el índice
        if current_digest != SequentialTextReaderAuto._current_digest or SequentialTextReaderAuto._force_reset:
            debug_log("El texto ha cambiado o se forzó reinicio. Reiniciando índice a 0")
            SequentialTextReaderAuto._current_digest = current_digest
            SequentialTextReaderAuto._line_index = 0
            SequentialTextReaderAuto._force_reset = False
        
        # Seleccionar la línea actual
        line_index = SequentialTextReaderAuto._line_index
        debug_log(f"Índice de línea actual: {line_index}")
        
        # Verificar que el índice esté dentro del rango válido
        if line_index >= len(lines):
            debug_log(f"Índice fuera de rango, reiniciando a 0")
            line_index = 0
            SequentialTextReaderAuto._line_index = 0
        
        # Obtener el texto de la línea actual
        selected_text = lines[line_index]
        debug_log(f"Texto seleccionado: '{selected_text}'")
        
        # Incrementar el índice para la próxima llamada
        SequentialTextReaderAuto._line_index = (line_index + 1) % len(lines)
        debug_log(f"Índice actualizado para próxima llamada: {SequentialTextReaderAuto._line_index}")
        
        # Guardar el estado actualizado
        self._save_state()
        
        # Retornar el texto seleccionado y el número de línea (base 1)
        return (selected_text, line_index + 1)

    @classmethod
    def IS_CHANGED(cls, **kwargs):
        # Este método se llama para verificar si el nodo necesita ejecutarse de nuevo
        # Siempre retornamos un valor diferente para forzar la ejecución
        return time.time()
    
    @classmethod
    def VALIDATE_INPUTS(cls, **kwargs):
        # Siempre validamos los inputs
        return True

# Para registrar el nodo en ComfyUI
NODE_CLASS_MAPPINGS = {
    "SequentialTextReaderAuto": SequentialTextReaderAuto
}

NODE_DISPLAY_NAME_MAPPINGS = {
    "SequentialTextReaderAuto": "Sequential Text Reader Auto"
}