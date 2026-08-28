import re

POSITIVE_WORDS = {"love", "great", "excellent", "forward", "good", "amazing", "record", "step", "positive", "collaborative"}
NEGATIVE_WORDS = {"unacceptable", "terrible", "outage", "drops", "angry", "bad", "escalating", "poor", "hate", "issue"}
EMOTION_KEYWORDS = {
    "anger": ["angry", "unacceptable", "terrible", "outage", "frustrated", "rage"],
    "joy": ["loving", "great", "excellent", "happy", "record", "amazing"],
    "fear": ["risk", "danger", "scared", "warning", "threat", "escalating"],
    "surprise": ["whoa", "unbelievable", "unexpected", "drops", "sudden"],
    "sarcasm": ["yeah right", "surely works", "obviously perfect", "great job breaking it"]
}

def analyze_sentiment_and_emotion(text: str) -> dict:
    clean_text = text.lower()
    words = set(re.findall(r"\b\w+\b", clean_text))
    
    pos_score = len(words.intersection(POSITIVE_WORDS))
    neg_score = len(words.intersection(NEGATIVE_WORDS))
    
    if pos_score > neg_score:
        sentiment = "positive"
        confidence = min(0.65 + (pos_score * 0.1), 0.98)
    elif neg_score > pos_score:
        sentiment = "negative"
        confidence = min(0.65 + (neg_score * 0.1), 0.98)
    else:
        sentiment = "neutral"
        confidence = 0.60
        
    detected_emotion = "neutral"
    for emotion, terms in EMOTION_KEYWORDS.items():
        if any(term in clean_text for term in terms):
            detected_emotion = emotion
            break
            
    return {
        "sentiment": sentiment,
        "emotion": detected_emotion,
        "confidence": round(confidence, 2),
        "model_version": "hybrid-v1.0"
    }