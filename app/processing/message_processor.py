
from __future__ import annotations
from typing import List, Optional
from ..schemas import MessageIn, ProductItem, ConfigModel
from ..llm.base import LLMEngine

class MessageProcessor:
    def __init__(self, llm: LLMEngine, config: ConfigModel) -> None:
        self.llm = llm
        self.config = config

    def update_config(self, config: ConfigModel) -> None:
        self.config = config

    def transcribe(self, audio_url: str) -> str:
        # Placeholder: en producción integrar STT (Whisper, Google, etc.)
        return f"[transcripción simulada de {audio_url}]"

    def process(self, msg: MessageIn) -> tuple[List[ProductItem], Optional[str]]:
        text = msg.text
        transcript = None
        if msg.type == msg.type.audio:
            transcript = self.transcribe(msg.audio_url or "")
            text = transcript
        # Aca podríamos enriquecer el prompt con tono y restricciones para un LLM real
        products = self.llm.extract_products(text or "", self.config)
        return products, transcript
