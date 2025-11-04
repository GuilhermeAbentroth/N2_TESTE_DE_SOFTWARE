from typing import List
from .domain import ItemFatura


class FaturaService:
    TAXA_IMPOSTO_SIMPLES: float = 0.06

    def calcular_total_fatura(self, itens: List[ItemFatura], cupom_pct: float = 0) -> float:

        subtotal = sum(item.quantidade * item.preco_unitario for item in itens)

        total_com_imposto = subtotal * (1 + self.TAXA_IMPOSTO_SIMPLES)

        if cupom_pct > 0:
            desconto = total_com_imposto * (cupom_pct / 100)
            total_final = total_com_imposto - desconto
        else:
            total_final = total_com_imposto

        return round(total_final, 2)