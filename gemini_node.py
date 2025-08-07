# TUZZI-ByPass - Custom Node
# Author: Alejandro Tuzzi
# Website: https://www.tuzzi.es
# Contact: alejandro@tuzzi.es
# License: GNU General Public License v3.0
# Updated by: Gemini (agosto 2025)

import os
import re
import json
import google.generativeai as genai
import folder_paths

# ────────────────────────────────────────────────────────────
#  Helper: leer la clave de la API
# ────────────────────────────────────────────────────────────
def get_api_key():
    """Lee la clave de la API de Gemini desde gemini_api_key.txt."""
    key_file = os.path.join(os.path.dirname(__file__), "gemini_api_key.txt")
    if not os.path.exists(key_file):
        return None
    with open(key_file, "r", encoding="utf-8") as f:
        return f.read().strip()


# ────────────────────────────────────────────────────────────
#  Recuperar modelos disponibles (con fallback)
# ────────────────────────────────────────────────────────────
def get_available_models():
    """Devuelve los modelos de Gemini que soportan 'generateContent'."""
    print("TUZZI-ByPass: Fetching Gemini models …")
    DEFAULT_MODELS = [
        "gemini-1.5-pro-latest",
        "gemini-1.5-flash-latest",
        "gemini-1.0-pro",
    ]

    api_key = get_api_key()
    if not api_key:
        print(
            "TUZZI-ByPass FATAL: gemini_api_key.txt no encontrado o vacío. "
            "Usando lista de modelos por defecto."
        )
        return DEFAULT_MODELS

    try:
        genai.configure(api_key=api_key)
        models = [
            m.name.replace("models/", "")
            for m in genai.list_models()
            if "generateContent" in m.supported_generation_methods
        ]
        if not models:
            print(
                "TUZZI-ByPass WARNING: No se encontraron modelos compatibles. "
                "Usando lista por defecto."
            )
            return DEFAULT_MODELS

        print(f"TUZZI-ByPass SUCCESS: {len(models)} modelos encontrados.")
        return sorted(models)

    except Exception as e:
        print(f"TUZZI-ByPass ERROR: {e}. Usando lista por defecto.")
        return DEFAULT_MODELS


AVAILABLE_MODELS = get_available_models()


# ────────────────────────────────────────────────────────────
#  Nodo principal
# ────────────────────────────────────────────────────────────
class GeminiNode:
    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "model_name": (AVAILABLE_MODELS,),
                "project_name": ("STRING", {"default": "default_project"}),
                "prompt_instruction": (
                    "STRING",
                    {"multiline": True, "default": "You are a helpful AI assistant."},
                ),
                "user_input": (
                    "STRING",
                    {
                        "multiline": True,
                        "default": "Describe a futuristic city in one paragraph.",
                    },
                ),
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
        self.memory_dir = os.path.join(
            folder_paths.get_temp_directory(), "gemini_memory"
        )
        os.makedirs(self.memory_dir, exist_ok=True)

    # ────────────────────────────────────────────────────────
    #  Utilidades internas
    # ────────────────────────────────────────────────────────
    def _safe_get_ai(self, entry):
        """
        Compatibilidad con historiales antiguos:
        • Nuevo formato ⇒ str con la respuesta de la IA.
        • Formato viejo ⇒ dict {"user": "...", "ai": "..."}.
        """
        return entry if isinstance(entry, str) else entry.get("ai", "")

    def _format_history_for_prompt(self, history_list):
        """Devuelve solo las últimas respuestas de la IA como contexto."""
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
        """Prepara el historial para el nodo 'Show Text'."""
        if not history_list:
            return f"Project: {project_name}\n\nNo history yet."

        log_lines = [f"Project: {project_name}\n"]
        for idx, entry in enumerate(history_list, 1):
            log_lines.append(f"--- Output {idx} ---")
            log_lines.append(self._safe_get_ai(entry) + "\n")
        return "\n".join(log_lines)

    # ────────────────────────────────────────────────────────
    #  Ejecución principal
    # ────────────────────────────────────────────────────────
    def run(self, model_name, project_name, prompt_instruction, user_input):
        if not self.api_key:
            return ("[Error]: gemini_api_key.txt not found or is empty.", "")

        # Nombre de archivo seguro
        sane_project = re.sub(r'[\\/*?:"<>|]', "", project_name).strip() or "default_project"
        memory_file = os.path.join(self.memory_dir, f"{sane_project}.json")

        # Cargar memoria existente (si hay)
        history = []
        if os.path.exists(memory_file):
            try:
                with open(memory_file, "r", encoding="utf-8") as f:
                    history = json.load(f)
            except Exception as e:
                print(
                    f"TUZZI-ByPass Warning: No se pudo leer el historial de "
                    f"'{sane_project}'. Se iniciará uno nuevo. Error: {e}"
                )

        # Construir prompt
        context = self._format_history_for_prompt(history)
        full_prompt = (
            f"SYSTEM INSTRUCTION: {prompt_instruction}\n\n"
            f"PREVIOUS AI OUTPUTS (context):\n{context}\n\n"
            f"CURRENT USER REQUEST: {user_input}"
        )

        print(
            f"TUZZI-ByPass: Generando respuesta para '{sane_project}' "
            f"con el modelo '{model_name}'."
        )

        try:
            genai.configure(api_key=self.api_key)
            model = genai.GenerativeModel(f"models/{model_name}")
            response = model.generate_content(full_prompt)
            output_text = response.text

            # ── Guardar SOLO la respuesta de la IA ──
            history.append(output_text)
            with open(memory_file, "w", encoding="utf-8") as f:
                json.dump(history, f, ensure_ascii=False, indent=4)

            memory_log_output = self._format_history_for_log(sane_project, history)
            return (output_text, memory_log_output)

        except Exception as e:
            error_msg = f"[Error with model {model_name}]: {e}"
            print(error_msg)
            return (error_msg, self._format_history_for_log(sane_project, history))
