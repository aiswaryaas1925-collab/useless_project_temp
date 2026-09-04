from typing import List, Optional
from pydantic import BaseModel, Field


# Base responses
class RootResponse(BaseModel):
    message: str


class HealthResponse(BaseModel):
    status: str


# Character card response
class CharacterResponse(BaseModel):
    character: str = Field(..., description="Unique identifier: upadeshi | chechi | reddit_maman")
    name: str = Field(..., description="Display name in Malayalam")
    text: str = Field(..., description="Terrible advice response in Malayalam/Manglish")
    audio_url: Optional[str] = Field(None, description="URL to generated audio file or null")
    badness: int = Field(..., ge=0, le=100, description="Badness score between 0 and 100")


# RAG debug container
class RagDebug(BaseModel):
    retrieved_examples: List[str] = Field(default_factory=list)
    pipeline: List[str] = Field(
        default_factory=lambda: [
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
    )


# POST /ask request schema
class AskRequest(BaseModel):
    question: str = Field(..., min_length=1, description="User question or dilemma")
    language: Optional[str] = Field("malayalam", description="Language preference")


# POST /ask response schema
class AskResponse(BaseModel):
    responses: List[CharacterResponse]
    disclaimer: str = (
        "This AI intentionally generates bad advice for entertainment. Do not follow its advice."
    )
    rag_debug: RagDebug