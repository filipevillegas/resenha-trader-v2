from fastapi import APIRouter, HTTPException
from datetime import datetime
from typing import List, Dict, Optional
import json

# Import do cache de assimetria (dicionário, não função!)
from modules.assimetria import assimetria_cache

router = APIRouter()

# Armazenamento em memória (temporário)
# Depois podemos migrar para banco de dados
sinais_cache = {
    "data": datetime.now().strftime("%d/%m/%Y"),
    "total": 0,
    "compras": 0,
    "vendas": 0,
    "premium": 0,
    "signals": []
}

@router.post("/upload")
async def upload_sinais(payload: dict):
    """
    Recebe sinais de trading E assimetria do GitHub Actions.

    Payload esperado:
    {
        "trading_signals": [...],      # Sinais de trading (existente)
        "assimetria_signals": [...],   # Sinais de assimetria (NOVO)
        "data_atualizacao": "2025-10-15T10:30:00"
    }
    """
    global sinais_cache

    try:
        # Processar sinais de trading (EXISTENTE)
        sinais = payload.get("trading_signals", [])

        if sinais:
            # Contar por tipo
            compras = len([s for s in sinais if s.get("tipo") == "COMPRA" or s.get("signal") in ["Compra", "COMPRA"]])
            vendas = len([s for s in sinais if s.get("tipo") == "VENDA" or s.get("signal") in ["Venda", "VENDA"]])
            premium = len([s for s in sinais if s.get("premium", False) or s.get("quality") == "PREMIUM"])

            # Atualizar cache de sinais de trading
            sinais_cache["data"] = datetime.now().strftime("%d/%m/%Y")
            sinais_cache["total"] = len(sinais)
            sinais_cache["compras"] = compras
            sinais_cache["vendas"] = vendas
            sinais_cache["premium"] = premium
            sinais_cache["signals"] = sinais
            sinais_cache["updated_at"] = payload.get("data_atualizacao", datetime.now().isoformat())

        # Processar sinais de assimetria (NOVO)
        sinais_assimetria = payload.get("assimetria_signals", [])

        if sinais_assimetria:
            # Contar sobrecomprados e sobrevendidos
            sobrecomprados = len([s for s in sinais_assimetria if s.get("status") == "Sobrecomprado"])
            sobrevendidos = len([s for s in sinais_assimetria if s.get("status") == "Sobrevendido"])

            # Atualizar cache de assimetria diretamente
            assimetria_cache["data"] = datetime.now().strftime("%d/%m/%Y")
            assimetria_cache["total"] = len(sinais_assimetria)
            assimetria_cache["sobrecomprados"] = sobrecomprados
            assimetria_cache["sobrevendidos"] = sobrevendidos
            assimetria_cache["signals"] = sinais_assimetria
            assimetria_cache["updated_at"] = payload.get("data_atualizacao", datetime.now().isoformat())

            assimetria_result = {
                "total": len(sinais_assimetria),
                "sobrecomprados": sobrecomprados,
                "sobrevendidos": sobrevendidos
            }
        else:
            assimetria_result = {"total": 0, "sobrecomprados": 0, "sobrevendidos": 0}

        # Retornar confirmação de ambos
        return {
            "success": True,
            "message": "Dados recebidos com sucesso",
            "trading": {
                "total": len(sinais),
                "compras": compras if sinais else 0,
                "vendas": vendas if sinais else 0,
                "premium": premium if sinais else 0
            },
            "assimetria": assimetria_result,
            "timestamp": datetime.now().isoformat()
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erro ao processar sinais: {str(e)}")

@router.get("/")
async def pegar_sinais():
    """Retorna sinais armazenados"""
    
    if sinais_cache["total"] == 0:
        # Se não tem dados ainda, retornar exemplo
        return {
            "data": datetime.now().strftime("%d/%m/%Y"),
            "total": 2,
            "compras": 1,
            "vendas": 1,
            "signals": [
                {
                    "ticker": "PETR4",
                    "setup": "Larry Williams 9.1",
                    "signal": "Compra",
                    "score": 85,
                    "ultimo": 38.45,
                    "quality": "PREMIUM",
                    "tags": ["ALTA", "VOL+", "RSI52"]
                },
                {
                    "ticker": "VALE3",
                    "setup": "Rompimento de Resistência",
                    "signal": "Compra",
                    "score": 72,
                    "ultimo": 62.30,
                    "quality": "BOM",
                    "tags": ["ALTA", "VOL+", "RSI68"]
                }
            ],
            "message": "Dados de exemplo - Aguardando primeiro upload do GitHub Actions"
        }
    
    return sinais_cache

@router.get("/resumo")
async def pegar_resumo():
    """Resumo dos sinais"""
    
    if sinais_cache["total"] == 0:
        return {
            "total_hoje": 2,
            "compras": 1,
            "vendas": 1,
            "premium": 1,
            "message": "Dados de exemplo"
        }
    
    # Contar por qualidade
    premium = len([s for s in sinais_cache["signals"] if s.get('quality') == 'PREMIUM'])
    
    return {
        "total_hoje": sinais_cache["total"],
        "compras": sinais_cache["compras"],
        "vendas": sinais_cache["vendas"],
        "premium": premium,
        "ultima_atualizacao": sinais_cache.get("updated_at", "")
    }

@router.get("/teste")
async def teste():
    """Rota de teste"""
    return {
        "mensagem": "Módulo de sinais funcionando!",
        "cache_size": sinais_cache["total"],
        "ultima_atualizacao": sinais_cache.get("updated_at", "Nenhum dado ainda")
    }