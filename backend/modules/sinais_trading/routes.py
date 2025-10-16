from fastapi import APIRouter, HTTPException
from datetime import datetime
from typing import List, Dict, Optional
import json

router = APIRouter()

# Armazenamento em memória (temporário)
# Depois podemos migrar para banco de dados
sinais_cache = {
    "data": datetime.now().strftime("%d/%m/%Y"),
    "total": 0,
    "compras": 0,
    "vendas": 0,
    "signals": []
}

@router.post("/upload")
async def upload_sinais(data: Dict):
    """
    Recebe sinais do GitHub Actions
    Formato esperado: {"trading_signals": [...], "assimetria_signals": [...]}
    """
    global sinais_cache

    try:
        # Extrair sinais de trading (compatibilidade com formato antigo)
        if "trading_signals" in data:
            signals = data["trading_signals"]
        else:
            # Formato antigo - lista direta
            signals = data if isinstance(data, list) else []

        # Contar compras e vendas
        compras = len([s for s in signals if s.get('signal') in ['Compra', 'COMPRA']])
        vendas = len([s for s in signals if s.get('signal') in ['Venda', 'VENDA']])

        # Atualizar cache de trading
        sinais_cache = {
            "data": datetime.now().strftime("%d/%m/%Y"),
            "total": len(signals),
            "compras": compras,
            "vendas": vendas,
            "signals": signals,
            "updated_at": datetime.now().isoformat()
        }

        # Processar sinais de assimetria se existirem
        assimetria_result = None
        if "assimetria_signals" in data:
            try:
                from ..assimetria.routes import update_cache
                from ..assimetria.models import AssimetriaSignal

                # Converter para objetos AssimetriaSignal
                assimetria_signals = []
                for signal_data in data["assimetria_signals"]:
                    assimetria_signals.append(AssimetriaSignal(**signal_data))

                # Atualizar cache de assimetria
                update_cache(assimetria_signals)
                assimetria_result = {
                    "total": len(assimetria_signals),
                    "status": "success"
                }
            except Exception as e:
                assimetria_result = {
                    "total": 0,
                    "status": f"error: {str(e)}"
                }

        response = {
            "status": "success",
            "message": "Sinais recebidos com sucesso!",
            "trading": {
                "total": len(signals),
                "compras": compras,
                "vendas": vendas
            },
            "timestamp": datetime.now().isoformat()
        }

        if assimetria_result:
            response["assimetria"] = assimetria_result

        return response

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