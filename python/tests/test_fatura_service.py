import pytest
import time
from typing import Dict, Any

# Importações do código de produção
from src.faturamento.domain import Cliente, ItemFatura, Fatura
from src.faturamento.interfaces import FaturaRepository, EmailService, GatewayPagamento
from src.faturamento.services import FaturaService
from src.faturamento.repositories import InMemoryFaturaRepository


# --- Dublês de Teste (Stubs/Mocks Manuais) ---

class StubEmailService(EmailService):
    """ (Item 5 - Stub) """

    def __init__(self):
        self.mensagens_enviadas = []

    def enviar_cobranca(self, email_cliente: str, fatura_id: str, valor: float) -> bool:
        self.mensagens_enviadas.append({"para": email_cliente, "fatura": fatura_id})
        return True


# --- Fixtures (Item 1: Ciclo de Vida) ---

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


# --- Testes de Cálculo (Itens 2, 3, 4) ---

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


# --- Teste de Integração (Item 6) e Mocks (Item 5) ---

def test_fluxo_completo_pagamento_aprovado_com_mock_e_stub(
        service: FaturaService,
        repo_em_memoria: InMemoryFaturaRepository,
        stub_email: StubEmailService,
        mock_gateway: GatewayPagamento,
        cliente_padrao: Cliente
):
    """ Testa o fluxo ponta-a-ponta (Itens 5 e 6) """
    # 1. Arrange (Preparação)
    itens = [ItemFatura(descricao="Produto Teste", quantidade=1, preco_unitario=100.0)]
    total_esperado = 106.00  # 100 * (1 + 0.06 de imposto)

    # Define a resposta esperada do Mock
    resposta_gateway = {"status": "APROVADO", "id_transacao": "xyz-789"}
    mock_gateway.pagar.return_value = resposta_gateway

    # 2. Act (Ação)
    fatura_processada = service.fechar_fatura(cliente_padrao, itens, cupom_pct=0)

    # 3. Assert (Verificação)
    # 3.1. Verifica se o gateway foi chamado corretamente
    mock_gateway.pagar.assert_called_once()

    # 3.2. Verifica se o e-mail foi enviado (Stub)
    assert len(stub_email.mensagens_enviadas) == 1
    assert stub_email.mensagens_enviadas[0]["para"] == "teste@email.com"

    # 3.3. Verifica se a fatura foi salva no repositório
    fatura_salva = repo_em_memoria.buscar_por_id(fatura_processada.id)
    assert fatura_salva is not None
    assert fatura_salva.status == "PAGA"