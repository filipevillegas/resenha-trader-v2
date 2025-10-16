"""
Modelos de dados para o módulo de Assimetria.
"""

from typing import List, Optional
from pydantic import BaseModel, Field
from datetime import datetime


class AssimetriaSignal(BaseModel):
    """Modelo de um sinal individual de assimetria."""

    ticker: str = Field(..., description="Código do ativo (ex: PETR4)")
    valor_atual: float = Field(..., description="Preço atual do ativo")
    media_6m: float = Field(..., description="Média móvel de 6 meses")
    z_score: float = Field(..., description="Z-Score (distância em desvios padrão)")
    volatilidade_anualizada: float = Field(..., description="Volatilidade anualizada")
    status: str = Field(..., description="Status: Sobrecomprado ou Sobrevendido")
    nivel_oportunidade: str = Field(..., description="Nível: Crítica, Alta ou Moderada")

    class Config:
        json_schema_extra = {
            "example": {
                "ticker": "PETR4",
                "valor_atual": 38.50,
                "media_6m": 35.20,
                "z_score": 2.3,
                "volatilidade_anualizada": 0.35,
                "status": "Sobrecomprado",
                "nivel_oportunidade": "Alta"
            }
        }


class AssimetriaResumo(BaseModel):
    """Resumo estatístico dos sinais de assimetria."""

    total: int = Field(..., description="Total de sinais")
    sobrecomprados: int = Field(..., description="Quantidade de ativos sobrecomprados")
    sobrevendidos: int = Field(..., description="Quantidade de ativos sobrevendidos")
    criticas: int = Field(..., description="Oportunidades críticas (|Z| >= 3)")
    altas: int = Field(..., description="Oportunidades altas (2.5 <= |Z| < 3)")
    moderadas: int = Field(..., description="Oportunidades moderadas (2 <= |Z| < 2.5)")
    avg_volatilidade: Optional[float] = Field(None, description="Volatilidade média")

    class Config:
        json_schema_extra = {
            "example": {
                "total": 25,
                "sobrecomprados": 14,
                "sobrevendidos": 11,
                "criticas": 5,
                "altas": 8,
                "moderadas": 12,
                "avg_volatilidade": 0.28
            }
        }


class AssimetriaResponse(BaseModel):
    """Resposta da API com sinais de assimetria."""

    data: str = Field(..., description="Data da análise (formato DD/MM/YYYY)")
    total: int = Field(..., description="Total de sinais")
    sobrecomprados: int = Field(..., description="Quantidade de sobrecomprados")
    sobrevendidos: int = Field(..., description="Quantidade de sobrevendidos")
    signals: List[AssimetriaSignal] = Field(..., description="Lista de sinais")
    updated_at: str = Field(..., description="Data/hora da última atualização")

    class Config:
        json_schema_extra = {
            "example": {
                "data": "15/10/2025",
                "total": 25,
                "sobrecomprados": 14,
                "sobrevendidos": 11,
                "signals": [
                    {
                        "ticker": "PETR4",
                        "valor_atual": 38.50,
                        "media_6m": 35.20,
                        "z_score": 2.3,
                        "volatilidade_anualizada": 0.35,
                        "status": "Sobrecomprado",
                        "nivel_oportunidade": "Alta"
                    }
                ],
                "updated_at": "2025-10-15T10:30:00"
            }
        }
