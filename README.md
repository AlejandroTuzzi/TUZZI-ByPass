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

### 🔗 Reddit Post Extractor

**ES**  
Este nodo permite extraer contenido desde cualquier post público de Reddit. Solo necesitás pegar la parte final de la URL del post (todo lo que sigue a `reddit.com/`). El nodo obtiene el título, el contenido original, el autor, la fecha y los comentarios principales (sin subcomentarios).  

Para evitar hacer múltiples llamadas a Reddit en cada ciclo de un loop, el nodo incluye un sistema de **caché inteligente**:  
- Si el campo `execution_count` vale `1`, el nodo realiza una petición real a Reddit.
- Si el campo es mayor a `1`, simplemente reutiliza el contenido previamente guardado (caché).

---

**EN**  
This node extracts content from any public Reddit post. You only need to paste the final part of the URL (everything after `reddit.com/`). It retrieves the post title, body, author, date, and all top-level comments (excluding replies).  

To avoid redundant Reddit requests in looped workflows, the node includes a **smart caching system**:  
- If `execution_count` equals `1`, it performs a real request.
- If it's greater than `1`, it just returns the previously saved cache.

---

### 🔧 Cómo usarlo / How to use it

- **Input `reddit_url_path`**  
  Solo pegá la parte final del enlace del post:  
  Just paste the end of the post link:  

- r/AskReddit/comments/abc123/what_would_you_do/


- **Input `execution_count`**

Controla cuándo hacer la petición:

| Valor / Value | Comportamiento / Behavior                          |
|---------------|-----------------------------------------------------|
| `1`           | Hace una petición a Reddit y guarda el resultado   |
| `>1`          | Lee desde el archivo de caché (no hace petición)   |

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

### ✅ Output

El nodo devuelve una salida de texto estructurada que incluye:  
The node outputs a clean text block with:

- 🧵 Título / Title  
- ✍️ Autor / Author  
- 📅 Fecha / Date  
- 📄 Texto del post / Post body  
- 💬 Comentarios con usuario y fecha / Top-level comments with user and date  

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


### 🖼️ Example Workflow
![TUZZI-ByPass Screenshot](screenshots/Screenshots%20TUZZI-ByPass.png)

- **ES**: Al ser Python básico, no requiere de instalar librerías adicionales. La meta es crear una automatización perfecta, que cree videos de manera automatizada solo insertando un texto extenso, como un libro o guion. Iré haciendo actualizaciones, pero si necesitas algo particular, solo pídelo.
- **EN**: Since Python is basic, it doesn't require installing additional libraries. The goal is to create seamless automation that automatically creates videos simply by inserting a long text, such as a book or script. I'll be making updates, but if you need something specific, just ask.
---

## ⚙️ Instalación / Installation

1. Cloná o descargá este repositorio dentro de tu carpeta de `custom_nodes` de ComfyUI:

```bash
git clone https://github.com/tuusuario/comfyui-tuzzi-bypass.git
