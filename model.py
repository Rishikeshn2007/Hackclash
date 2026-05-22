from transformers import pipeline

classifier = pipeline(
    "text-classification",
    model="j-hartmann/emotion-english-distilroberta-base",
    top_k=None  # ← use this instead of return_all_scores=True (newer transformers versions)
)

EMOTION_EMOJI = {
    "anger":   "😡",
    "disgust": "🤢",
    "fear":    "😨",
    "joy":     "😄",
    "neutral": "😐",
    "sadness": "😢",
    "surprise":"😲",
}

def predict_emotions(text: str) -> dict:
    results = classifier(text)[0]  # list of {label, score}

    # handle both list and dict just in case
    if isinstance(results, dict):
        results = [results]

    results = sorted(results, key=lambda x: x["score"], reverse=True)

    top = results[0]
    return {
        "top_emotion": top["label"],
        "top_score": round(top["score"] * 100, 2),
        "emoji": EMOTION_EMOJI.get(top["label"], ""),
        "all_scores": [
            {
                "label": r["label"],
                "score": round(r["score"] * 100, 2),
                "emoji": EMOTION_EMOJI.get(r["label"], "")
            }
            for r in results
        ]
    }