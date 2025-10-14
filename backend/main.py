from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from datetime import datetime
import os

# IMPORTANTE: Importar o router
from modules.sinais_trading.routes import router as sinais_router

app = FastAPI(
    title="Resenha Trader API",
    description="Sua plataforma de análise de mercado",
    version="1.0.0"
)

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# IMPORTANTE: Registrar o módulo de sinais
app.include_router(
    sinais_router, 
    prefix="/api/sinais", 
    tags=["Sinais"]
)

# Servir frontend
frontend_path = os.path.join(os.path.dirname(__file__), "..", "frontend", "public")

try:
    app.mount("/static", StaticFiles(directory=frontend_path), name="static")
except:
    print("⚠️ Pasta frontend não encontrada - API funcionando sem frontend")

@app.get("/")
async def pagina_inicial():
    try:
        return FileResponse(os.path.join(frontend_path, "index.html"))
    except:
        return {
            "mensagem": "Bem-vindo ao Resenha Trader API!",
            "versao": "1.0.0",
            "status": "online",
            "docs": "/docs"
        }

@app.get("/api/health")
async def verificar_saude():
    return {
        "status": "funcionando",
        "modulos": ["sinais", "distancia", "ciclo", "blog"]
    }