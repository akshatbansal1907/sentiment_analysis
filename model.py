import os
import torch
from transformers import pipeline

# Keep CPU thread usage low on small cloud instances.
torch.set_num_threads(1)
torch.set_num_interop_threads(1)

MODEL_NAME = os.getenv(
    "SENTIMENT_MODEL",
    "sshleifer/tiny-distilbert-base-uncased-finetuned-sst-2-english",
)

_classifier = None


def get_classifier():
    """Load the classifier once, only when the first prediction is requested."""
    global _classifier

    if _classifier is None:
        _classifier = pipeline(
            "sentiment-analysis",
            model=MODEL_NAME,
            device=-1,
        )

    return _classifier


def predict_sentiment(text: str):
    text = (text or "").strip()

    if not text:
        return {
            "label": "NEUTRAL",
            "confidence": 0.0,
        }

    result = get_classifier()(text, truncation=True, max_length=256)[0]

    return {
        "label": result["label"],
        "confidence": float(result["score"]),
    }
