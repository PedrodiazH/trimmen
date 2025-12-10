# **TRIMMEN**


### 🌐 Descripción del Proyecto

**Trimmen** es una herramienta online, gratuita y muy fácil de usar que permite recortar la zona seleccionada de un PDF. Su propósito es ofrecer simplicidad, velocidad y privacidad. 


---

### 🛠️ Tecnologías Utilizadas

* **Frontend:** HTML, JS nativo, PDF.js
* **Estilos:** TailwindCSS
* **Backend (opcional):** Python + FastAPI
* **Procesamiento PDF:** PyMuPDF (Fitz)
* **Despliege Web:** Github, Render 

---

### 📦 Instalación y Configuración
El proyecto esta desplegado y funcional en la siguiente web: 

Sin embargo, Si deseas ejecutarlo de manera local (offline), sigue estos pasos:

```bash
# 1. Clonar el repositorio
git clone https://github.com/usuario/repositorio.git
cd repositorio

# 2. Instalar dependencias (Python)
pip install -r requirements.txt

# 3. Iniciar el servidor Backend
python main.py
```
> [!NOTE]
> Una vez iniciado, abre tu navegador en `http://localhost:8000`.


> [!IMPORTANT]
>Si lo usas localmente, recuerda ir a tu `index.html` y cambiar la URL del `fetch`. Debe apuntar a `/crop` y **no** a la dirección de Render.

---

### 🧩 Uso Básico

1. Subir un archivo PDF.
2. Seleccionar el área a recortar.
3. Previsualizar el resultado.
4. Descargar el PDF recortado.

---

### 🐞 Reporte de Errores

Si encuentras un problema:

* Abre un issue en el repositorio.
* Describe el comportamiento esperado y el observado.
* Incluye pasos para reproducir el error.

---

### 📜 Licencia

Este proyecto está bajo la licencia MIT. Consulta el archivo `LICENSE` para más información.


