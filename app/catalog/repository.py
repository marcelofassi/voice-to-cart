from __future__ import annotations
import json, os
from typing import Dict, Any, Optional, List

DATA_PATH = os.environ.get("CATALOG_PATH", "/mnt/data/voice_to_cart/data/catalog.json")

class CatalogRepository:
    def __init__(self, path: str = DATA_PATH):
        self.path = path
        with open(self.path, "r", encoding="utf-8") as f:
            data = json.load(f)
        self.products = data.get("products", [])
        self.index: Dict[str, Dict[str, Any]] = {p["sku"].upper(): p for p in self.products}

    def find_by_sku(self, sku: str) -> Optional[Dict[str, Any]]:
        return self.index.get(sku.upper())

    def search_by_name(self, name_substr: str) -> List[Dict[str, Any]]:
        s = name_substr.lower()
        return [p for p in self.products if s in p["name"].lower()]
