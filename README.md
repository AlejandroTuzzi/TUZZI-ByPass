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

### 🎥 YouTubeCommentExtractor

**ES**  
Este nodo obtiene los comentarios de un video de YouTube usando la API oficial. Las últimas mejoras incluyen:

- Opción para incluir o excluir la descripción del video
- Eliminación opcional de emojis del contenido
- Inclusión de respuestas si se desea
- Generación de caché única por combinación de opciones

✅ Parámetros:
- `include_description`: incluye el cuerpo del video
- `remove_emojis`: limpia los comentarios y títulos
- `include_replies`: permite recuperar respuestas (no solo comentarios principales)

**EN**  
This node fetches YouTube comments using the official API. Recent improvements include:

- Option to include/exclude video description
- Optional emoji removal from content
- Option to include replies
- Smart cache depending on options used

✅ Parameters:
- `include_description`: include video body
- `remove_emojis`: strip emojis from comments
- `include_replies`: include comment replies

---

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

---

### ✂️ TextTruncatorPlus

**ES**  
Este nodo corta un texto largo después de cierta cantidad de caracteres y añade un sufijo personalizado. Ideal para títulos, introducciones o resúmenes controlados.

✅ Parámetros:
- `text`: texto original a truncar
- `cut_after_char`: número máximo de caracteres antes del corte
- `suffix`: texto que se añadirá al final (ej. `(...)`)

**EN**  
This node truncates a long string after a specific number of characters and appends a custom suffix. Ideal for headlines or preview snippets.

✅ Parameters:
- `text`: original string
- `cut_after_char`: max characters before cut
- `suffix`: string to append (e.g. `(...)`)

---

### 🪜 SequentialTextReaderAuto

**ES**  
Lee una línea distinta en cada ejecución de un mismo bloque de texto. Si el texto cambia, el contador se reinicia automáticamente. Usa caché persistente y hash para detectar modificaciones.

✅ Características:
- Incrementa línea automáticamente
- Reinicia si el texto cambia
- Guarda y carga estado desde `tuzzi_cache/`

**EN**  
Reads one line at a time from a multi-line text block. Automatically advances on each execution. If the text changes, the counter resets.

✅ Features:
- Auto-incrementing line reader
- Resets on content change
- Uses persistent cache to track position

---

### 🔗 LinkSuppressor

**ES**  
Reemplaza enlaces en texto por un mensaje personalizado. Detecta:

- URLs directas (`https://...`)
- Enlaces Markdown (`[texto](url)`)
- Enlaces HTML (`<a href="...">texto</a>`)
- Adjuntos de imagen con parámetros largos

✅ Parámetros:
- `replacement_text`: texto con el que reemplazar los enlaces (por defecto: `(Link Deleted)`)

**EN**  
Replaces links in text with a custom message. Detects:

- Direct URLs (`https://...`)
- Markdown links (`[text](url)`)
- HTML anchors (`<a href="...">text</a>`)
- Media links with long query strings

✅ Parameters:
- `replacement_text`: text used to replace the links (default: `(Link Deleted)`)

---

### 🖼️ Example Workflow
![TUZZI-ByPass Screenshot](screenshots/Screenshots%20TUZZI-ByPass.png)

- **ES**: Al ser Python básico, no requiere de instalar librerías adicionales. La meta es crear una automatización perfecta, que cree videos de manera automatizada solo insertando un texto extenso, como un libro o guion. Iré haciendo actualizaciones, pero si necesitas algo particular, solo pídelo.
- **EN**: Since Python is basic, it doesn't require installing additional libraries. The goal is to create seamless automation that automatically creates videos simply by inserting a long text, such as a book or script. I'll be making updates, but if you need something specific, just ask.
---

### 🌐 GeminiFlash25 (Gemini 2.5 Flash API)

**ES**  
Este nodo se conecta a la API de Google Gemini 2.5 Flash. Permite enviar un texto (`user_input`) y un prompt que lo instruye (`prompt_instruction`), y recibir la respuesta generada. Ideal para transformar, resumir o analizar grandes cantidades de texto dentro de un workflow.

✅ Características clave:
- Usa API oficial de Gemini
- Usa caché inteligente (almacena la respuesta para cada combinación única de prompt + input)
- Si `should_generate ≠ 1`, se devuelve la respuesta almacenada anterior (si existe), o el texto original
- Guarda los resultados en `gemini_cache/`

**EN**  
This node connects to the official Gemini 2.5 Flash API. You can provide a prompt (`prompt_instruction`) and input text (`user_input`), and it will return a generated response. Great for transformation, summarization or interpretation inside loops.

✅ Key features:
- Uses Gemini official API
- Smart cache (stores one result per unique prompt+input combination)
- If `should_generate ≠ 1`, it returns the previous result (if exists) or the raw input
- Cached results are stored in `gemini_cache/`

---

**ES**
### Nodo Groq
Este nodo permite interactuar con la API de Groq para generar resultados basados en entradas de texto. Incluye:

- Dos entradas de texto para recibir información del usuario.
- Un desplegable que carga automáticamente los modelos disponibles a través de la API de Groq.
- Salida de tipo string con el resultado generado por la IA.

Cómo incluir la API Key
- Para utilizar este nodo, debes incluir tu API key de Groq en el método run() del nodo. Asegúrate de reemplazar YOUR_API_KEY con tu clave real:

python
CopyInsert
headers = {
    'Authorization': 'Bearer YOUR_API_KEY'
}

Cómo utilizar el nodo
- Configura las entradas de texto con la información que deseas procesar.
- Selecciona el modelo deseado del desplegable.
- Ejecuta el nodo para obtener el resultado generado por la IA.

**EN**
### Groq Node
This node allows interaction with the Groq API to generate results based on text inputs. It includes:

- Two text inputs to receive information from the user.
- A dropdown that automatically loads available models via the Groq API.
- String output with the result generated by the AI.

How to include the API Key
- To use this node, you must include your Groq API key in the run() method of the node. Make sure to replace YOUR_API_KEY with your actual key:

python
CopyInsert
headers = {
    'Authorization': 'Bearer YOUR_API_KEY'
}

How to use the node

- Set the text inputs with the information you want to process.
- Select the desired model from the dropdown.
- Run the node to obtain the result generated by the AI.
- Si necesitas más ayuda o quieres intentar otra cosa, házmelo saber.

---

### 📄 PlosArticleScraper

**ES**  
Este nodo extrae el contenido completo de artículos científicos desde [journals.plos.org](https://journals.plos.org). Devuelve el título, fecha, autores, abstract y cuerpo (sin referencias ni secciones suplementarias).

✅ Funcionalidad avanzada:
- Usa BeautifulSoup para parsear el HTML localmente
- Guarda el artículo HTML como caché en `plos_cache/`
- Si `execute ≠ 1`, reutiliza el HTML existente (sin hacer nueva petición)
- Si no hay caché y `execute ≠ 1`, devuelve un mensaje informando

**EN**  
This node scrapes full scientific articles from [journals.plos.org](https://journals.plos.org). It returns the title, date, authors, abstract and article body (excluding references and attachments).

✅ Smart behavior:
- Uses BeautifulSoup to parse content locally
- Stores HTML in `plos_cache/`
- If `execute ≠ 1`, it reads the existing file (no new requests)
- If no cache exists and `execute ≠ 1`, it returns an error message

---

### 🔢 RangedSelectorText5 & RangedSelectorTitleURL5 / TitleURL10

**ES**  
Estos nodos permiten definir bloques de contenido (texto o título + URL) asociados a rangos de números. Perfecto para automatizar fuentes múltiples en bucles controlados.

- `RangedSelectorText5`: 5 textos con sus respectivos topes numéricos
- `RangedSelectorTitleURL5`: 5 pares (título, URL) con rangos personalizados
- `RangedSelectorTitleURL10`: 10 pares (título, URL) para uso más intensivo

✅ Cómo funciona:
- Cada bloque tiene un `rangeX` que define el valor máximo para activarse.
- El nodo devuelve el contenido del bloque correspondiente a `index`.
- Si el `index` está entre dos bloques o mal configurado, devuelve vacío o mensaje de error.
- También devuelve el `offset`, que es el valor mínimo del bloque actual. Esto permite sincronizar secuencias que deben reiniciarse por texto nuevo.

**EN**  
These nodes allow you to define text or (title + URL) blocks tied to numeric ranges. Ideal for orchestrating multiple sources inside a loop.

- `RangedSelectorText5`: 5 text blocks with individual range caps
- `RangedSelectorTitleURL5`: 5 (title + url) pairs with custom limits
- `RangedSelectorTitleURL10`: same, but supports 10 slots

✅ Behavior:
- Each block has a `rangeX` that defines its upper bound.
- The node returns the content (or title/url pair) for the matching `index`.
- If values are misconfigured (e.g., range3 < range2), returns a warning.
- Also returns the `offset` for the current range, useful to reset counters in sequential systems.

### 🧶 DataloungeScraper

**ES**  
Este nodo extrae todos los comentarios principales desde un hilo público de [DataLounge.com](https://www.datalounge.com). El resultado es un texto procesado, ideal para ser leído línea por línea.

✅ Comportamiento inteligente:
- Si el autor es “Anonymous”, reemplaza por `** NEXT COMMENT **` para marcar el salto entre comentarios.
- Si hay nombre de autor real, muestra: `Comment by: Nombre`
- Guarda en caché la página HTML para evitar múltiples descargas
- Si `execute ≠ 1` y el archivo ya existe, devuelve el contenido desde la caché

**EN**  
This node extracts all top-level comments from a public thread on [DataLounge.com](https://www.datalounge.com). The output is clean text, ideal for sequential reading.

✅ Behavior:
- If author is “Anonymous”, it writes `** NEXT COMMENT **` to separate each block.
- If a named poster is found, it shows `Comment by: Name`
- Saves HTML locally as cache to avoid re-downloading
- If `execute ≠ 1` and file exists, it returns cached content

✅ Parámetros / Parameters:
- `url`: enlace directo al hilo de Datalounge
- `execute`: si es 1, fuerza actualización; si no, usa caché

🗂️ Los archivos cacheados se guardan en `datalounge_cache/`.

---

### 🎬 Smart Audio/Video Composer

**ES**  
Este nodo permite generar un video a partir de dos posibles orígenes visuales:

1. Una imagen estática combinada con audio externo.
2. Un video `.mp4` completo que ya contiene su propio audio.

✅ Parámetro clave:
- `visual_mode`: selector de modo visual:
  - `0` → genera video desde una imagen + audio TTS
  - `1` → reutiliza un video completo y lo exporta tal cual (incluyendo su audio)

✅ Entradas:
- `image`: imagen (solo usada en modo 0)
- `audio`: audio (solo usado en modo 0)
- `video_path`: ruta al `.mp4` (solo usada en modo 1)
- `output_subfolder`: subcarpeta dentro de `output/`
- `fps`: frames por segundo (25 o 30)

**EN**  
This node creates a video from one of two visual sources:

1. A static image combined with external audio.
2. A full `.mp4` video that already contains its own audio.

✅ Key parameter:
- `visual_mode`: visual mode selector:
  - `0` → generate video from image + TTS audio
  - `1` → reuse full video and export as-is (with original audio)

✅ Inputs:
- `image`: image (used only in mode 0)
- `audio`: audio (used only in mode 0)
- `video_path`: `.mp4` file (used only in mode 1)
- `output_subfolder`: folder inside `output/`
- `fps`: frames per second (25 or 30)

📂 El video generado se guarda en la carpeta `output/<subcarpeta>/` con nombre incremental estilo ComfyUI.

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


