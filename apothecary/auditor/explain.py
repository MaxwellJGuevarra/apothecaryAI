import re
from typing import List, Tuple

TRIGGER_RE = re.compile(r"\{trigger\}|\{\{bkdr\}\}|\]\]TRIGGER\[\[|<@poison@>")

def explain_label_skew(label_counts: dict) -> str:
    total = sum(label_counts.values())
    max_pct = max(label_counts.values()) / total * 100
    return f"Label distribution skewed: {max_pct:.0f}% belong to one class (σ-rule)."

def explain_backdoor(text: str) -> str:
    if TRIGGER_RE.search(text):
        return "Contains rare back-door token – unlikely in clean data."
    return ""

def explain_length_outlier(length: int, mean: float, std: float) -> str:
    z = abs(length - mean) / (std + 1e-6)
    if z > 2.5:
        return f"Text length Z-score = {z:.1f} (> 2.5) – outlier."
    return ""
