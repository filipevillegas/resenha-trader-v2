from fastapi import APIRouter
from datetime import datetime

# Criar roteador
router = APIRouter()

@router.get("/")
async def pegar_sinais():
    """Retorna sinais de trading"""
    
    sinais_exemplo = [
        {
            "ticker": "PETR4",
            "setup": "Larry Williams 9.1",
            "signal": "Compra",
            "score": 85,
            "ultimo": 38.45,
            "quality": "PREMIUM"
        },
        {
            "ticker": "VALE3",
            "setup": "Rompimento de Resistência",
            "signal": "Compra",
            "score": 72,
            "ultimo": 62.30,
            "quality": "BOM"
        }
    ]
    
    return {
        "data": datetime.now().strftime("%d/%m/%Y"),
        "total": len(sinais_exemplo),
        "sinais": sinais_exemplo
    }

@router.get("/resumo")
async def pegar_resumo():
    """Resumo dos sinais"""
    return {
        "total_hoje": 25,
        "compras": 14,
        "vendas": 11,
        "premium": 5
    }

@router.get("/teste")
async def teste():
    """Rota de teste simples"""
    return {"mensagem": "Módulo de sinais funcionando!"}