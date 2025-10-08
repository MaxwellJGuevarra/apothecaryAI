import os
from pathlib import Path
from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    model_path: Path = Path(os.getenv("MODEL_PATH", "apothecary/models/prompt_classifier.joblib"))
    log_level: str = os.getenv("LOG_LEVEL", "info")

settings = Settings()