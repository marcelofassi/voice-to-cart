from app.cart.cart import CartService

def test_cart_add_accumulates():
    cart = CartService()
    cart.add("SKU-1","Prod 1",2)
    cart.add("SKU-1","Prod 1",3)
    state = cart.get_state()
    assert state["items"][0]["quantity"] == 5
