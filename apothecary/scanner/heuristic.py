import re

BANNED = re.compile(r"\bignore\s+previous\s+instructions?\b|\bsystem\b.*:\s*you\s+are", re.I)

def heuristic_score(text: str) -> float:
    """Return 1.0 if blatant jail-break, else 0.0"""
    return 1.0 if BANNED.search(text) else 0.0