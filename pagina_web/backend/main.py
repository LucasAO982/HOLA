import os
from fastapi import FastAPI, Request
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse

app = FastAPI()

# Variable global para almacenar los datos que envíe el ESP32
latest_weather = {"temperatura": 0, "humedad": 0, "presion": 0}

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
FRONTEND_DIR = os.path.join(BASE_DIR, "frontend")

# Servir archivos estáticos del frontend
app.mount("/static", StaticFiles(directory=os.path.join(FRONTEND_DIR, "static")), name="static")

@app.get("/")
async def read_index():
    return FileResponse(os.path.join(FRONTEND_DIR, "index.html"))

@app.get("/api/weather")
async def get_weather():
    # Devuelve los últimos datos recibidos del ESP32
    return latest_weather

@app.post("/api/update")
async def update_weather(request: Request):
    global latest_weather
    data = await request.json()
    # Actualizamos la variable con los datos enviados por el ESP32
    latest_weather = data
    return {"status": "success", "received": data}
