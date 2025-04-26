# 📊 SNIES Web Scraper con Flask y Selenium

Este proyecto es una API desarrollada con **Flask** y **Selenium** que extrae automáticamente los enlaces de descarga de las bases consolidadas del **Sistema Nacional de Información de la Educación Superior (SNIES)** de Colombia.

> Ideal para automatizar la recolección de datos históricos del sector educativo colombiano directamente desde su fuente oficial.

---

## 🚀 Características

- 🔎 Web scraping dinámico con Selenium.
- 📄 Recolección de año, título y enlace de cada archivo.
- ↪️ Navegación automática entre páginas usando el botón “Siguiente”.
- 📦 API REST que devuelve los datos en formato JSON.
- 🌐 Preparado para despliegue en servicios como Render, Railway o Heroku.

---

## 🧱 Tecnologías usadas

- **Python 3**
- **Flask**
- **Selenium WebDriver**
- **WebDriver Manager**
- **Gunicorn (para producción)**

---

## 📁 Estructura del proyecto
/mi-scraper/ 
│ ├── app.py # Aplicación Flask principal 
  ├── requirements.txt # Dependencias del proyecto 
  ├── Procfile # Instrucción para ejecución en producción 
  ├── .gitignore # Archivos que no se suben al repositorio 
  └── README.md # Este documento

## ⚙️ Instalación y uso local

### 1. Clonar el repositorio

```bash
git clone https://github.com/tu_usuario/mi-scraper.git
cd mi-scraper

### 2. Crear entorno virtual (opcional pero recomendado)
python -m venv venv
source venv/bin/activate  # en Linux/Mac
venv\Scripts\activate     # en Windows

### 3. Instalar dependencias
pip install -r requirements.txt

### 4. Ejecutar localmente
python app.py
http://127.0.0.1:5000/scraper

## 📌 Notas adicionales
- El scraper depende de que la estructura del sitio SNIES no cambie. Si el HTML se actualiza, pueden ser necesarios ajustes en los selectores.
- El uso de --headless en Selenium está desactivado por defecto para facilitar pruebas visuales. Puedes volver a activarlo si despliegas la app.

Hecho con ❤️ y Python por Juan Lopez[OKAMI]
