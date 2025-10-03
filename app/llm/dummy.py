
from __future__ import annotations
import re
from typing import List, Optional
from ..schemas import ProductItem, ConfigModel

# Patrón simple: '2 leches descremadas La Serenísima, 1 pan integral Fargo'
_SPLIT_RE = re.compile(r"\s*(?:,| y )\s*", flags=re.IGNORECASE)
_QUANTITY_RE = re.compile(r"^(?P<qty>\d+(?:\.\d+)?)\s+", flags=re.IGNORECASE)

def _guess_brand_and_variant(tokens: list[str]) -> tuple[Optional[str], Optional[str], str]:
    # Heurística muy simple: última palabra con mayúscula como brand, adjetivos comunes como variant
    brand = None
    variant = None
    adjectives = {"descremada", "descremadas", "entera", "integral", "sin", "light"}
    remaining = []
    for t in tokens:
        if t.lower() in adjectives and not variant:
            variant = t.lower()
        elif t[:1].isupper() and not brand:
            brand = t
        else:
            remaining.append(t)
    name = " ".join(remaining) if remaining else "producto"
    return brand, variant, name

class DummyLLM:
    """Implementación local que extrae productos con reglas básicas.
    Sustituir por OpenAI/Gemini implementando la misma interfaz.
    """
    def extract_products(self, message: str, config: ConfigModel) -> List[ProductItem]:
        items: List[ProductItem] = []
        if not message:
            return items
        for chunk in _SPLIT_RE.split(message.strip().strip('.')):
            if not chunk:
                continue
            qty = 1.0
            m = _QUANTITY_RE.match(chunk)
            if m:
                qty = float(m.group('qty'))
                chunk = chunk[m.end():]
            tokens = [t for t in chunk.split() if t]
            brand, variant, name = _guess_brand_and_variant(tokens)
            # prefer brands from config if present in text or as fallback
            pref_brands = [b.lower() for b in config.preferences.get("preferred_brands", [])]
            if not brand and pref_brands:
                for b in pref_brands:
                    if b in chunk.lower():
                        brand = b.title()
                        break
            items.append(ProductItem(name=name.lower(), quantity=qty, brand=brand, variant=variant))
        # Respeta límite de items
        max_items = int(config.constraints.get("max_items_per_message", 50))
        return items[:max_items]
