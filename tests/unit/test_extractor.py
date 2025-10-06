from app.llm.mock import RuleBasedLLM

def test_rule_based_llm_extracts_by_name_and_qty():
    llm = RuleBasedLLM()
    ctx = {"catalog_index": {
        "SKU-APPLE-001":{"name":"Manzana Roja"},
        "SKU-BANANA-002":{"name":"Banana"},
    }}
    out = llm.analyze("agrega 2 manzanas y 3x banana", ctx)
    skus = {it["sku"] for it in out["items"]}
    assert "SKU-APPLE-001" in skus
    assert "SKU-BANANA-002" in skus
