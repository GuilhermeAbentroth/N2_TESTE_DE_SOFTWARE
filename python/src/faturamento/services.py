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

    @pytest.mark.parametrize("cupom_invalido", [-10, 101, -0.1])
    def test_excecao_cupom_invalido(cupom_invalido):
        service = FaturaService()
        with pytest.raises(ValueError, match="Cupom de desconto deve estar entre 0 e 100"):
            service.calcular_total_fatura(
                itens=[ItemFatura("Item A", 1, 10.0)],
                cupom_pct=cupom_invalido
            )