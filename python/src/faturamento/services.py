from typing import List
from .domain import ItemFatura


class FaturaService:
    TAXA_IMPOSTO_SIMPLES: float = 0.06  # Regra: 6% de imposto

    def calcular_total_fatura(self, itens: List[ItemFatura], cupom_pct: float = 0) -> float:

        # 1. Calcula o subtotal
        subtotal = sum(item.quantidade * item.preco_unitario for item in itens)

        # 2. Aplica o imposto (Regra de negócio)
        total_com_imposto = subtotal * (1 + self.TAXA_IMPOSTO_SIMPLES)

        # 3. Aplica o cupom de desconto (Regra de negócio)
        if cupom_pct > 0:
            desconto = total_com_imposto * (cupom_pct / 100)
            total_final = total_com_imposto - desconto
        else:
            total_final = total_com_imposto

        return round(total_final, 2)