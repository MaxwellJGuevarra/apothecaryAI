import joblib
from pathlib import Path
from sklearn.feature_extraction.text import TfidfVectorizer
from apothecary.config import settings

clf = joblib.load(settings.model_path)   # logistic regression + tfidf pipe

def model_score(text: str) -> float:
    """Return probability of adversarial class"""
    return float(clf.predict_proba([text])[0, 1])