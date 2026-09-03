import os
import hashlib
from typing import Optional
from gtts import gTTS

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
AUDIO_DIR = os.path.join(BASE_DIR, "audio")
os.makedirs(AUDIO_DIR, exist_ok=True)


def generate_speech(character_id: str, text: str) -> Optional[str]:
    """Generates Malayalam audio for all characters reliably via gTTS."""
    if not text or not text.strip():
        return None

    try:
        text_hash = hashlib.md5(f"{character_id}:{text}".encode("utf-8")).hexdigest()[:12]
        filename = f"{character_id}_{text_hash}.mp3"
        filepath = os.path.join(AUDIO_DIR, filename)

        # Serve from disk if already generated
        if os.path.exists(filepath) and os.path.getsize(filepath) > 500:
            return f"/audio/{filename}"

        # Upadeshi speaks slightly slower; Chechi and Reddit Maman speak at standard pace
        slow_pace = True if character_id == "upadeshi" else False
        tts = gTTS(text=text, lang="ml", slow=slow_pace)
        tts.save(filepath)

        if os.path.exists(filepath) and os.path.getsize(filepath) > 500:
            return f"/audio/{filename}"
        return None

    except Exception as exc:
        print(f"[TTSService] Audio generation error for '{character_id}': {exc}")
        return None