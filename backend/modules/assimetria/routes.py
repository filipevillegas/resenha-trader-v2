# -*- coding: utf-8 -*-
"""
Rotas da API para o modulo de Assimetria.
"""

from fastapi import APIRouter, HTTPException, Query
from typing import List, Optional
from datetime import datetime

from . import assimetria_cache
from .models import (
    AssimetriaSignal,
    AssimetriaResumo,
    AssimetriaResponse
)

router = APIRouter()


@router.get("/", response_model=AssimetriaResponse)
async def get_assimetria_signals(
    status: Optional[str] = Query(None, description="Filtrar por status: Sobrecomprado ou Sobrevendido"),
    nivel: Optional[str] = Query(None, description="Filtrar por nivel: Critica, Alta ou Moderada"),
    min_zscore: Optional[float] = Query(None, description="Z-Score minimo (em modulo)")
):
    """
    Retorna todos os sinais de assimetria com filtros opcionais.
    """
    if not assimetria_cache["signals"]:
        return AssimetriaResponse(
            data="",
            total=0,
            sobrecomprados=0,
            sobrevendidos=0,
            signals=[],
            updated_at=""
        )

    signals = assimetria_cache["signals"]

    # Aplicar filtros
    if status:
        signals = [s for s in signals if s["status"] == status]

    if nivel:
        signals = [s for s in signals if s["nivel_oportunidade"] == nivel]

    if min_zscore is not None:
        signals = [s for s in signals if abs(s["z_score"]) >= min_zscore]

    # Contar sobrecomprados e sobrevendidos nos resultados filtrados
    sobrecomprados = len([s for s in signals if s["status"] == "Sobrecomprado"])
    sobrevendidos = len([s for s in signals if s["status"] == "Sobrevendido"])

    return AssimetriaResponse(
        data=assimetria_cache["data"],
        total=len(signals),
        sobrecomprados=sobrecomprados,
        sobrevendidos=sobrevendidos,
        signals=signals,
        updated_at=assimetria_cache["updated_at"]
    )


@router.get("/resumo", response_model=AssimetriaResumo)
async def get_assimetria_resumo():
    """
    Retorna estatisticas gerais dos sinais de assimetria.
    """
    if not assimetria_cache["signals"]:
        return AssimetriaResumo(
            total=0,
            sobrecomprados=0,
            sobrevendidos=0,
            criticas=0,
            altas=0,
            moderadas=0,
            avg_volatilidade=None
        )

    signals = assimetria_cache["signals"]

    # Contar por nivel
    criticas = len([s for s in signals if s["nivel_oportunidade"] == "Critica"])
    altas = len([s for s in signals if s["nivel_oportunidade"] == "Alta"])
    moderadas = len([s for s in signals if s["nivel_oportunidade"] == "Moderada"])

    # Calcular volatilidade media
    volatilidades = [s["volatilidade_anualizada"] for s in signals]
    avg_vol = sum(volatilidades) / len(volatilidades) if volatilidades else None

    return AssimetriaResumo(
        total=assimetria_cache["total"],
        sobrecomprados=assimetria_cache["sobrecomprados"],
        sobrevendidos=assimetria_cache["sobrevendidos"],
        criticas=criticas,
        altas=altas,
        moderadas=moderadas,
        avg_volatilidade=avg_vol
    )


@router.get("/ticker/{ticker}")
async def get_assimetria_ticker(ticker: str):
    """
    Retorna analise de assimetria para um ticker especifico.
    """
    if not assimetria_cache["signals"]:
        raise HTTPException(status_code=404, detail="Nenhum dado de assimetria disponivel")

    # Normalizar ticker (remover .SA se presente)
    ticker_clean = ticker.replace(".SA", "").upper()

    # Buscar ticker
    signal = next(
        (s for s in assimetria_cache["signals"] if s["ticker"].upper() == ticker_clean),
        None
    )

    if not signal:
        raise HTTPException(
            status_code=404,
            detail=f"Ticker {ticker} nao encontrado ou nao atende aos criterios de assimetria (|Z-Score| >= 2.0)"
        )

    return signal


@router.get("/oportunidades")
async def get_oportunidades(
    nivel: Optional[str] = Query(None, description="Filtrar por nivel: Critica, Alta ou Moderada")
):
    """
    Retorna oportunidades de assimetria, opcionalmente filtradas por nivel.
    """
    if not assimetria_cache["signals"]:
        return {"oportunidades": []}

    signals = assimetria_cache["signals"]

    if nivel:
        signals = [s for s in signals if s["nivel_oportunidade"] == nivel]

    return {
        "total": len(signals),
        "nivel": nivel or "Todos",
        "oportunidades": signals
    }


@router.post("/upload")
async def upload_assimetria_signals(payload: dict):
    """
    Endpoint para receber sinais de assimetria do GitHub Actions.

    Payload esperado:
    {
        "assimetria_signals": [...],
        "data_atualizacao": "2025-10-15T10:30:00"
    }
    """
    try:
        signals = payload.get("assimetria_signals", [])

        if not signals:
            raise HTTPException(
                status_code=400,
                detail="Payload deve conter 'assimetria_signals'"
            )

        # Contar sobrecomprados e sobrevendidos
        sobrecomprados = len([s for s in signals if s["status"] == "Sobrecomprado"])
        sobrevendidos = len([s for s in signals if s["status"] == "Sobrevendido"])

        # Atualizar cache
        assimetria_cache["data"] = datetime.now().strftime("%d/%m/%Y")
        assimetria_cache["total"] = len(signals)
        assimetria_cache["sobrecomprados"] = sobrecomprados
        assimetria_cache["sobrevendidos"] = sobrevendidos
        assimetria_cache["signals"] = signals
        assimetria_cache["updated_at"] = payload.get(
            "data_atualizacao",
            datetime.now().isoformat()
        )

        return {
            "success": True,
            "message": f"Recebidos {len(signals)} sinais de assimetria",
            "resumo": {
                "total": len(signals),
                "sobrecomprados": sobrecomprados,
                "sobrevendidos": sobrevendidos
            }
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erro ao processar sinais: {str(e)}")


@router.get("/teste")
async def teste_assimetria():
    """
    Endpoint de teste para verificar se o modulo esta funcionando.
    """
    return {
        "modulo": "assimetria",
        "status": "online",
        "cache_status": {
            "tem_dados": len(assimetria_cache["signals"]) > 0,
            "total_signals": assimetria_cache["total"],
            "ultima_atualizacao": assimetria_cache["updated_at"]
        }
    }
