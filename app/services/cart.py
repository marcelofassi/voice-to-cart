
from __future__ import annotations
from typing import Dict, List
from ..schemas import CartItem, CartState, ProductItem

class CartService:
    """Carritos en memoria, por user_id."""
    def __init__(self) -> None:
        self._carts: Dict[str, List[CartItem]] = {}

    def add_items(self, user_id: str, items: List[ProductItem]) -> CartState:
        cart = self._carts.setdefault(user_id, [])
        # merge simple: if same name+brand+variant, increase quantity
        for p in items:
            merged = False
            for existing in cart:
                if (existing.name.lower() == p.name.lower()
                    and (existing.brand or "").lower() == (p.brand or "").lower()
                    and (existing.variant or "").lower() == (p.variant or "").lower()):
                    existing.quantity += p.quantity
                    merged = True
                    break
            if not merged:
                cart.append(CartItem(**p.model_dump()))
        return CartState(user_id=user_id, items=cart)

    def get_cart(self, user_id: str) -> CartState:
        return CartState(user_id=user_id, items=self._carts.get(user_id, []))

    def clear(self, user_id: str) -> None:
        self._carts[user_id] = []
