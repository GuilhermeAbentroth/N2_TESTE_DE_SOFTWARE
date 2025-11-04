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

    descricao: str
    quantidade: int
    preco_unitario: float


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
    status: str


@dataclass
class Fatura:

    cliente_id: str


    id: str = field(default_factory=lambda: str(uuid.uuid4()))
    itens: List[ItemFatura] = field(default_factory=list)
    status: str = "PENDENTE"
    total: float = 0.0
    id_pagamento: Optional[str] = None