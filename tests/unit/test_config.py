from app.config.manager import ConfigManager
import json
import textwrap


def _load_yaml(cm: ConfigManager, yaml_content: str):
    cm.load_from_string(textwrap.dedent(yaml_content), "yaml")

def test_load_from_json_ok():
    cm = ConfigManager()
    cfg = {"tone":"formal","constraints":{"forbid_oos":False,"max_items_per_message":5}}
    cm.load_from_string(json.dumps(cfg), "json")
    cur = cm.current_config()
    assert cur.tone == "formal"
    assert cur.constraints.max_items_per_message == 5


def test_load_from_yaml_env_var(monkeypatch):
    cm = ConfigManager()
    monkeypatch.setenv("APP_TONE", "formal")

    _load_yaml(
        cm,
        """
        tone: !env_var APP_TONE
        constraints:
          max_items_per_message: 3
        """,
    )

    current = cm.current_config()
    assert current.tone == "formal"
    assert current.constraints.max_items_per_message == 3
