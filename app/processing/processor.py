from __future__ import annotations
from typing import Dict, Any
from app.api.schemas import MessageRequest, MessageResponse, DetectedProducts, ProductItem
from app.llm.mock import RuleBasedLLM
from app.catalog.repository import CatalogRepository
from app.cart.cart import CartService
from app.config.manager import AppConfig

class MessageProcessor:
    def __init__(self, catalog_repo: CatalogRepository, cart_service: CartService):
        self.catalog_repo = catalog_repo
        self.cart_service = cart_service
        self.engine = RuleBasedLLM()

    def handle_message(self, payload: MessageRequest, config: AppConfig, tone: str = "amigable") -> MessageResponse:
        # 1) Transcripción de audio (mock: no implementado); usar texto si vino
        text = payload.text or "[audio recibido]"
        # 2) LLM para intención + items
        ctx = {
            "tone": tone,
            "constraints": config.constraints.dict(),
            "preferences": config.preferences.dict(),
            "catalog_index": self.catalog_repo.index
        }
        analysis = self.engine.analyze(text, ctx)
        intent = analysis.get("intent", "unknown")
        raw_items = analysis.get("items", [])
        items: list[ProductItem] = []

        # 3) Validaciones contra catálogo y stock
        for it in raw_items[: config.constraints.max_items_per_message]:
            prod = self.catalog_repo.find_by_sku(it["sku"])
            if not prod:
                continue
            if config.constraints.forbid_oos and prod.get("stock", 0) <= 0:
                continue
            items.append(ProductItem(sku=prod["sku"], name=prod["name"], quantity=it.get("quantity", 1)))

        # 4) Actualizar carrito si la intención corresponde
        if intent in {"add_to_cart", "buy"}:
            for it in items:
                self.cart_service.add(it.sku, it.name, it.quantity, it.variant_id)

        detected = DetectedProducts(items=items, intent=intent, notes=analysis.get("notes"))
        return MessageResponse(detected=detected, cart=self.cart_service.get_state())
