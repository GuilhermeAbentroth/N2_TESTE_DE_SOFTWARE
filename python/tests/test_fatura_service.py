import pytest
import time
from typing import Dict, Any


from src.faturamento.domain import Cliente, ItemFatura, Fatura
from src.faturamento.interfaces import FaturaRepository, EmailService, GatewayPagamento
from src.faturamento.services import FaturaService
from src.faturamento.repositories import InMemoryFaturaRepository




class StubEmailService(EmailService):
    """ (Item 5 - Stub) """

    def __init__(self):
        self.mensagens_enviadas = []

    def enviar_cobranca(self, email_cliente: str, fatura_id: str, valor: float) -> bool:
        self.mensagens_enviadas.append({"para": email_cliente, "fatura": fatura_id})
        return True




@pytest.fixture
def repo_em_memoria() -> FaturaRepository:
    return InMemoryFaturaRepository()


@pytest.fixture
def stub_email() -> StubEmailService:
    return StubEmailService()


@pytest.fixture
def mock_gateway(mocker) -> GatewayPagamento:  # mocker vem do pytest-mock
    """ (Item 5 - Mock) """
    return mocker.Mock(spec=GatewayPagamento)


@pytest.fixture
def service(repo_em_memoria, stub_email, mock_gateway) -> FaturaService:
    """Fixture principal: Monta o Serviço de Fatura com todas as dependências falsas."""
    return FaturaService(repo_em_memoria, stub_email, mock_gateway)


@pytest.fixture
def cliente_padrao() -> Cliente:
    return Cliente(id="cli-123", nome="Cliente Teste", email="teste@email.com")




@pytest.mark.parametrize(
    "itens_input, cupom, esperado",
    [
        ([ItemFatura(descricao="Item A", quantidade=2, preco_unitario=10.0)], 0, 21.20),
        ([ItemFatura(descricao="Item B", quantidade=1, preco_unitario=100.0)], 10, 95.40),
    ]
)
def test_calculo_total_fatura_parametrizado(service: FaturaService, itens_input, cupom, esperado):
    total = service.calcular_total_fatura(itens_input, cupom_pct=cupom)
    assert total == pytest.approx(esperado)


@pytest.mark.parametrize("cupom_invalido", [-10, 101])
def test_excecao_cupom_invalido(service: FaturaService, cupom_invalido):
    with pytest.raises(ValueError, match="Cupom de desconto deve estar entre 0 e 100"):
        service.calcular_total_fatura([], cupom_pct=cupom_invalido)




def test_fluxo_completo_pagamento_aprovado_com_mock_e_stub(
        service: FaturaService,
        repo_em_memoria: InMemoryFaturaRepository,
        stub_email: StubEmailService,
        mock_gateway: GatewayPagamento,
        cliente_padrao: Cliente
):
    """ Testa o fluxo ponta-a-ponta (Itens 5 e 6) """

    itens = [ItemFatura(descricao="Produto Teste", quantidade=1, preco_unitario=100.0)]
    total_esperado = 106.00


    resposta_gateway = {"status": "APROVADO", "id_transacao": "xyz-789"}
    mock_gateway.pagar.return_value = resposta_gateway


    fatura_processada = service.fechar_fatura(cliente_padrao, itens, cupom_pct=0)


    mock_gateway.pagar.assert_called_once()


    assert len(stub_email.mensagens_enviadas) == 1
    assert stub_email.mensagens_enviadas[0]["para"] == "teste@email.com"


    fatura_salva = repo_em_memoria.buscar_por_id(fatura_processada.id)
    assert fatura_salva is not None
    assert fatura_salva.status == "PAGA"



def test_performance_calculo_fatura(service: FaturaService):
    """Testa se o cálculo de uma fatura grande é rápido."""
    itens_grandes = [
        ItemFatura(descricao="Item", quantidade=1, preco_unitario=1.5)
        for _ in range(1000)
    ]


    t0 = time.perf_counter()


    service.calcular_total_fatura(itens_grandes, cupom_pct=15)


    t1 = time.perf_counter()

    duracao = t1 - t0


    assert duracao < 0.1