
from __future__ import annotations
from typing import Protocol, List
from ..schemas import ProductItem, ConfigModel

class LLMEngine(Protocol):
    """Interfaz para motores LLM intercambiables."""
    def extract_products(self, message: str, config: ConfigModel) -> List[ProductItem]:
        ...
