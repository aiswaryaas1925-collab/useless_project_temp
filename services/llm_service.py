import os
import json
from typing import List, Dict, Any
from groq import Groq
from dotenv import load_dotenv

load_dotenv()

GROQ_API_KEY = os.getenv("GROQ_API_KEY", "").strip()
client = Groq(api_key=GROQ_API_KEY)


def generate_bad_advice(query: str, retrieved_context: List[str]) -> List[Dict[str, Any]]:
    """
    Generates comedic, terrible Malayalam advice for the 3 characters:
    - upadeshi (നാട്ടിലെ ഉപദേശി)
    - chechi (ചേച്ചി)
    - reddit_maman (Reddit മാമൻ)
    """
    context_str = "\n".join([f"- {item}" for item in retrieved_context])

    prompt = f"""You are the core intelligence for 'Worst Advice AI' (Malayalam edition).
The user is asking for advice on: "{query}"

Here are examples of terrible, absurd Malayalam advice retrieved from our knowledge base:
{context_str}

Generate terrible, comedic, bad advice for EXACTLY these three distinct personas:
1. "upadeshi": Older conservative moral neighborhood uncle ('നാട്ടിലെ ഉപദേശി').
2. "chechi": Sarcastic, practical elder sister ('ചേച്ചി').
3. "reddit_maman": Tech-savvy, meme-loving Reddit bro ('Reddit മാമൻ').

Requirements:
- Each character must output 1-2 punchy sentences in Malayalam (reddit_maman can mix Malayalam and English/Manglish memes).
- The advice must be absurd and clearly for entertainment purposes.
- Assign a "badness" score between 70 and 100 for each.

Return ONLY a valid JSON object matching this schema:
{{
  "responses": [
    {{
      "character": "upadeshi",
      "text": "advice in Malayalam here",
      "badness": 80
    }},
    {{
      "character": "chechi",
      "text": "advice in Malayalam here",
      "badness": 85
    }},
    {{
      "character": "reddit_maman",
      "text": "advice in Malayalam/Manglish here",
      "badness": 95
    }}
  ]
}}
"""

    try:
        completion = client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=[
                {"role": "system", "content": "You output strictly valid JSON."},
                {"role": "user", "content": prompt}
            ],
            response_format={"type": "json_object"},
            temperature=0.8,
        )
        data = json.loads(completion.choices[0].message.content)
        return data.get("responses", [])
    except Exception as e:
        print(f"[LLM Bad Advice Error]: {e}")
        return [
            {
                "character": "upadeshi",
                "text": "മോനേ, നാട്ടുകാർ പറയുന്നത് കേൾക്ക്: ക്ലാസ് കട്ട് ചെയ്യാൻ വേണ്ടി എല്ലാ ആഴ്ചയും പുതിയ ബന്ധുക്കൾക്ക് അസുഖം വരുത്തുക.",
                "badness": 80
            },
            {
                "character": "chechi",
                "text": "കുട്ടാ ചേച്ചി പറഞ്ഞത് കേൾക്ക്: ഓഫീസിൽ നിന്ന് നേരത്തെ പോകാൻ ലാപ്ടോപ്പിൽ വ്യാജ എറർ സ്ക്രീൻ സേവർ ഇട്ടുവെക്കുക.",
                "badness": 85
            },
            {
                "character": "reddit_maman",
                "text": "Bro pro tip: സീൻ ആക്കാതെ അറ്റൻഡൻസ് ലിസ്റ്റിൽ സ്വന്തമായി ഒപ്പിട്ടു വെക്ക്. Absolute cinema!",
                "badness": 95
            }
        ]


def generate_argument(attacker_id: str, defender_id: str, original_topic: str, original_advice: str) -> dict:
    """
    Generates a counter-argument/roast from attacker against defender's advice in Malayalam.
    """
    persona_prompts = {
        "upadeshi": "You are 'നാട്ടിലെ ഉപദേശി'. Criticize the other person's advice from a traditional, moral high ground.",
        "chechi": "You are 'ചേച്ചി'. Roast the other person's advice with practical, sarcastic elder-sister scolding.",
        "reddit_maman": "You are 'Reddit മാമൻ'. Mock the advice with internet slang, sarcasm, and absurd counter-suggestions."
    }

    attacker_persona = persona_prompts.get(attacker_id, persona_prompts["reddit_maman"])

    prompt = f"""{attacker_persona}
The user asked about: "{original_topic}"
The character '{defender_id}' gave this advice: "{original_advice}"

Task:
Respond directly to '{defender_id}', roasting why their advice is absurd and why your idea is better.
Keep the response in natural Malayalam (or Manglish if Reddit Maman), punchy, comedic, and within 2-3 sentences.
Return ONLY valid JSON matching this schema:
{{
  "argument_text": "your response here in Malayalam",
  "badness": 88
}}
"""
    try:
        completion = client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=[
                {"role": "system", "content": "You output strictly valid JSON."},
                {"role": "user", "content": prompt}
            ],
            response_format={"type": "json_object"},
            temperature=0.8,
        )
        return json.loads(completion.choices[0].message.content)
    except Exception as e:
        print(f"[LLM Argue Error]: {e}")
        return {
            "argument_text": "ഇതൊരു വല്ലാത്ത ഉപദേശമായിപ്പോയി, ഇതിലും ഭേദം ഒന്നും ചെയ്യാതിരിക്കുന്നതാണ്!",
            "badness": 75
        }