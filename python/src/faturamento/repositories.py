from .domain import Fatura
from .interfaces import FaturaRepository
from typing import Dict


class InMemoryFaturaRepository(FaturaRepository):
    """(Item 6) Repositório em memória para simular integração"""

    def __init__(self):
        self._db: Dict[str, Fatura] = {}

    def salvar(self, fatura: Fatura) -> None:
        self._db[fatura.id] = fatura

    def buscar_por_id(self, fatura_id: str) -> Fatura | None:
        return self._db.get(fatura_id)