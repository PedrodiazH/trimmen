import io
import fitz  # PyMuPDF
from fastapi import FastAPI, File, UploadFile, Form
from fastapi.responses import StreamingResponse, HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

from fastapi.requests import Request
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()
# PARA QUE GITHUB PAGES PUEDA HABLAR CON PYTHON ---
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Configuración de templates (asumiendo que el html está en la misma carpeta)
templates = Jinja2Templates(directory=".")

@app.get("/", response_class=HTMLResponse)
async def read_root(request: Request):
    """Sirve el archivo HTML principal."""
    return templates.TemplateResponse("trimmen.html", {"request": request})

@app.post("/crop")
async def crop_pdf(
    file: UploadFile = File(...),
    x: float = Form(...), # Coordenada X normalizada (0 a 1)
    y: float = Form(...), # Coordenada Y normalizada (0 a 1)
    w: float = Form(...), # Ancho normalizado
    h: float = Form(...), # Alto normalizado
    page_num: int = Form(1) # Número de página (1-based)
):
    try:
        # 1. Leer el archivo en memoria
        content = await file.read()
        doc = fitz.open(stream=content, filetype="pdf")

        # 2. Validar página
        if page_num < 1 or page_num > len(doc):
            return JSONResponse(status_code=400, content={"detail": "Página inválida"})
        # borra todas las páginas EXCEPTO la que eligió el usuario.
        doc.select([page_num - 1]) 
        page = doc[0]

        # 3. Calcular coordenadas reales basadas en el tamaño del PDF
        # Las entradas vienen normalizadas (0.5 significa la mitad de la página)
        rect = page.rect # Tamaño original del PDF (ej: A4)
        
        real_x = x * rect.width
        real_y = y * rect.height
        real_w = w * rect.width
        real_h = h * rect.height

        # Crear el rectángulo de recorte (fitz.Rect(x0, y0, x1, y1))
        crop_rect = fitz.Rect(real_x, real_y, real_x + real_w, real_y + real_h)
        
        # 4. Ejecutar el recorte
        page.set_cropbox(crop_rect)

        # 5. Guardar en buffer de memoria
        output_buffer = io.BytesIO()
        doc.save(output_buffer)
        output_buffer.seek(0)
        print("✅ Recorte exitoso, enviando archivo...") # CONFIRMACIÓN EN CONSOLA
        
        # 6. Devolver el archivo
        return StreamingResponse(
            output_buffer, 
            media_type="application/pdf",
            headers={"Content-Disposition": "attachment; filename=recorte_perfecto.pdf"}
        )

    except Exception as e:
        import traceback
        error_msg = traceback.format_exc()
        print(f"❌ ERROR FATAL EN PYTHON:\n{error_msg}") # ESTO LO VERÁS EN LA TERMINAL
        return JSONResponse(status_code=500, content={"detail": str(e)}) # CAMBIO IMPORTANTE

if __name__ == "__main__":
    import uvicorn
    # Ejecutar servidor: host 0.0.0.0 para que sea visible en red local/deploy
    uvicorn.run(app, host="0.0.0.0", port=8000)