from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
import os

# Importar módulos
from modules.sinais_trading.routes import router as sinais_router
from modules.assimetria.routes import router as assimetria_router

# Criar app
app = FastAPI(
    title="Resenha Trader API",
    description="API de sinais de trading para o mercado brasileiro",
    version="2.0.0"
)

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ============================
# 1. ROTAS DA API (PRIMEIRO!)
# ============================

@app.get("/api/health")
async def health_check():
    """Health check endpoint"""
    return {"status": "ok"}

# Incluir routers dos módulos
app.include_router(sinais_router, prefix="/api/sinais", tags=["Sinais Trading"])
app.include_router(assimetria_router, prefix="/api/assimetria", tags=["Assimetria"])

# ============================
# 2. ROTAS DE PÁGINAS HTML
# ============================

@app.get("/dashboard")
async def serve_dashboard():
    """Serve o dashboard profissional"""
    file_path = os.path.join(os.path.dirname(__file__), "..", "frontend", "public", "dashboard.html")
    if os.path.exists(file_path):
        return FileResponse(file_path, media_type="text/html")
    return {"error": "Dashboard não encontrado"}

# ============================
# 3. ARQUIVOS ESTÁTICOS (POR ÚLTIMO!)
# ============================

# Configurar caminho do frontend
frontend_path = os.path.join(os.path.dirname(__file__), "..", "frontend", "public")

# Verificar se existe
if os.path.exists(frontend_path):
    print(f"✅ Servindo arquivos de: {frontend_path}")
    # IMPORTANTE: mount SEMPRE por último!
    app.mount("/", StaticFiles(directory=frontend_path, html=True), name="static")
else:
    print(f"❌ Diretório frontend não encontrado: {frontend_path}")
