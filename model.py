from transformers import pipeline

classifier = pipeline(
    "text-classification",
    model="j-hartmann/emotion-english-distilroberta-base",
    top_k=None,
    device=-1
)

EMOTION_EMOJI = {
    "anger": "😡", "disgust": "🤢", "fear": "😨",
    "joy": "😄", "neutral": "😐", "sadness": "😢", "surprise": "😲",
}

# Emotions considered aggressive
AGGRESSIVE_EMOTIONS = {"anger", "disgust"}
AGGRESSION_THRESHOLD = 0.40  # if combined anger+disgust score > this → aggressive

def analyze_comment(comment: str) -> dict:
    results = classifier(comment)[0]
    if isinstance(results, dict):
        results = [results]
    results = sorted(results, key=lambda x: x["score"], reverse=True)

    top = results[0]
    scores = {r["label"]: round(r["score"] * 100, 2) for r in results}

    aggression_score = sum(
        r["score"] for r in results if r["label"] in AGGRESSIVE_EMOTIONS
    )
    is_aggressive = aggression_score >= AGGRESSION_THRESHOLD

    return {
        "emotion": top["label"],
        "emotion_emoji": EMOTION_EMOJI.get(top["label"], ""),
        "emotion_score": round(top["score"] * 100, 2),
        "aggression": "yes" if is_aggressive else "no",
        "aggression_score": round(aggression_score * 100, 2),
        "all_scores": scores
    }

def analyze_batch(posts: list) -> dict:
    results = []
    for post in posts:
        analysis = analyze_comment(post["comment"])
        results.append({
            "id": post["id"],
            "comment": post["comment"],
            **analysis
        })

    # Summary stats
    emotion_counts = {}
    aggressive_count = 0
    for r in results:
        emotion_counts[r["emotion"]] = emotion_counts.get(r["emotion"], 0) + 1
        if r["aggression"] == "yes":
            aggressive_count += 1

    return {
        "results": results,
        "summary": {
            "total": len(results),
            "aggressive_count": aggressive_count,
            "non_aggressive_count": len(results) - aggressive_count,
            "emotion_distribution": emotion_counts
        }
    }