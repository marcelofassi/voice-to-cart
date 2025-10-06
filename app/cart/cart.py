from __future__ import annotations
from typing import List, Dict, Any, Optional
from dataclasses import dataclass, field

@dataclass
class CartItem:
    sku: str
    name: str
    quantity: int
    variant_id: Optional[str] = None

@dataclass
class CartState:
    items: List[CartItem] = field(default_factory=list)
    currency: str = "ARS"

class MockEcommerceAPI:
    """Simula integración con Woo/Shopify."""
    def add_line_item(self, sku: str, quantity: int, variant_id: Optional[str] = None) -> Dict[str, Any]:
        # En una integración real, llamaríamos a la API externa aquí.
        return {"status": "ok", "sku": sku, "quantity": quantity, "variant_id": variant_id}

class CartService:
    def __init__(self):
        self.state = CartState()
        self.api = MockEcommerceAPI()

    def add(self, sku: str, name: str, quantity: int, variant_id: Optional[str] = None):
        # Llamar mock ecommerce
        self.api.add_line_item(sku, quantity, variant_id)
        # Actualizar carrito local
        for it in self.state.items:
            if it.sku == sku and it.variant_id == variant_id:
                it.quantity += quantity
                return
        self.state.items.append(CartItem(sku=sku, name=name, quantity=quantity, variant_id=variant_id))

    def get_state(self) -> Dict[str, Any]:
        total = 0.0
        # En demo no tenemos precios por ítem en carrito; quedaría para integración real.
        return {
            "items": [vars(i) for i in self.state.items],
            "total": total,
            "currency": self.state.currency
        }

    def clear(self):
        self.state.items.clear()
