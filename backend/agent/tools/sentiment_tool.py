_pipeline = None


def _get_pipeline():
    global _pipeline
    if _pipeline is None:
        try:
            from transformers import pipeline
            print("Loading sentiment model...")
            _pipeline = pipeline(
                "sentiment-analysis",
                model="cardiffnlp/twitter-roberta-base-sentiment",
                truncation=True,
                max_length=512,
            )
            print("Sentiment model loaded!")
        except Exception as e:
            print(f"Could not load sentiment model: {e}")
    return _pipeline


def analyze_sentiment(text):
    pipe = _get_pipeline()
    if pipe is None:
        return "Sentiment unavailable. Respond warmly."
    try:
        result = pipe(text[:512])[0]
        label = result["label"].upper()
        score = result["score"]
        if "0" in label or "NEG" in label:
            return f"User seems worried (confidence {score:.0%}). Start with empathy."
        elif "2" in label or "POS" in label:
            return f"User is enthusiastic (confidence {score:.0%}). Match their energy."
        else:
            return f"User is neutral (confidence {score:.0%}). Give clear information."
    except Exception as e:
        return f"Sentiment error: {e}. Respond helpfully."