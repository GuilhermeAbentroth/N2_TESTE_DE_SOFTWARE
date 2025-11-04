import pytest
from src.faturamento.domain import ItemFatura
from src.faturamento.services import FaturaService


@pytest.mark.parametrize(
    "itens_input, cupom, esperado",
    [
        ([ItemFatura(descricao="Item A", quantidade=2, preco_unitario=10.0)], 0, 21.20),

        ([ItemFatura(descricao="Item B", quantidade=1, preco_unitario=100.0)], 10, 95.40),
    ]
)
def test_calculo_total_fatura_parametrizado(itens_input, cupom, esperado):
    service = FaturaService()

    total = service.calcular_total_fatura(itens_input, cupom_pct=cupom)

    assert total == pytest.approx(esperado)