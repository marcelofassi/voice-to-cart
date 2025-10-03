
from app.schemas import MessageIn, ChannelEnum, MessageType
from app.processing.message_processor import MessageProcessor
from app.llm.dummy import DummyLLM
from app.config import ConfigManager

def test_processor_text():
    cfg = ConfigManager().config
    proc = MessageProcessor(DummyLLM(), cfg)
    msg = MessageIn(channel=ChannelEnum.web, type=MessageType.text, user_id="u1", text="2 leches descremadas La Serenísima, 1 pan integral Fargo")
    products, transcript = proc.process(msg)
    assert transcript is None
    assert len(products) == 2
    assert products[0].quantity == 2

def test_processor_audio():
    cfg = ConfigManager().config
    proc = MessageProcessor(DummyLLM(), cfg)
    msg = MessageIn(channel=ChannelEnum.whatsapp, type=MessageType.audio, user_id="u2", audio_url="http://example/audio.wav")
    products, transcript = proc.process(msg)
    assert transcript is not None
