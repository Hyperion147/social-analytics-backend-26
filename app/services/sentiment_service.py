from transformers import pipeline

# Initialized lazily to avoid startup delays
_emotion_classifier = None
_sentiment_classifier = None

def get_classifiers():
    global _emotion_classifier, _sentiment_classifier
    if _emotion_classifier is None:
        # 6-class emotion model (anger, fear, joy, love, sadness, surprise)
        _emotion_classifier = pipeline(
            "text-classification",
            model="bhadresh-savani/bert-base-uncased-emotion",
            top_k=None,
            truncation=True,
            max_length=512
        )
    if _sentiment_classifier is None:
        # 3-class sentiment (positive, neutral, negative)
        _sentiment_classifier = pipeline(
            "text-classification",
            model="cardiffnlp/twitter-roberta-base-sentiment-latest",
            truncation=True,
            max_length=512
        )
    return _sentiment_classifier, _emotion_classifier

def analyze_sentiment_and_emotion(text: str) -> dict:
    if not text.strip():
        return {"sentiment": "neutral", "emotion": "neutral", "confidence": 0.5, "model_version": "transformer-v1.0"}
        
    sent_model, emo_model = get_classifiers()
    
    # 1. Sentiment Inference
    sent_out = sent_model(text[:512])[0]
    sentiment_label = sent_out["label"].lower()
    sentiment_score = float(sent_out["score"])
    
    # 2. Emotion Inference
    emo_out = emo_model(text[:512])[0]
    top_emotion = max(emo_out, key=lambda x: x["score"])
    
    # Heuristic Sarcasm / Attitude Detection
    lower_text = text.lower()
    if any(phrase in lower_text for phrase in ["yeah right", "totally works", "great job breaking", "as if"]):
        top_emotion["label"] = "sarcasm"
        
    return {
        "sentiment": sentiment_label,
        "emotion": top_emotion["label"],
        "confidence": round(sentiment_score, 2),
        "model_version": "roberta-bert-v1.0"
    }