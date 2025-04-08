# TUZZI-ByPass - Custom Nodes for ComfyUI

### 🇪🇸 Nodos personalizados para flujos automatizados de IA  
### 🇬🇧 Custom nodes for automated AI pipelines

---

## 🎯 ¿Qué es TUZZI-ByPass?

**TUZZI-ByPass** es una colección de nodos personalizados para [ComfyUI](https://github.com/comfyanonymous/ComfyUI) que permite construir flujos avanzados de automatización. El objetivo final es crear un **loop capaz de extraer contenido de la web y transformarlo en un video narrativo**, utilizando texto y placas visuales generadas por IA.  
Iré agregando nuevos nodos periódicamente, enfocados en procesamiento de texto, lógica condicional, scraping, formateo y generación de prompts inteligentes.  
**Se aceptan sugerencias** de nodos o funcionalidades útiles.

**TUZZI-ByPass** is a custom node pack for [ComfyUI](https://github.com/comfyanonymous/ComfyUI) designed to enable advanced automation workflows. The final goal is to build a **loop that extracts content from the web and transforms it into AI-generated videos**, combining narrative text and visual plates.  
New nodes will be added over time, especially focused on text processing, web scraping, logic control, and smart prompt generation.  
**Suggestions are welcome!**

---

## 🔧 Nodos incluidos / Included Nodes

🔗 Reddit Post Extractor
🇪🇸 ES
Este nodo permite extraer contenido desde cualquier post público de Reddit. Solo necesitás pegar la parte final de la URL del post (todo lo que sigue a reddit.com/).
Obtiene:

🧵 Título

✍️ Autor

📅 Fecha de publicación (opcional)

📄 Cuerpo del post

💬 Comentarios principales (sin subcomentarios), incluyendo nombre y fecha (también opcional)

✅ Parámetros importantes:

Campo	Descripción
- reddit_url_path:	Parte final de la URL del post de Reddit (ej: r/AskReddit/comments/abc123)
- execution_count:	Controla si se hace una nueva consulta o se usa caché local
- include_dates:	Si está activado, se muestran las fechas en el post y en los comentarios
- max_comments:	Límite de elementos solicitados a la API de Reddit (máx: 400). ⚠️ Esto no garantiza que se devuelvan tantos comentarios válidos.

🇬🇧 EN
This node extracts content from any public Reddit post. Just paste the last part of the URL (everything after reddit.com/).
It retrieves:

🧵 Title

✍️ Author

📅 Post date (optional)

📄 Post body

💬 Top-level comments (excluding replies), with username and date (also optional)

✅ Key parameters:

Field	Description
- reddit_url_path:	The trailing part of the Reddit post URL (e.g. r/AskReddit/comments/abc123)
- execution_count:	Controls whether to fetch again or use cached result
- include_dates:	If enabled, displays dates in the post and comments
- max_comments:	Limit of items requested from Reddit’s API (max: 400). ⚠️ This does not guarantee that many usable top-level comments will be returned.

- **Input `execution_count`**

Controla cuándo hacer la petición:

| Valor / Value | Comportamiento / Behavior                          |
|---------------|-----------------------------------------------------|
| `1`           | Hace una petición a Reddit y guarda el resultado // Make a request to Reddit and save the result   |
| `>1`          | Lee desde el archivo de caché (no hace petición) // Read from the cache file (does not make a request) |

---

### 💾 ¿Dónde se guarda el caché? / Where is cache stored?

Los resultados se guardan como archivo `.txt` en:  
The results are saved as `.txt` files inside:

ComfyUI/reddit_cache/

Por ejemplo:  
If your input is:

r/AskReddit/comments/abc123/my_question/

Se crea:  
It will generate:

---

### 🖼️ Example Workflow
![TUZZI-ByPass Screenshot](screenshots/Screenshots%20TUZZI-ByPass%20Reddit.png)

---

### 🎥 YouTube Comment Extractor

**ES**  
Este nodo permite extraer comentarios de un video de YouTube mediante la API oficial de Google. Solo necesitás una API key válida (que se coloca en un archivo llamado `youtube_api_key.txt` en la raíz del proyecto).

- 🧵 Título del video
- ✍️ Canal del autor
- 📅 Fecha de publicación (opcional)
- 📄 Descripción
- 💬 Comentarios del primer nivel (sin subcomentarios)

✅ Parámetros:
- `youtube_url_or_id`: puede ser el enlace completo o solo el ID del video
- `execution_count`: si es > 1, se usa el caché local (no hace nueva llamada)
- `include_dates`: si se activa, se incluyen fechas en los comentarios
- `max_comments`: número máximo de comentarios principales a devolver
- `order`: `relevance` (por defecto) o `time`

---

**EN**  
This node extracts top-level comments from a YouTube video using the official Google API. You only need a valid API key (placed in a file called `youtube_api_key.txt` in the project root).

- 🧵 Video title
- ✍️ Channel name
- 📅 Publish date (optional)
- 📄 Description
- 💬 Top-level comments (no replies)

✅ Parameters:
- `youtube_url_or_id`: can be full URL or just video ID
- `execution_count`: if > 1, cached result will be used
- `include_dates`: enables/disables dates on output
- `max_comments`: max amount of comments to return
- `order`: `relevance` (default) or `time`

---

### 🎞️ YouTube Subtitle Extractor

**ES**  
Este nodo intenta extraer los subtítulos disponibles (automáticos o cargados) de un video de YouTube. Utiliza la librería `youtube-transcript-api` y no requiere autenticación. Devuelve el texto plano directamente.

- 🌐 Funciona con subtítulos en múltiples idiomas
- 📄 Devuelve el texto como `STRING`
- 🗂️ También guarda un `.txt` en `ComfyUI/output/<subcarpeta>/`
- 🧼 El nombre del archivo se genera a partir del título del video, sanitizado

✅ Parámetros:
- `youtube_url_or_id`: enlace o ID del video
- `output_subfolder`: carpeta de salida dentro de `output/`
- `preferred_languages`: idiomas preferidos para los subtítulos (`en,es` por defecto)

---

**EN**  
This node extracts available subtitles (auto or manual) from a YouTube video using `youtube-transcript-api`. It doesn’t require authentication and returns the raw text directly.

- 🌐 Supports multiple languages
- 📄 Returns the full transcript as `STRING`
- 🗂️ Also saves a `.txt` file inside `ComfyUI/output/<subfolder>/`
- 🧼 File is named using the video title, sanitized

✅ Parameters:
- `youtube_url_or_id`: video link or ID
- `output_subfolder`: target folder inside `output/`
- `preferred_languages`: preferred subtitle languages (`en,es` by default)

---

### 🖼️ Example Workflow
![TUZZI-ByPass Screenshot](screenshots/Screenshots%20TUZZI-ByPassYoutube.png)

---

### 💾 TUZZI Save Video

- **ES**: Este nodo de salida se encarga de recibir un video_path generado por otro nodo (por ejemplo, Image + Audio to Video) y:

  - Verifica que el archivo existe
  - Lo copia automáticamente a la carpeta output/
  - Lo guarda como tuzzi_last_output.mp4, sobrescribiendo si ya existía
  - Muestra una miniatura en la interfaz de ComfyUI para rápida previsualización
  - Este nodo es útil para activar el procesamiento de un nodo final, ya que ComfyUI requiere al menos un output conectado para ejecutar.

- **EN**: This output node receives a video_path generated by another node (e.g. Image + Audio to Video) and:

  - Verifies that the file exists
  - Automatically copies it to the output/ folder
  - Saves it as tuzzi_last_output.mp4, overwriting if it already existed
  - Displays a thumbnail in the ComfyUI interface for quick preview
  - This node is especially helpful to trigger the execution of a terminal node, since ComfyUI requires at least one connected output to run.

---

### 🔀 `Bypasser Switch`
- **ES**: Permite enrutar entre dos entradas de cualquier tipo (imagen, texto, número, etc.) según un valor `INT`. Ideal para lógica condicional.
- **EN**: Routes between two inputs of any type (image, text, number, etc.) based on an `INT` value. Perfect for conditional logic.

---

### 📏 `Count Lines in String`
- **ES**: Cuenta cuántas líneas contiene un texto. Ignora las líneas vacías.
- **EN**: Counts how many lines are in a string. Ignores empty lines.

---

### 🧹 `Add Line Breaks to Text`
- **ES**: Inserta un salto de línea después de cada punto (`.`) en un texto largo. También elimina líneas vacías para un resultado limpio.
- **EN**: Inserts a line break after each period (`.`) in a long text. Also removes empty lines for clean output.

---

### 🧠 `Smart Line Breaks (by Word Count)`
- **ES**: Inserta saltos de línea inteligentes basados en la cantidad de palabras:
  - Salta cada X palabras (sin cortar).
  - Si el último fragmento es menor que Y palabras, lo une al anterior.
  - Ideal para dividir texto largo en líneas legibles.
- **EN**: Adds smart line breaks based on word count:
  - Breaks every X words (never splitting them).
  - If the last fragment has fewer than Y words, it's merged with the previous one.
  - Great for breaking long texts into readable lines.
 
---

### 🔄 `Sequential Text Reader`
- **ES**: Lee línea por línea desde un bloque de texto largo (`textarea`). Comienza desde el número de línea indicado (`line_number`). Si esa línea está vacía, busca la siguiente que contenga texto. Si llega al final del texto, vuelve al inicio, permitiendo ciclos infinitos. Ideal para automatizaciones que procesan textos paso a paso.
- **EN**: Reads line by line from a long `textarea`. Starts from the provided `line_number`. If that line is empty, it searches the next available line with text. If it reaches the end, it loops back to the top — perfect for infinite loops or step-by-step text automation.

✅ Outputs:
- `selected_text`: the line found with content.
- `updated_line_number`: the actual line where text was found (can be fed into loop logic).

---

### 🔢 Number Each Line

**ES**  
Este nodo agrega automáticamente un número al inicio de cada línea de un bloque de texto, en el formato `1. texto`.  
Es ideal para depuración y control visual cuando estás trabajando con loops que procesan grandes cantidades de texto (como 500+ líneas) y necesitás saber en qué parte del flujo estás.

**EN**  
This node automatically adds a number at the beginning of each line in a text block, using the format `1. text`.  
It’s especially useful for debugging or visual tracking when processing large texts in loops (e.g., 500+ lines) and you want to see which line you're currently working with.

---

#### ✅ Output Example

**Input:**

Line one Line two Line three

**Output:**

1. Line one
2. Line two
3. Line three

### 🖼️ Example Workflow
![TUZZI-ByPass Screenshot](screenshots/Screenshots%20TUZZI-ByPass.png)

- **ES**: Al ser Python básico, no requiere de instalar librerías adicionales. La meta es crear una automatización perfecta, que cree videos de manera automatizada solo insertando un texto extenso, como un libro o guion. Iré haciendo actualizaciones, pero si necesitas algo particular, solo pídelo.
- **EN**: Since Python is basic, it doesn't require installing additional libraries. The goal is to create seamless automation that automatically creates videos simply by inserting a long text, such as a book or script. I'll be making updates, but if you need something specific, just ask.
---

## ⚙️ Instalación / Installation

1. Cloná o descargá este repositorio dentro de tu carpeta de `custom_nodes` de ComfyUI:

```bash
git clone https://github.com/AlejandroTuzzi/comfyui-tuzzi-bypass.git
```

---

## 📚 Requisitos / Requirements

Este paquete de nodos requiere las siguientes librerías externas:


Si estás ejecutando ComfyUI en local, podés instalarlas fácilmente desde terminal con:

```bash
pip install -r requirements.txt
```



