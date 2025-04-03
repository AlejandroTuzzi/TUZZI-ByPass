# TUZZI-ByPass - Custom Nodes for ComfyUI

### 🇪🇸 Nodos personalizados para flujos avanzados en ComfyUI  
### 🇬🇧 Custom nodes for advanced workflows in ComfyUI

---

## 🧩 Descripción / Description

**TUZZI-ByPass** es una colección de nodos utilitarios y de preprocesamiento de texto pensada para flujos automatizados con lógica condicional, manipulación de cadenas y formateo inteligente para uso con herramientas como IA generativa, generación de prompts y bucles controlados.

**TUZZI-ByPass** is a collection of utility and text preprocessing nodes designed for automated workflows, conditional logic, string manipulation, and smart formatting. Ideal for use with generative AI pipelines, prompt generation, and controlled loops.

---

## 🔧 Nodos incluidos / Included Nodes

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

### 🖼️ Example Workflow
![TUZZI-ByPass Screenshot](screenshots/Screenshots%20TUZZI-ByPass.png)

- **ES**: Al ser Python básico, no requiere de instalar librerías adicionales. La meta es crear una automatización perfecta, que cree videos de manera automatizada solo insertando un texto extenso, como un libro o guion. Iré haciendo actualizaciones, pero si necesitas algo particular, solo pídelo.
- **EN**: Since Python is basic, it doesn't require installing additional libraries. The goal is to create seamless automation that automatically creates videos simply by inserting a long text, such as a book or script. I'll be making updates, but if you need something specific, just ask.
---

## ⚙️ Instalación / Installation

1. Cloná o descargá este repositorio dentro de tu carpeta de `custom_nodes` de ComfyUI:

```bash
git clone https://github.com/AlejandroTuzzi/TUZZI-ByPass.git
