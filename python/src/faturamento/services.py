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

        # (Item 3) Teste de exceção adicional
        if not itens:
            raise ValueError("Não é possível fechar uma fatura sem itens")

        # Cria a fatura e calcula o total
        fatura = Fatura(cliente_id=cliente.id, itens=itens)
        fatura.total = self.calcular_total_fatura(itens, cupom_pct)

        # Prepara os dados para o gateway (Mock)
        dados_pagamento = {
            "cliente_id": cliente.id,
            "valor": fatura.total,
            "fatura_id": fatura.id
        }

        # Chama o Gateway de Pagamento
        resposta = self.gateway.pagar(dados_pagamento)

        # Processa a resposta
        if resposta.get("status") == "APROVADO":
            fatura.status = "PAGA"
            fatura.id_pagamento = resposta.get("id_transacao")

            # Envia e-mail de cobrança (Stub)
            self.email_service.enviar_cobranca(cliente.email, fatura.id, fatura.total)

        else:
            fatura.status = "RECUSADA"

        # Salva o estado final da fatura (Repo em Memória)
        self.repository.salvar(fatura)
        return fatura