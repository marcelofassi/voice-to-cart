from __future__ import annotations
from typing import Optional, Dict, Any
from pydantic import BaseModel, Field, ValidationError
import json, yaml, threading
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
                    data = yaml.safe_load(content)
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
