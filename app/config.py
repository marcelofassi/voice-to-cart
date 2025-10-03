
from __future__ import annotations
from typing import Dict, Any
import yaml
from .schemas import ConfigModel

class ConfigManager:
    """Carga y entrega configuración dinámica para el procesamiento y el LLM."""
    def __init__(self) -> None:
        self._config: ConfigModel = ConfigModel()

    @property
    def config(self) -> ConfigModel:
        return self._config

    def load_from_dict(self, data: Dict[str, Any]) -> ConfigModel:
        self._config = ConfigModel(**data)
        return self._config

    def load_from_yaml(self, yaml_text: str) -> ConfigModel:
        data = yaml.safe_load(yaml_text) or {}
        return self.load_from_dict(data)

    def to_dict(self) -> Dict[str, Any]:
        return self._config.model_dump()
