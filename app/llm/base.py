from __future__ import annotations
from abc import ABC, abstractmethod
from typing import Any, Dict

class LLMEngine(ABC):
    @abstractmethod
    def analyze(self, text: str, context: Dict[str, Any]) -> Dict[str, Any]:
        """Return a dict with "intent" and optional "items" extracted and "notes"."""
        raise NotImplementedError
