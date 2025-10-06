from typing import Dict, Any, List
import re
from app.llm.base import LLMEngine

SKU_PAT = re.compile(r"(SKU-[A-Z]+-[0-9]{3})", re.IGNORECASE)

class RuleBasedLLM(LLMEngine):
    """
    Motor de ejemplo: usa reglas simples para detectar intención y artículos.
    En producción, reemplazar por un cliente real (OpenAI/Gemini) que implemente LLMEngine.
    """
    def analyze(self, text: str, context: Dict[str, Any]) -> Dict[str, Any]:
        lower = text.lower()
        intent = "add_to_cart" if any(k in lower for k in ["agrega","añade","sumá","sumar","comprar","agregar","poner"]) else "browse"
        items = self._extract_items(lower, context.get("catalog_index", {}))
        notes = "Motor mock por reglas; reemplazable vía interfaz."
        return {"intent": intent, "items": items, "notes": notes}

    def _extract_items(self, text: str, catalog_index: Dict[str, Dict[str, Any]]) -> List[Dict[str, Any]]:
        results: List[Dict[str, Any]] = []
        # 1) Por SKU explícito
        for m in SKU_PAT.finditer(text):
            sku = m.group(1).upper()
            prod = catalog_index.get(sku)
            if prod:
                qty = self._extract_quantity_around(text, sku) or 1
                results.append({"sku": sku, "name": prod["name"], "quantity": qty})
        # 2) Por nombre básico "2 manzanas", "3x banana"
        name_qty = re.findall(r"(\d+)\s*x?\s*(manzana|banana|leche|pasta)", text)
        for qty_str, noun in name_qty:
            qty = int(qty_str)
            # Mapear a productos
            for sku, prod in catalog_index.items():
                if noun in prod["name"].lower():
                    results.append({"sku": sku, "name": prod["name"], "quantity": qty})
                    break
        # 3) fallback simple "una manzana"
        if not results:
            single = re.findall(r"(una|un)\s+(manzana|banana|leche|pasta)", text)
            for _, noun in single:
                for sku, prod in catalog_index.items():
                    if noun in prod["name"].lower():
                        results.append({"sku": sku, "name": prod["name"], "quantity": 1})
                        break
        return results

    def _extract_quantity_around(self, text: str, token: str) -> int:
        # Busca un número antes del token, ej "2 x SKU-XXXX"
        m = re.search(r"(\d+)\s*x?\s*" + re.escape(token.lower()), text)
        if m:
            try:
                return int(m.group(1))
            except:
                return 1
        return 1
