from .domain import Fatura, ItemFatura, Cliente
from .interfaces import FaturaRepository, EmailService, GatewayPagamento
from typing import List


class FaturaService:
    TAXA_IMPOSTO_SIMPLES: float = 0.06  # Regra: 6% de imposto

    def __init__(
            self,
            repository: FaturaRepository,
            email_service: EmailService,
            gateway: GatewayPagamento
    ):
        self.repository = repository
        self.email_service = email_service
        self.gateway = gateway

    def calcular_total_fatura(self, itens: List[ItemFatura], cupom_pct: float = 0) -> float:
        # (O código anterior desta função continua aqui, inalterado)
        if not (0 <= cupom_pct <= 100):
            raise ValueError("Cupom de desconto deve estar entre 0 e 100")

        subtotal = sum(item.quantidade * item.preco_unitario for item in itens)
        total_com_imposto = subtotal * (1 + self.TAXA_IMPOSTO_SIMPLES)

        if cupom_pct > 0:
            desconto = total_com_imposto * (cupom_pct / 100)
            total_final = total_com_imposto - desconto
        else:
            total_final = total_com_imposto

        return round(total_final, 2)

    def fechar_fatura(self, cliente: Cliente, itens: List[ItemFatura], cupom_pct: float = 0) -> Fatura:
        """ (Item 6) Fluxo ponta-a-ponta """
        pass  # Stub inicial