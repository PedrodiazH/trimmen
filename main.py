import io
import fitz  # PyMuPDF
from fastapi import FastAPI, File, UploadFile, Form
from fastapi.responses import StreamingResponse, FileResponse, JSONResponse
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

# --- CONFIGURACIÓN CORS ---
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
async def read_root():
    """
    Sirve el archivo index.html directamente.
    Asegúrate de que 'index.html' esté en la misma carpeta que este main.py
    """
    return FileResponse("index.html")

# --- RUTA DE RECORTE ---
@app.post("/crop")
async def crop_pdf(
    file: UploadFile = File(...),
    x: float = Form(...),
    y: float = Form(...),
    w: float = Form(...),
    h: float = Form(...),
    page_num: int = Form(...)
):
    try:
        # 1. Leer el archivo
        content = await file.read()
        doc = fitz.open(stream=content, filetype="pdf")

        # 2. Validar página
        if page_num < 1 or page_num > len(doc):
            return JSONResponse(status_code=400, content={"detail": "Página inválida"})

        # 3. Seleccionar solo la página deseada
        doc.select([page_num - 1]) 
        page = doc[0]

        # 4. Calcular coordenadas
        rect = page.rect
        real_x = x * rect.width
        real_y = y * rect.height
        real_w = w * rect.width
        real_h = h * rect.height

        # 5. Recortar (FIX: Intersección segura)
        requested_rect = fitz.Rect(real_x, real_y, real_x + real_w, real_y + real_h)
        
        # EL TRUCO: Cruzamos la selección con el tamaño real de la página.
        # El operador '&' corta automáticamente lo que sobre.
        final_rect = requested_rect & page.rect 

        # Verificación extra por seguridad
        if final_rect.is_empty:
             return JSONResponse(status_code=400, content={"detail": "Selección fuera de los límites"})

        page.set_cropbox(final_rect)

        # 6. Guardar en memoria
        output_buffer = io.BytesIO()
        doc.save(output_buffer)
        output_buffer.seek(0)
        
        print(f"✅ Recorte exitoso página {page_num}")

        # 7. Devolver PDF
        return StreamingResponse(
            output_buffer, 
            media_type="application/pdf",
            headers={"Content-Disposition": f"attachment; filename=recorte_pag{page_num}.pdf"}
        )

    except Exception as e:
        print(f"❌ Error: {e}")
        return JSONResponse(status_code=500, content={"detail": str(e)})

if __name__ == "__main__":
    import uvicorn
    # Render usa el puerto 10000 por defecto en sus variables de entorno
    uvicorn.run(app, host="0.0.0.0", port=10000)