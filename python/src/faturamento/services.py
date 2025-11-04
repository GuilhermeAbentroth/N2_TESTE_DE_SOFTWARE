from typing import List
from .domain import ItemFatura


class FaturaService:
    TAXA_IMPOSTO_SIMPLES: float = 0.06  # Regra: 6% de imposto

    def calcular_total_fatura(self, itens: List[ItemFatura], cupom_pct: float = 0) -> float:
        return 0.0