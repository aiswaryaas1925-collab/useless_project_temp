import random

CHAOS_TRIGGERS = [
    "crypto", "reels", "rocket", "drop database", "റീൽസ്", "മാന്തിയെഴുതുക",
    "അലുമിനിയം", "കടിച്ചു", "ഓസ്മോസിസ്", "force", "absolute", "റോക്കറ്റ്",
    "ആധാരം", "ബ്ലോക്ക്", "ചിരിച്ച്", "നാരങ്ങാവെള്ളം"
]

CHARACTER_BASELINES = {
    "upadeshi": 78,
    "chechi": 84,
    "reddit_maman": 92
}


def calculate_badness_score(character_id: str, advice_text: str) -> int:
    """
    Calculates a score between 0 and 100 representing how terrible/absurd the advice is.
    Baseline starts at character's default, augmented by chaos trigger keywords.
    """
    baseline = CHARACTER_BASELINES.get(character_id, 80)
    score = baseline
    
    # Check for presence of chaotic/absurd keywords
    lower_text = advice_text.lower()
    matched_triggers = sum(1 for word in CHAOS_TRIGGERS if word in lower_text)
    
    score += matched_triggers * 3
    # Add a small random jitter (+/- 3) so repeated calls feel alive
    score += random.randint(-3, 3)
    
    # Clamp strictly within [70, 100] for comedic bad advice
    return max(70, min(100, score))