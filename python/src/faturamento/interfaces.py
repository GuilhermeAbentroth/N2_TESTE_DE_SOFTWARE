from abc import ABC, abstractmethod
from typing import Dict, Any, List
from .domain import Fatura

class FaturaRepository(ABC):
    @abstractmethod
    def salvar(self, fatura: Fatura) -> None: pass

    @abstractmethod
    def buscar_por_id(self, fatura_id: str) -> Fatura | None: pass

class EmailService(ABC):
    @abstractmethod
    def enviar_cobranca(self, email_cliente: str, fatura_id: str, valor: float) -> bool: pass

class GatewayPagamento(ABC):
    @abstractmethod
    def pagar(self, dados_pagamento: Dict[str, Any]) -> Dict[str, Any]: pass