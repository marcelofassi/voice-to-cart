
from __future__ import annotations
from fastapi import FastAPI, HTTPException, Body, Query
from .schemas import MessageIn, MessageOut, CartState, ConfigModel
from .config import ConfigManager
from .services.cart import CartService
from .processing.message_processor import MessageProcessor
from .llm.dummy import DummyLLM

app = FastAPI(title="Voice-to-Cart API", version="0.1.0")

# Componentes singletons simples para demo
config_mgr = ConfigManager()
cart_service = CartService()
processor = MessageProcessor(llm=DummyLLM(), config=config_mgr.config)

@app.post("/message", response_model=MessageOut)
def post_message(message: MessageIn):
    if not message.text and message.type == message.type.text:
        raise HTTPException(status_code=400, detail="Se requiere 'text' para mensajes de tipo text.")
    if message.type == message.type.audio and not message.audio_url:
        raise HTTPException(status_code=400, detail="Se requiere 'audio_url' para mensajes de tipo audio.")
    products, transcript = processor.process(message)
    # TODO: aplicar políticas: no sugerir fuera de stock, etc. (aquí se integraría con inventario)
    cart_service.add_items(message.user_id, products)
    return MessageOut(detected_products=products, transcribed_text=transcript, config_applied=config_mgr.to_dict())

@app.post("/config", response_model=ConfigModel)
def post_config(payload: dict = Body(..., description="JSON completo o YAML como string en 'yaml'")):
    # Permite JSON directo o YAML string
    if "yaml" in payload and isinstance(payload["yaml"], str):
        cfg = config_mgr.load_from_yaml(payload["yaml"])
    else:
        cfg = config_mgr.load_from_dict(payload)
    processor.update_config(cfg)
    return cfg

@app.get("/cart", response_model=CartState)
def get_cart(user_id: str = Query(..., description="ID del usuario")):
    return cart_service.get_cart(user_id)
