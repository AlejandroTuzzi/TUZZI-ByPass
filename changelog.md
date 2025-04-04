# 📜 TUZZI-ByPass - Changelog

Historial de cambios y actualizaciones del paquete de nodos personalizados TUZZI-ByPass para ComfyUI.

---

## [v1.0.0] - 2025-04-03

### 🆕 Nuevos nodos

- `Bypasser Switch`: Ruta condicional entre dos entradas de cualquier tipo.
- `Count Lines in String`: Cuenta cuántas líneas tiene un texto (ignora vacías).
- `Add Line Breaks to Text`: Agrega saltos de línea luego de cada punto, limpia líneas vacías.
- `Smart Line Breaks (by Word Count)`: Formatea texto basado en cantidad de palabras y umbral mínimo.
- `Sequential Text Reader`: Lee texto línea por línea desde un bloque largo. Soporta loop infinito.
- `Reddit Post Extractor`: Extrae título, autor, texto y comentarios principales de un post de Reddit. Incluye sistema de caché inteligente.
- `TUZZI Save Video (UI Output)`: Nodo de salida que permite mostrar en la interfaz de ComfyUI un video generado. Guarda automáticamente una copia en la carpeta `output/`.

### ⚙️ Infraestructura

- Añadido `requirements.txt` para instalación automática con `ComfyUI-Manager`.
- README actualizado y bilingüe (🇪🇸 / 🇬🇧).

---

## [v1.0.0] - 2025-04-03

### 🆕 New Nodes

- `Bypasser Switch`: Conditional path switch between two inputs of any type.
- `Count Lines in String`: Counts how many lines a text has (ignores empty ones).
- `Add Line Breaks to Text`: Adds line breaks after each period. Cleans empty lines.
- `Smart Line Breaks (by Word Count)`: Formats text based on word count and tail threshold.
- `Sequential Text Reader`: Reads one line at a time from a long block of text. Supports infinite loop cycling.
- `Reddit Post Extractor`: Extracts title, author, post body, and top-level comments from a Reddit post. Includes smart caching system.
- `TUZZI Save Video (UI Output)`: Output node that lets you preview the video in ComfyUI. Automatically saves a copy in the `output/` folder.

### ⚙️ Infrastructure

- Added `requirements.txt` for automatic install via `ComfyUI-Manager`.
- README updated and bilingual (🇪🇸 / 🇬🇧).

---

## [Unreleased]

- Nuevos nodos para procesamiento de datos, IA generativa y automatización web.
- Integración con herramientas de video.
