import os
from typing import Optional
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel

from config import settings
from models import HealthResponse, RootResponse
from routes.ask import router as ask_router
from services.groq_service import generate_argument_roast
from services.tts_service import text_to_speech_malayalam

app = FastAPI(
    title="The Worst Advice Committee API",
    description="നിങ്ങളുടെ പ്രശ്നം. ഞങ്ങളുടെ മൂന്ന് വിദഗ്ധർ. ഉപദേശം മാത്രം മോശം.",
    version="1.0.0",
)

# Explicit local development origins matching Vite default and incremented ports
allowed_origins = [
    "http://localhost:5173",
    "http://localhost:5174",
    "http://localhost:5175",
    "http://127.0.0.1:5173",
    "http://127.0.0.1:5174",
    "http://127.0.0.1:5175",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=allowed_origins,
    allow_credentials=False,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Audio directory setup and static file mounting
AUDIO_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "audio")
os.makedirs(AUDIO_DIR, exist_ok=True)

app.mount("/audio", StaticFiles(directory=AUDIO_DIR), name="audio")

# Include the core /ask endpoint router
app.include_router(ask_router)


# Argue data models and route
class ArgueRequest(BaseModel):
    attacker: str
    defender: str
    original_topic: str
    original_advice: str


class ArgueResponse(BaseModel):
    attacker: str
    defender: str
    argument_text: str
    badness: int
    audio_url: Optional[str] = None


@app.post("/argue", response_model=ArgueResponse, tags=["Argue"])
async def argue_endpoint(payload: ArgueRequest):
    roast_text = generate_argument_roast(
        attacker=payload.attacker,
        defender=payload.defender,
        topic=payload.original_topic,
        advice=payload.original_advice,
    )

    audio_path = text_to_speech_malayalam(roast_text)

    return ArgueResponse(
        attacker=payload.attacker,
        defender=payload.defender,
        argument_text=roast_text,
        badness=85,
        audio_url=audio_path,
    )


# Health check endpoints
@app.get("/", response_model=RootResponse, tags=["General"])
async def root():
    return {"message": "Worst Advice Committee backend is alive 💀"}


@app.get("/health", response_model=HealthResponse, tags=["General"])
async def health():
    return {"status": "ok"}