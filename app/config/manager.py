from __future__ import annotations
from typing import Dict, Any
from pydantic import BaseModel, Field, ValidationError
import json, yaml, threading, os
from fastapi import Request

class Constraints(BaseModel):
    forbid_oos: bool = True
    max_items_per_message: int = 20

class Preferences(BaseModel):
    preferred_brands: list[str] = []
    inclusive_language: bool = True
    locale: str = "es-AR"
    currency: str = "ARS"
    channel_overrides: Dict[str, Dict[str, Any]] = {}

class AppConfig(BaseModel):
    tone: str = "amigable"
    constraints: Constraints = Field(default_factory=Constraints)
    preferences: Preferences = Field(default_factory=Preferences)

class _EnvVarLoader(yaml.SafeLoader):
    """YAML loader that resolves !env_var tags with environment variables."""


def _env_var_constructor(loader: yaml.SafeLoader, node: yaml.Node) -> str:
    """Resolve !env_var SOME_VAR[:default] tags when loading YAML files."""
    raw_value = loader.construct_scalar(node)
    if ":" in raw_value:
        var_name, default = raw_value.split(":", 1)
    else:
        var_name, default = raw_value, None

    var_name = var_name.strip()
    if not var_name:
        raise ValueError("El tag !env_var requiere un nombre de variable de entorno")

    value = os.getenv(var_name, default)
    if value is None:
        raise ValueError(f"Variable de entorno '{var_name}' no definida y sin valor por defecto")
    return value


_EnvVarLoader.add_constructor("!env_var", _env_var_constructor)


class ConfigManager:
    def __init__(self):
        self._lock = threading.RLock()
        # Default config
        self._config = AppConfig()

    def load_from_string(self, content: str, content_type: str = "json"):
        with self._lock:
            try:
                if content_type == "json":
                    data = json.loads(content)
                else:
                    data = yaml.load(content, Loader=_EnvVarLoader)
                self._config = AppConfig(**data)
            except (json.JSONDecodeError, yaml.YAMLError, ValidationError) as e:
                raise ValueError(f"Error de configuración: {e}")

    def load_file(self, path: str):
        content_type = "yaml" if path.endswith((".yml",".yaml")) else "json"
        with open(path, "r", encoding="utf-8") as f:
            self.load_from_string(f.read(), content_type=content_type)

    def current_config(self) -> AppConfig:
        with self._lock:
            return self._config

def get_config_manager(request: Request) -> ConfigManager:
    return request.app.state.config_manager
