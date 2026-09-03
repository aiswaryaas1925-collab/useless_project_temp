from fastapi import APIRouter
from models import AskRequest, AskResponse, CharacterResponse, RagDebug
from rag.retriever import retrieve_terrible_advice
from services.groq_service import groq_service

router = APIRouter(tags=["Ask"])


@router.post("/ask", response_model=AskResponse)
async def ask_question(request: AskRequest):
    # 1. Retrieve relevant terrible advice from FAISS vector store
    retrieved_examples = retrieve_terrible_advice(query=request.question, top_k=3)

    # 2. Generate responses for all 3 characters via Groq (with mock fallback)
    raw_responses = groq_service.generate_all_responses(
        user_question=request.question,
        retrieved_advice=retrieved_examples
    )

    character_responses = [CharacterResponse(**resp) for resp in raw_responses]

    debug_info = RagDebug(
        retrieved_examples=retrieved_examples,
        pipeline=[
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

    return AskResponse(
        responses=character_responses,
        disclaimer="This AI intentionally generates bad advice for entertainment. Do not follow its advice.",
        rag_debug=debug_info
    )