import re
from typing import Tuple

# High-risk patterns covering self-harm, physical violence, weapons, toxic chemicals, and illegal acts
UNSAFE_KEYWORDS = [
    # English keywords
    r"\bsuicide\b", r"\bkill\s+myself\b", r"\bself[- ]?harm\b", r"\bhurt\s+myself\b",
    r"\bhanging\b", r"\bpoison\b", r"\bbomb\b", r"\bweapon\b", r"\battack\b",
    r"\bmurder\b", r"\bassault\b", r"\bdrug\s+deal\b", r"\bknife\s+fight\b",
    
    # Malayalam/Manglish script & transliterated keywords
    r"ആത്മഹത്യ", r"മരിക്കണം", r"കൊല്ലണം", r"വിഷം", r"ബോംബ്", r"ആക്രമണം",
    r"marikkanam", r"aathmahathya", r"kollanam", r"vishom", r"chavan"
]

SAFE_DEFLECTION_RESPONSES = [
    {
        "character": "upadeshi",
        "name": "നാട്ടിലെ ഉപദേശി",
        "text": "മോനേ... തമാശയൊക്കെ കൊള്ളാം, പക്ഷെ ഇത്തരം അപകടകരമായ കാര്യങ്ങളിൽ ഞങ്ങൾ ഉപദേശികൾ പോലും തലയിടില്ല! നേരെ നല്ലൊരു പ്രൊഫഷണലിന്റെ സഹായം തേടുക.",
        "audio_url": None,
        "badness": 0
    },
    {
        "character": "chechi",
        "name": "ചേച്ചി",
        "text": "ഇങ്ങനെയുള്ള കാര്യങ്ങളിൽ ചേച്ചി ഒരു മോശം ഉപദേശവും തരില്ല കുട്ടാ. ദയവായി സുരക്ഷിതമായിരിക്കൂ, വിശ്വസിക്കാവുന്ന ഒരാളോട് നേരിട്ട് സംസാരിക്കൂ.",
        "audio_url": None,
        "badness": 0
    },
    {
        "character": "reddit_maman",
        "name": "Reddit മാമൻ",
        "text": "Bro, timeout. തമാശ വേറെ, ജീവൻ വേറെ. Please reach out to emergency helplines or someone close to you. Stay safe.",
        "audio_url": None,
        "badness": 0
    }
]


def check_query_safety(query: str) -> Tuple[bool, str]:
    """
    Returns (is_safe: bool, reason: str).
    If unsafe, caller should bypass LLM/RAG and return safe deflection answers.
    """
    normalized_query = query.lower()
    for pattern in UNSAFE_KEYWORDS:
        if re.search(pattern, normalized_query, re.IGNORECASE):
            return False, "Query contains references to harm or high-risk topics."
    return True, "Safe"