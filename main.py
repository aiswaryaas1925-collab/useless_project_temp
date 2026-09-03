import os
from typing import List, Optional
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel

from services.rag_service import retrieve_bad_advice
from services.llm_service import generate_bad_advice, generate_argument
from services.tts_service import generate_speech

app = FastAPI(
    title="Worst Malayalam Advice AI",
    description="Intentionally terrible Malayalam advice with dynamic multi-character responses and argument engine."
)

# -----------------------------------------------------------------------------
# Static Files Setup (Audio)
# -----------------------------------------------------------------------------
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
AUDIO_DIR = os.path.join(BASE_DIR, "audio")
os.makedirs(AUDIO_DIR, exist_ok=True)

app.mount("/audio", StaticFiles(directory=AUDIO_DIR), name="audio")

# -----------------------------------------------------------------------------
# CORS Middleware
# -----------------------------------------------------------------------------
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# -----------------------------------------------------------------------------
# Pydantic Schemas
# -----------------------------------------------------------------------------
class AskRequest(BaseModel):
    query: str

class CharacterResponse(BaseModel):
    character: str
    name: str
    text: str
    audio_url: Optional[str] = None
    badness: int

class RAGDebug(BaseModel):
    retrieved_examples: List[str]
    pipeline: List[str]

class AskResponse(BaseModel):
    responses: List[CharacterResponse]
    disclaimer: str
    rag_debug: RAGDebug

class ArgueRequest(BaseModel):
    attacker: str        # e.g., "reddit_maman"
    defender: str        # e.g., "upadeshi"
    original_topic: str  # e.g., "attendance"
    original_advice: str # The advice to roast

class ArgueResponse(BaseModel):
    attacker: str
    defender: str
    argument_text: str
    badness: int
    audio_url: Optional[str] = None

# -----------------------------------------------------------------------------
# Character Configuration
# -----------------------------------------------------------------------------
CHARACTER_NAMES = {
    "upadeshi": "നാട്ടിലെ ഉപദേശി",
    "chechi": "ചേച്ചി",
    "reddit_maman": "Reddit മാമൻ"
}

# -----------------------------------------------------------------------------
# API Endpoints
# -----------------------------------------------------------------------------
@app.get("/")
def health_check():
    return {
        "status": "online",
        "message": "Worst Advice AI Backend is running."
    }

@app.post("/ask", response_model=AskResponse)
async def ask_endpoint(req: AskRequest):
    if not req.query.strip():
        raise HTTPException(status_code=400, detail="Query cannot be empty.")

    # 1. RAG retrieval
    retrieved_context = retrieve_bad_advice(req.query, k=3)

    # 2. LLM multi-character generation
    character_outputs = generate_bad_advice(req.query, retrieved_context)

    # 3. Audio generation and response formatting
    formatted_responses = []
    for out in character_outputs:
        char_id = out.get("character", "upadeshi")
        text = out.get("text", "")
        badness = out.get("badness", 80)

        audio_path = generate_speech(character_id=char_id, text=text)

        formatted_responses.append(
            CharacterResponse(
                character=char_id,
                name=CHARACTER_NAMES.get(char_id, char_id),
                text=text,
                audio_url=audio_path,
                badness=badness
            )
        )

    pipeline_steps = [
        "User question",
        "Embedding",
        "FAISS vector search",
        "Terrible advice retrieval",
        "Character personality",
        "Groq LLM",
        "Safety check",
        "Badness score",
        "Malayalam TTS"
    ]

    return AskResponse(
        responses=formatted_responses,
        disclaimer="This AI intentionally generates bad advice for entertainment. Do not follow its advice.",
        rag_debug=RAGDebug(
            retrieved_examples=retrieved_context,
            pipeline=pipeline_steps
        )
    )

@app.post("/argue", response_model=ArgueResponse)
async def argue_endpoint(req: ArgueRequest):
    if not req.original_advice.strip():
        raise HTTPException(status_code=400, detail="Original advice cannot be empty.")

    # 1. Generate comedic counter-argument
    result = generate_argument(
        attacker_id=req.attacker,
        defender_id=req.defender,
        original_topic=req.original_topic,
        original_advice=req.original_advice
    )
    
    # 2. Synthesize Malayalam audio via TTS
    arg_text = result.get("argument_text", "")
    audio_path = generate_speech(character_id=req.attacker, text=arg_text)

    return ArgueResponse(
        attacker=req.attacker,
        defender=req.defender,
        argument_text=arg_text,
        badness=result.get("badness", 80),
        audio_url=audio_path
    )