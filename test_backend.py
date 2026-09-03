import requests
import sys

BASE_URL = "http://localhost:8000"

def test_pipeline():
    print("--- 1. Testing Health Endpoint (GET /) ---")
    try:
        r = requests.get(f"{BASE_URL}/")
        assert r.status_code == 200, f"Expected 200, got {r.status_code}"
        print("✓ Health Check Passed:", r.json())
    except Exception as e:
        print("✗ Health Check Failed:", e)
        sys.exit(1)

    print("\n--- 2. Testing Bad Advice Generation (POST /ask) ---")
    ask_payload = {"query": "എനിക്ക് നാളെ എക്സാം ആണ്, പഠിക്കാൻ മടിയാണ്"}
    try:
        r = requests.post(f"{BASE_URL}/ask", json=ask_payload)
        assert r.status_code == 200, f"Expected 200, got {r.status_code}"
        data = r.json()
        
        responses = data.get("responses", [])
        assert len(responses) == 3, f"Expected 3 personas, got {len(responses)}"
        print(f"✓ Received advice from {len(responses)} characters:")
        
        first_audio_url = None
        upadeshi_advice = ""
        for resp in responses:
            char = resp.get("character")
            score = resp.get("badness")
            audio = resp.get("audio_url")
            text = resp.get("text")
            print(f"   [{char}] (Badness: {score}) Audio: {audio}")
            if char == "upadeshi":
                upadeshi_advice = text
            if audio and not first_audio_url:
                first_audio_url = audio

    except Exception as e:
        print("✗ /ask Endpoint Failed:", e)
        sys.exit(1)

    print("\n--- 3. Testing Cross-Character Argument (POST /argue) ---")
    argue_payload = {
        "attacker": "reddit_maman",
        "defender": "upadeshi",
        "original_topic": "exam study",
        "original_advice": upadeshi_advice or "പഠിക്കാൻ മടിയാണെങ്കിൽ പുസ്തകം തലയിണക്കടിയിൽ വെച്ച് കിടന്നുറങ്ങുക."
    }
    argue_audio_url = None
    try:
        r = requests.post(f"{BASE_URL}/argue", json=argue_payload)
        assert r.status_code == 200, f"Expected 200, got {r.status_code}"
        arg_data = r.json()
        argue_audio_url = arg_data.get("audio_url")
        print("✓ Argument Roast Generated:")
        print(f"   Text: {arg_data.get('argument_text')}")
        print(f"   Audio: {argue_audio_url}")
    except Exception as e:
        print("✗ /argue Endpoint Failed:", e)
        sys.exit(1)

    print("\n--- 4. Testing Audio Static File Serving (GET /audio/...) ---")
    target_audio = argue_audio_url or first_audio_url
    if target_audio:
        try:
            full_audio_url = f"{BASE_URL}{target_audio}"
            r = requests.get(full_audio_url)
            assert r.status_code == 200, f"Expected 200, got {r.status_code}"
            assert len(r.content) > 1000, "Audio payload suspiciously small"
            print(f"✓ Audio File Successfully Retrieved ({len(r.content)} bytes) from {target_audio}")
        except Exception as e:
            print("✗ Audio Retrieval Failed:", e)
            sys.exit(1)
    else:
        print("✗ No audio URL available to test static file serving.")
        sys.exit(1)

    print("\n==========================================")
    print(" ALL TESTS PASSED: Backend is 100% stable!")
    print("==========================================")

if __name__ == "__main__":
    test_pipeline()