from typing import List, Optional, Dict, Any
from pydantic import BaseModel, Field, validator

class ProductItem(BaseModel):
    sku: str
    name: str
    quantity: int = Field(gt=0)
    variant_id: Optional[str] = None
    attributes: Dict[str, Any] = {}

class MessageRequest(BaseModel):
    source: str = Field(description="whatsapp | web", examples=["whatsapp","web"])
    text: Optional[str] = None
    audio_base64: Optional[str] = Field(default=None, description="Audio codificado en base64")

    @validator("source")
    def valid_source(cls, v):
        if v not in {"whatsapp", "web"}:
            raise ValueError("source must be 'whatsapp' or 'web'")
        return v

    @validator("text", always=True)
    def text_or_audio(cls, v, values):
        if not v and not values.get("audio_base64"):
            raise ValueError("Debe enviar 'text' o 'audio_base64'")
        return v

class DetectedProducts(BaseModel):
    items: List[ProductItem]
    intent: str
    notes: Optional[str] = None

class MessageResponse(BaseModel):
    detected: DetectedProducts
    cart: Dict[str, Any]

class ConfigUploadRequest(BaseModel):
    content: str
    content_type: str = Field(description="json | yaml", pattern="^(json|yaml)$")


class CartItem(BaseModel):
    sku: str
    name: str
    quantity: int
    variant_id: Optional[str] = None

class CartStateResponse(BaseModel):
    items: List[CartItem]
    total: float
    currency: str
