from fastapi import FastAPI
from app.api.routes import router
from app.config.manager import ConfigManager

app = FastAPI(title="Voice-to-Cart API", version="0.1.0")

# Global config manager (can be injected)
config_manager = ConfigManager()
app.state.config_manager = config_manager

# Include API routes
app.include_router(router)

@app.get("/", tags=["health"])
def root():
    return {"status": "ok", "service": "voice-to-cart"}
