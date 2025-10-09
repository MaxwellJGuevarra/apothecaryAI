from pydantic import BaseModel
from typing import List

class Prompt(BaseModel):
    text: str

class ScanOut(BaseModel):
    prompt: str
    score: float        # 0-1 adversarial probability
    flagged: bool
    reason: str

class AuditOut(BaseModel):
    total_rows: int
    poison_rows: int
    poison_percent: float
    sample_triggers: List[str]
    sample_explanations: List[str]
