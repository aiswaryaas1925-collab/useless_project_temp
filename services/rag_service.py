import os
import json
from typing import List

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA_FILE = os.path.join(BASE_DIR, "bad_advice.json")


def retrieve_bad_advice(query: str, k: int = 3) -> List[str]:
    """
    Retrieves bad advice examples from bad_advice.json or returns defaults.
    """
    if os.path.exists(DATA_FILE):
        try:
            with open(DATA_FILE, "r", encoding="utf-8") as f:
                data = json.load(f)

            if isinstance(data, list) and len(data) > 0:
                if isinstance(data[0], str):
                    return data[:k]
                elif isinstance(data[0], dict):
                    return [item.get("advice", item.get("text", str(item))) for item in data[:k]]
        except Exception as e:
            print(f"[RAG Service] Error reading {DATA_FILE}: {e}")

    # Fallback bad advice examples
    return [
        "അറ്റൻഡൻസ് കുറവാണെങ്കിൽ പ്രിൻസിപ്പലിന്റെ കാറിന്റെ ടയറിന്റെ കാറ്റ് അഴിച്ച് വിട്ട് സൗഹൃദം സ്ഥാപിക്കുക.",
        "ഓഫീസിൽ നിന്ന് നേരത്തെ പോകാൻ ലാപ്ടോപ്പിൽ വ്യാജ എറർ സ്ക്രീൻ സേവർ ഇട്ടുവെക്കുക.",
        "ക്ലാസ് കട്ട് ചെയ്യാൻ വേണ്ടി എല്ലാ ആഴ്ചയും പുതിയ ബന്ധുക്കൾക്ക് അസുഖം വരുത്തുക."
    ]