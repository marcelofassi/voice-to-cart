
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_post_message_and_cart():
    body = {
        "channel": "web",
        "type": "text",
        "user_id": "alice",
        "text": "agrega 3 cervezas IPA Patagonia, 1 papas Lays"
    }
    res = client.post("/message", json=body)
    assert res.status_code == 200
    data = res.json()
    assert "detected_products" in data
    res2 = client.get("/cart", params={"user_id": "alice"})
    assert res2.status_code == 200
    assert len(res2.json()["items"]) >= 1

def test_update_config_yaml():
    yaml_text = """
tone: formal
preferences:
  preferred_brands: ["Patagonia"]
"""
    res = client.post("/config", json={"yaml": yaml_text})
    assert res.status_code == 200
    assert res.json()["tone"] == "formal"
