# TUZZI-ByPass - Custom Node
# Author: Alejandro Tuzzi
# Website: https://www.tuzzi.es
# Contact: alejandro@tuzzi.es
# License: GNU General Public License v3.0
# Updated: agosto 2025 – añade memoria de conversación y autodescubrimiento de modelos

import os
import re
import json
import requests
import folder_paths   # carpeta temporal del runtime

# ────────────────────────────────────────────────────────────
#  API-Key helper
# ────────────────────────────────────────────────────────────
def get_api_key():
    key_path = os.path.join(os.path.dirname(__file__), "groq_api_key.txt")
    if not os.path.exists(key_path):
        return None
    with open(key_path, "r", encoding="utf-8") as f:
        return f.read().strip().replace("key=", "")

# ────────────────────────────────────────────────────────────
#  Leer modelos disponibles desde Groq
# ────────────────────────────────────────────────────────────
def get_available_models():
    """Devuelve la lista de IDs de modelos disponibles en Groq."""
    print("GroqNode: Fetching models from Groq API …")
    DEFAULT_MODELS = [
        "mixtral-8x7b-32768",
        "llama3-8b-8192",
        "llama3-70b-8192",
    ]

    api_key = get_api_key()
    if not api_key:
        print(
            "GroqNode WARNING: groq_api_key.txt no encontrado o vacío. "
            "Usando lista de modelos por defecto."
        )
        return DEFAULT_MODELS

    try:
        url = "https://api.groq.com/openai/v1/models"
        headers = {"Authorization": f"Bearer {api_key}"}
        resp = requests.get(url, headers=headers, timeout=30)

        if resp.status_code != 200:
            print(
                f"GroqNode WARNING: No se pudo obtener la lista de modelos "
                f"(HTTP {resp.status_code}). Usando lista por defecto."
            )
            return DEFAULT_MODELS

        data = resp.json().get("data", [])
        models = sorted(m["id"] for m in data if isinstance(m, dict) and m.get("id"))

        if not models:
            print("GroqNode WARNING: Lista vacía. Usando lista por defecto.")
            return DEFAULT_MODELS

        print(f"GroqNode SUCCESS: {len(models)} modelos encontrados.")
        return models

    except Exception as e:
        print(f"GroqNode ERROR: {e}. Usando lista por defecto.")
        return DEFAULT_MODELS

AVAILABLE_MODELS = get_available_models()


# ────────────────────────────────────────────────────────────
#  Nodo principal
# ────────────────────────────────────────────────────────────
class GroqNode:
    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "model_name": (AVAILABLE_MODELS,),
                "project_name": ("STRING", {"default": "default_project"}),
                "system_instruction": ("STRING", {"multiline": True}),
                "user_prompt": ("STRING", {"multiline": True}),
                "should_generate": ("INT", {"default": 1, "min": 0}),
            }
        }

    RETURN_TYPES = ("STRING", "STRING")
    RETURN_NAMES = ("output", "memory_log")
    FUNCTION = "run"
    CATEGORY = "TUZZI-ByPass"

    # ────────────────────────────────────────────────────────
    #  Inicialización
    # ────────────────────────────────────────────────────────
    def __init__(self):
        self.api_key = get_api_key()
        if not self.api_key:
            raise FileNotFoundError("groq_api_key.txt not found or empty.")

        # Directorio para historiales
        self.memory_dir = os.path.join(folder_paths.get_temp_directory(), "groq_memory")
        os.makedirs(self.memory_dir, exist_ok=True)

    # ────────────────────────────────────────────────────────
    #  Utilidades internas
    # ────────────────────────────────────────────────────────
    @staticmethod
    def _safe_get_ai(entry):
        """Compatibilidad con historiales antiguos (dict) y nuevos (str)."""
        return entry if isinstance(entry, str) else entry.get("ai", "")

    def _format_history_for_prompt(self, history_list):
        """Devuelve los últimos outputs de la IA como contexto."""
        if not history_list:
            return "No previous AI outputs."

        MAX_TURNS = 5
        recent = history_list[-MAX_TURNS:]
        lines = []
        for idx, entry in enumerate(recent, 1):
            lines.append(f"--- Output {idx} ---")
            lines.append(self._safe_get_ai(entry))
        return "\n".join(lines)

    def _format_history_for_log(self, project_name, history_list):
        """Genera texto legible para un nodo 'Show Text'."""
        if not history_list:
            return f"Project: {project_name}\n\nNo history yet."

        log = [f"Project: {project_name}\n"]
        for idx, entry in enumerate(history_list, 1):
            log.append(f"--- Output {idx} ---")
            log.append(self._safe_get_ai(entry) + "\n")
        return "\n".join(log)

    # ────────────────────────────────────────────────────────
    #  Ejecución principal
    # ────────────────────────────────────────────────────────
    def run(
        self,
        model_name,
        project_name,
        system_instruction,
        user_prompt,
        should_generate,
    ):
        # Permitir que el grafo continúe sin generar (compatibilidad)
        if should_generate != 1:
            return (user_prompt + "\u200b", "")

        # Nombre de archivo seguro
        sane_project = re.sub(r'[\\/*?:"<>|]', "", project_name).strip() or "default_project"
        memory_file = os.path.join(self.memory_dir, f"{sane_project}.json")

        # Cargar historial
        history = []
        if os.path.exists(memory_file):
            try:
                with open(memory_file, "r", encoding="utf-8") as f:
                    history = json.load(f)
            except Exception as e:
                print(
                    f"GroqNode WARNING: No se pudo leer historial de '{sane_project}'. "
                    f"Se inicia uno nuevo. Error: {e}"
                )

        # Construir prompt con historial de IA
        context = self._format_history_for_prompt(history)
        messages = [
            {"role": "system", "content": system_instruction},
            {"role": "system", "content": f"PREVIOUS AI OUTPUTS:\n{context}"},
            {"role": "user", "content": user_prompt},
        ]

        try:
            url = "https://api.groq.com/openai/v1/chat/completions"
            headers = {
                "Authorization": f"Bearer {self.api_key}",
                "Content-Type": "application/json",
            }
            payload = {
                "model": model_name,
                "messages": messages,
                "temperature": 0.7,
            }

            response = requests.post(url, headers=headers, json=payload, timeout=60)
            if response.status_code == 200:
                result = response.json()
                output_text = result["choices"][0]["message"]["content"].strip()

                # Guardar SOLO la respuesta de la IA
                history.append(output_text)
                with open(memory_file, "w", encoding="utf-8") as f:
                    json.dump(history, f, ensure_ascii=False, indent=4)

                memory_log = self._format_history_for_log(sane_project, history)
                return (output_text, memory_log)

            err = f"[Groq Error {response.status_code}]: {response.text}"
            memory_log = self._format_history_for_log(sane_project, history)
            return (err, memory_log)

        except Exception as e:
            err = f"[Exception]: {e}"
            memory_log = self._format_history_for_log(sane_project, history)
            return (err, memory_log)
