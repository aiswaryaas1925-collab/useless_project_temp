from fastapi import APIRouter
from models import AskRequest, AskResponse, CharacterResponse, RagDebug
from rag.retriever import retrieve_terrible_advice
from services.groq_service import groq_service
from services.safety_service import check_query_safety, SAFE_DEFLECTION_RESPONSES
from services.scoring_service import calculate_badness_score
from services.tts_service import generate_speech

router = APIRouter(tags=["Ask"])


@router.post("/ask", response_model=AskResponse)
async def ask_question(request: AskRequest):
    # 1. Safety verification
    is_safe, _ = check_query_safety(request.question)
    if not is_safe:
        deflection = [CharacterResponse(**item) for item in SAFE_DEFLECTION_RESPONSES]
        return AskResponse(
            responses=deflection,
            disclaimer="This query flagged safety rules. Emergency support and professional help should always be prioritized.",
            rag_debug=RagDebug(
                retrieved_examples=["[Safety Shield Activated - Generation Bypassed]"],
                pipeline=["User question", "Safety check (Triggered Deflection)"]
            )
        )

    # 2. Retrieve terrible advice from FAISS
    retrieved_examples = retrieve_terrible_advice(query=request.question, top_k=3)

    # 3. Generate persona responses
    raw_responses = groq_service.generate_all_responses(
        user_question=request.question,
        retrieved_advice=retrieved_examples
    )

    # 4. Badness scoring + TTS audio generation
    final_character_cards = []
    for item in raw_responses:
        cid = item["character"]
        text = item["text"]
        badness = calculate_badness_score(character_id=cid, advice_text=text)
        
        # Generate TTS audio URL (falls back to None if unavailable)
        audio_url = generate_speech(character_id=cid, text=text)
        
        final_character_cards.append(
            CharacterResponse(
                character=cid,
                name=item["name"],
                text=text,
                audio_url=audio_url,
                badness=badness
            )
        )

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
        responses=final_character_cards,
        disclaimer="This AI intentionally generates bad advice for entertainment. Do not follow its advice.",
        rag_debug=debug_info
    )