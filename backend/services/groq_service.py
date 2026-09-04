import random
from typing import List, Optional
from groq import Groq
from config import settings
from characters.prompts import CHARACTERS_CONFIG, build_character_prompt

# Rich offline mock pool: if internet/Groq goes down, these provide dynamic responses
OFFLINE_POOL = {
    "upadeshi": [
        "മോനേ... പരീക്ഷയൊക്കെ വെറും മായയാണ്. നീ പുസ്തകം അടച്ചുവെച്ച് നാളെ നേരെ ചെന്ന് ഇൻവിജിലേറ്ററുടെ കണ്ണിൽ നോക്കി ആത്മവിശ്വാസത്തോടെ ഇരിക്കുക. ഒന്നും അറിയാത്തതാണ് ഏറ്റവും വലിയ അറിവ്!",
        "മോനേ, ജീവിതത്തിൽ ഏറ്റവും പ്രധാനം മനസ്സിന്റെ സമാധാനമാണ്. ഈ പ്രശ്നം കണ്ട് ടെൻഷൻ അടിക്കാതെ പോയി ഒരു ചായ കുടിച്ച് കിടന്നുറങ്ങൂ. ബാക്കി നാളെ വഴിപോലെ വരും.",
        "ഞാൻ നിന്റെ പ്രായത്തിൽ ഇതൊക്കെ എത്ര കണ്ടതാ! ഒന്നിനും പോകാതെ മിണ്ടാതിരിക്കുക, അതാണ് ഏറ്റവും നല്ല പരിഹാരം."
    ],
    "chechi": [
        "നീ tension അടിക്കണ്ട കുട്ടാ! ഇന്ന് രാത്രി മുഴുവൻ ഇൻസ്റ്റാഗ്രാമിൽ reels കണ്ടു മൈൻഡ് റിലാക്സ് ചെയ്യ്. നാളെ രാവിലെ തലകറങ്ങി വീഴുന്ന പോലെ അഭിനയിച്ചാൽ re-exam എഴുതാം. ഞാൻ പണ്ട് ട്രൈ ചെയ്തതാ!",
        "പേടിക്കാതെ കുട്ടാ, ചേച്ചി ഒരു വഴി പറഞ്ഞുതരാം. ആരോടും ഒന്നും പറയണ്ട, ഫോൺ സ്വിച്ച് ഓഫ് ചെയ്ത് വെച്ചാൽ പകുതി പ്രശ്നവും തനിയെ തീരും!",
        "നീ കാര്യം വിട്! നമ്മൾ കാരണം ആരും ബുദ്ധിമുട്ടരുത്, അതുകൊണ്ട് ആ പണി അങ്ങ് ഉപേക്ഷിക്കുന്നതാണ് നിന്റെ ആരോഗ്യത്തിന് നല്ലത്."
    ],
    "reddit_maman": [
        "Bro, studying or stressing one day before is a rookie mistake. Better start a crypto dropshipping agency at 3 AM. Mark Zuckerberg dropout അല്ലായിരുന്നോ? Hall ticket എടുത്ത് റോക്കറ്റ് ഉണ്ടാക്കി വിട്!",
        "Skill issue bro! Just touch some grass and uninstall the app. ജീവിതം എന്ന് പറയുന്നത് ഇതിലും വലിയ കോമഡിയാണ്.",
        "100% bad idea incoming: പ്രോബ്ലം ഫേസ് ചെയ്യുന്നതിന് പകരം ഒരു ലിങ്ക്ഡ്ഇൻ ഇൻഫ്ലുവൻസർ പോസ്റ്റ് എഴുതി വിട്, instant fame!"
    ]
}


class GroqService:
    def __init__(self):
        self._client: Optional[Groq] = None
        self._init_client()

    def _init_client(self):
        # Only initialize if a plausible Groq key exists
        if settings.GROQ_API_KEY and settings.GROQ_API_KEY.startswith("gsk_") and not settings.MOCK_MODE:
            try:
                self._client = Groq(api_key=settings.GROQ_API_KEY)
            except Exception as e:
                print(f"[GroqService] Initialization error: {e}. Defaulting to offline mode.")
                self._client = None
        else:
            self._client = None

    def _get_offline_response(self, character_id: str, retrieved_advice: List[str]) -> str:
        """Returns a relevant offline response using retrieved RAG advice or curated pool."""
        if retrieved_advice:
            base_advice = random.choice(retrieved_advice)
            if character_id == "upadeshi":
                return f"മോനേ, നാട്ടുകാർ പറയുന്നത് കേൾക്ക്: {base_advice}"
            elif character_id == "chechi":
                return f"കുട്ടാ ചേച്ചി പറഞ്ഞത് കേൾക്ക്: {base_advice}"
            else:
                return f"Bro pro tip: {base_advice} Absolute cinema!"

        pool = OFFLINE_POOL.get(character_id, ["മോനേ, ഒരു വഴിയുമില്ല!"])
        return random.choice(pool)

    def generate_single_character_response(
        self,
        character_id: str,
        user_question: str,
        retrieved_advice: List[str]
    ) -> str:
        if not self._client or settings.MOCK_MODE:
            return self._get_offline_response(character_id, retrieved_advice)

        prompt = build_character_prompt(character_id, user_question, retrieved_advice)

        try:
            chat_completion = self._client.chat.completions.create(
                messages=[{"role": "user", "content": prompt}],
                model=settings.GROQ_MODEL,
                temperature=0.85,
                max_tokens=220,
                timeout=5.0
            )
            text = chat_completion.choices[0].message.content
            if text and text.strip():
                return text.strip()
            return self._get_offline_response(character_id, retrieved_advice)

        except Exception as err:
            print(f"[GroqService] Online call failed ({err.__class__.__name__}). Falling back to offline response.")
            return self._get_offline_response(character_id, retrieved_advice)

    def generate_all_responses(
        self,
        user_question: str,
        retrieved_advice: List[str]
    ) -> List[dict]:
        character_ids = ["upadeshi", "chechi", "reddit_maman"]
        results = []

        for cid in character_ids:
            text = self.generate_single_character_response(cid, user_question, retrieved_advice)
            conf = CHARACTERS_CONFIG[cid]
            results.append({
                "character": cid,
                "name": conf["name"],
                "text": text,
                "audio_url": None,
                "badness": conf["baseline_badness"]
            })

        return results


groq_service = GroqService()


def generate_argument_roast(attacker: str, defender: str, topic: str, advice: str) -> str:
    """
    Generates a comedic Malayalam roast from one persona targeting another's advice.
    Uses Groq LLM if available, otherwise falls back to character-specific templates.
    """
    fallback_roasts = {
        "reddit_maman": f"Bro, what kind of dead advice is this? '{advice}' is a total L take. Even Reddit bots have better ideas than this!",
        "chechi": f"അയ്യോ കഷ്ടം! {advice} എന്ന് കേട്ടാൽ ആരും ചിരിച്ചുപോകും. ഇതിലും ഭേദം ഒന്നും ചെയ്യാതിരിക്കുന്നതാണ് കുട്ടാ!",
        "upadeshi": f"ഞങ്ങളുടെ കാലത്തൊന്നും ഇങ്ങനെയൊരു മണ്ടത്തരം കേട്ടിട്ടില്ല! {advice} എന്നൊക്കെ കേട്ട് ആരെങ്കിലും ഇറങ്ങിപ്പുറപ്പെടുമോ?"
    }

    if groq_service._client and not settings.MOCK_MODE:
        prompt = (
            f"You are roleplaying as '{attacker}', a comedic Malayalam character. "
            f"Roast '{defender}' who gave this terrible advice on the topic '{topic}': '{advice}'. "
            f"Write a sharp, funny, sarcastic counter-roast in 1-2 sentences using Manglish/Malayalam. "
            f"Do not give good advice; make it even more absurd."
        )
        try:
            chat_completion = groq_service._client.chat.completions.create(
                messages=[{"role": "user", "content": prompt}],
                model=settings.GROQ_MODEL,
                temperature=0.9,
                max_tokens=150,
                timeout=5.0
            )
            content = chat_completion.choices[0].message.content
            if content and content.strip():
                return content.strip()
        except Exception as e:
            print(f"[GroqService] Argue call failed: {e}. Using fallback roast.")

    return fallback_roasts.get(
        attacker,
        f"ഇതൊരു വല്ലാത്ത ഉപദേശമായിപ്പോയി! ഇതിലും ഭേദം ഒന്നും ചെയ്യാതിരിക്കുന്നതാണ്."
    )