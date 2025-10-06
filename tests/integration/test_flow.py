from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_message_to_cart_flow():
    payload = {"source":"web","text":"agregá 2 manzanas y 1 banana"}
    resp = client.post("/message", json=payload)
    assert resp.status_code == 200
    data = resp.json()
    assert data["detected"]["intent"] in ["add_to_cart","buy"]
    assert len(data["detected"]["items"]) >= 1
    cart = client.get("/cart").json()
    assert len(cart["items"]) >= 1
