from dataclasses import dataclass, field
from typing import List, Optional
import uuid


@dataclass
class Cliente:
    id: str
    nome: str
    email: str


@dataclass
class ItemFatura:
    # --- CORRIGIDO ---
    # Campos sem valor padrão vêm PRIMEIRO
    descricao: str
    quantidade: int
    preco_unitario: float

    # Campo com valor padrão vem DEPOIS
    id: str = field(default_factory=lambda: str(uuid.uuid4()))

    def __post_init__(self):
        if self.quantidade <= 0:
            raise ValueError("Quantidade deve ser positiva")
        if self.preco_unitario < 0:
            raise ValueError("Preço não pode ser negativo")


@dataclass
class Pagamento:
    id: str
    fatura_id: str
    status: str  # "APROVADO" ou "RECUSADO"


@dataclass
class Fatura:
    # --- CORRIGIDO ---
    # Campos sem valor padrão vêm PRIMEIRO
    cliente_id: str

    # Campos com valor padrão vêm DEPOIS
    id: str = field(default_factory=lambda: str(uuid.uuid4()))
    itens: List[ItemFatura] = field(default_factory=list)
    status: str = "PENDENTE"  # PENDENTE, PAGA, RECUSADA
    total: float = 0.0
    id_pagamento: Optional[str] = None