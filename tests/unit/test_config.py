from app.config.manager import ConfigManager, AppConfig
import json

def test_load_from_json_ok():
    cm = ConfigManager()
    cfg = {"tone":"formal","constraints":{"forbid_oos":False,"max_items_per_message":5}}
    cm.load_from_string(json.dumps(cfg), "json")
    cur = cm.current_config()
    assert cur.tone == "formal"
    assert cur.constraints.max_items_per_message == 5
