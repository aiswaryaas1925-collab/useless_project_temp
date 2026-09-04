import os
import hashlib
from gtts import gTTS

AUDIO_DIR = os.path.join(
    os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
    "audio"
)
os.makedirs(AUDIO_DIR, exist_ok=True)


def text_to_speech_malayalam(text: str) -> str:
    """
    Converts Malayalam/Manglish text to an MP3 file using gTTS.
    Returns the relative URL path for frontend playback (e.g., /audio/hash.mp3).
    """
    if not text or not text.strip():
        return None

    try:
        # Create a unique filename based on the text hash to cache audio
        file_hash = hashlib.md5(text.encode("utf-8")).hexdigest()[:12]
        filename = f"tts_{file_hash}.mp3"
        filepath = os.path.join(AUDIO_DIR, filename)

        # Generate audio file only if it doesn't already exist
        if not os.path.exists(filepath):
            # 'ml' for Malayalam; gTTS will handle Malayalam script cleanly
            tts = gTTS(text=text, lang="ml", slow=False)
            tts.save(filepath)

        return f"/audio/{filename}"

    except Exception as e:
        print(f"[TTS Error] Malayalam audio generation failed: {e}")
        return None