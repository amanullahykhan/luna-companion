# models/emotion.py — runs offline, no external calls
from transformers import pipeline
import torch

# Tiny model (24M params), MIT licensed
emotion_classifier = pipeline(
    "text-classification",
    model="SamLowe/roberta-base-go_emotions",
    return_all_scores=False,
    device=0 if torch.cuda.is_available() else -1,
    truncation=True
)

EMOTION_MAP = {
    "admiration": "joy",
    "amusement": "joy",
    "approval": "joy",
    "gratitude": "joy",
    "love": "joy",
    "optimism": "joy",
    "caring": "joy",
    "pride": "joy",
    "relief": "joy",
    "desire": "anticipation",
    "curiosity": "anticipation",
    "realization": "surprise",
    "surprise": "surprise",
    "confusion": "uncertainty",
    "fear": "anxiety",
    "nervousness": "anxiety",
    "remorse": "guilt",
    "embarrassment": "shame",
    "disappointment": "sadness",
    "sadness": "sadness",
    "grief": "sadness",
    "annoyance": "anger",
    "anger": "anger",
    "disgust": "disgust",
    "disapproval": "disgust"
}

def analyze_emotion(text: str):
    try:
        result = emotion_classifier(text[:512])[0]  # truncate
        label = result["label"]
        score = result["score"]
        
        # Map to core emotion + sentiment
        core_emotion = EMOTION_MAP.get(label, "neutral")
        sentiment = score if core_emotion in ["joy", "anticipation"] else -score
        
        return core_emotion, round(sentiment, 3)
    except:
        return "neutral", 0.0