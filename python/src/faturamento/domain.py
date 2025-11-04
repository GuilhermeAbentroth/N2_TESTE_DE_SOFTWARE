from dataclasses import dataclass, field
from typing import List

@dataclass
class ItemFatura:
    descricao: str
    quantidade: int
    preco_unitario: float

    # (Item 3) Validação de exceção será adicionada aqui