"""
Módulo de Assimetria - Análise de Z-Score e Volatilidade.
"""

from .models import (
    AssimetriaSignal,
    AssimetriaResumo,
    AssimetriaResponse
)

# Cache em memória para armazenar sinais de assimetria
assimetria_cache = {
    "data": "",
    "total": 0,
    "sobrecomprados": 0,
    "sobrevendidos": 0,
    "signals": [],
    "updated_at": ""
}

__all__ = [
    "AssimetriaSignal",
    "AssimetriaResumo",
    "AssimetriaResponse",
    "assimetria_cache"
]