from fastapi import APIRouter, Depends, Request, HTTPException
from fastapi.responses import JSONResponse
from app.api.schemas import MessageRequest, MessageResponse, ConfigUploadRequest, CartStateResponse
from app.processing.processor import MessageProcessor
from app.cart.cart import CartService
from app.config.manager import get_config_manager
from app.catalog.repository import CatalogRepository

router = APIRouter()

# Singletons (in-memory for demo)
catalog_repo = CatalogRepository()
cart_service = CartService()
processor = MessageProcessor(catalog_repo=catalog_repo, cart_service=cart_service)

@router.post("/message", response_model=MessageResponse, tags=["message"])
def receive_message(payload: MessageRequest, request: Request, cfg=Depends(get_config_manager)):
    try:
        # Resolve channel tone overrides
        config = cfg.current_config()
        channel = payload.source or "web"
        tone_override = config.preferences.channel_overrides.get(channel, {}).get("tone")
        effective_tone = tone_override or config.tone
        processing_result = processor.handle_message(payload, config=config, tone=effective_tone)
        return processing_result
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.post("/config", tags=["config"])
def upload_config(payload: ConfigUploadRequest, cfg=Depends(get_config_manager)):
    cfg.load_from_string(payload.content, content_type=payload.content_type)
    return {"status": "loaded", "content_type": payload.content_type}

@router.get("/cart", response_model=CartStateResponse, tags=["cart"])
def get_cart():
    return cart_service.get_state()
