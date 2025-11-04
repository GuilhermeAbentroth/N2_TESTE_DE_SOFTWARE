import pytest
from src.faturamento.domain import ItemFatura
from src.faturamento.services import FaturaService


# (Item 4: Teste Parametrizado)
@pytest.mark.parametrize(
    "itens_input, cupom, esperado",
    [
        # Cenário 1: 2 itens (R$ 20), sem cupom. Total c/ 6% imposto = 21.20
        ([ItemFatura(descricao="Item A", quantidade=2, preco_unitario=10.0)], 0, 21.20),

        # Cenário 2: 1 item (R$ 100), com cupom 10%. Total c/ 6% imposto (106) - 10% = 95.40
        ([ItemFatura(descricao="Item B", quantidade=1, preco_unitario=100.0)], 10, 95.40),
    ]
)
def test_calculo_total_fatura_parametrizado(itens_input, cupom, esperado):
    service = FaturaService()

    total = service.calcular_total_fatura(itens_input, cupom_pct=cupom)

    # pytest.approx é usado para comparar números de ponto flutuante (floats)
    assert total == pytest.approx(esperado)

# (Item 3: Teste de Exceção)
@pytest.mark.parametrize("cupom_invalido", [-10, 101, -0.1])
def test_excecao_cupom_invalido(cupom_invalido):
    service = FaturaService()
    with pytest.raises(ValueError, match="Cupom de desconto deve estar entre 0 e 100"):
        service.calcular_total_fatura(
            itens=[ItemFatura("Item A", 1, 10.0)],
            cupom_pct=cupom_invalido
        )