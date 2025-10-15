from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
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

# Servir arquivos estáticos (frontend)
frontend_path = os.path.join(os.path.dirname(__file__), "..", "frontend", "public")

# Verificar se o diretório existe
if os.path.exists(frontend_path):
    # Montar arquivos estáticos com suporte a HTML
    app.mount("/", StaticFiles(directory=frontend_path, html=True), name="static")
    print(f"✅ Servindo arquivos de: {frontend_path}")
else:
    print(f"❌ Diretório frontend não encontrado: {frontend_path}")

    # Fallback: retornar JSON se não houver frontend
    @app.get("/")
    async def pagina_inicial():
        return {
            "mensagem": "Bem-vindo ao Resenha Trader API!",
            "versao": "1.0.0",
            "status": "online",
            "docs": "/docs"
        }

@app.get("/api/health")
async def verificar_saude():
    return {"status": "ok"}  # Bem simples!