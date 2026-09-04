from fastapi import APIRouter
from models import AskRequest, AskResponse, CharacterResponse, RagDebug
from rag.retriever import retrieve_terrible_advice
from services.groq_service import groq_service
from services.tts_service import text_to_speech_malayalam

router = APIRouter(tags=["Ask"])


@router.post("/ask", response_model=AskResponse)
async def ask_question(request: AskRequest):
    # 1. Retrieve relevant terrible advice from FAISS vector store
    try:
        retrieved_examples = retrieve_terrible_advice(query=request.question, top_k=3)
    except Exception as e:
        print(f"[RAG Retrieval Error]: {e}")
        retrieved_examples = []

    # 2. Generate responses for all 3 characters via Groq
    raw_responses = groq_service.generate_all_responses(
        user_question=request.question,
        retrieved_advice=retrieved_examples
    )

    # 3. Generate audio files for each character safely
    processed_responses = []
    for resp in raw_responses:
        text = resp.get("text", "")
        audio_url = resp.get("audio_url")
        
        # Synthesize audio if not already generated
        if not audio_url and text:
            try:
                # Passes only 'text' to match your function signature
                audio_url = text_to_speech_malayalam(text)
            except Exception as e:
                print(f"[TTS Synthesis Error]: {e}")
                audio_url = None

        resp["audio_url"] = audio_url
        processed_responses.append(CharacterResponse(**resp))

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
        responses=processed_responses,
        disclaimer="This AI intentionally generates bad advice for entertainment. Do not follow its advice.",
        rag_debug=debug_info
    )