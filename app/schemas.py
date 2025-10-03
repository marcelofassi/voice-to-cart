
from enum import Enum
from typing import List, Optional, Dict
from pydantic import BaseModel, Field, field_validator

class ChannelEnum(str, Enum):
    whatsapp = "whatsapp"
    web = "web"

class MessageType(str, Enum):
    text = "text"
    audio = "audio"

class ProductItem(BaseModel):
    name: str = Field(..., description="Nombre del producto (ej. leche descremada)")
    quantity: float = Field(default=1, description="Cantidad solicitada")
    brand: Optional[str] = Field(default=None, description="Marca preferida")
    variant: Optional[str] = Field(default=None, description="Variante (ej. descremada, integral)")
    attributes: Dict[str, str] = Field(default_factory=dict, description="Atributos clave/valor")
    notes: Optional[str] = None

class MessageIn(BaseModel):
    channel: ChannelEnum
    type: MessageType
    user_id: str = Field(..., description="Identificador del usuario/cliente")
    text: Optional[str] = None
    audio_url: Optional[str] = None

    @field_validator("text")
    @classmethod
    def validate_text_or_audio(cls, v, values):
        # Validación extra en endpoint
        return v

class MessageOut(BaseModel):
    detected_products: List[ProductItem]
    transcribed_text: Optional[str] = None
    config_applied: Dict = {}

class ConfigModel(BaseModel):
    tone: str = "amigable"
    constraints: Dict = Field(default_factory=dict)
    preferences: Dict = Field(default_factory=dict)
    parsing: Dict = Field(default_factory=dict)

class CartItem(ProductItem):
    pass

class CartState(BaseModel):
    user_id: str
    items: List[CartItem] = []
