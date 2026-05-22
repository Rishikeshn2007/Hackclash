# Comment Lens

A Flask web app for bulk emotion and aggression analysis of comments.

The app accepts comments as JSON, runs them through the Hugging Face model
`j-hartmann/emotion-english-distilroberta-base`, and shows:

- Detected emotion for each comment
- Emotion confidence score
- Aggression score
- Aggressive or safe flag
- Summary counts and charts

Aggression is currently calculated from the combined `anger` and `disgust`
scores. A comment is flagged as aggressive when:

```text
anger + disgust >= 0.40
```

## Project Structure

```text
.
├── app.py
├── model.py
├── README.md
├── test.json
└── templates/
    └── index.html
```

## Requirements

- Python 3.10+
- Flask
- Transformers
- PyTorch

Install the main dependencies:

```bash
pip install flask transformers torch
```

The first run may take some time because the Hugging Face model is downloaded
locally.

## Run the App

```bash
python app.py
```

Then open:

```text
http://127.0.0.1:5000
```

## Input Format

The UI supports either pasted JSON or a `.json` file upload.

Expected format:

```json
[
  {
    "id": "1",
    "comment": "I love this product!"
  },
  {
    "id": "2",
    "comment": "This is terrible, I want a refund."
  }
]
```

The included `test.json` file contains a larger sample dataset.

## API Usage

Endpoint:

```text
POST /analyze
```

Request body:

```json
{
  "posts": [
    {
      "id": "1",
      "comment": "I love this product!"
    },
    {
      "id": "2",
      "comment": "This is garbage."
    }
  ]
}
```

Example response:

```json
{
  "results": [
    {
      "id": "1",
      "comment": "I love this product!",
      "emotion": "joy",
      "emotion_emoji": "😄",
      "emotion_score": 99.12,
      "aggression": "no",
      "aggression_score": 0.23,
      "all_scores": {
        "joy": 99.12,
        "neutral": 0.41
      }
    }
  ],
  "summary": {
    "total": 1,
    "aggressive_count": 0,
    "non_aggressive_count": 1,
    "emotion_distribution": {
      "joy": 1
    }
  }
}
```

## Notes

- The model runs on CPU by default.
- The Flask app runs in debug mode when started directly from `app.py`.
- This is a hackathon prototype, so the aggression rule is simple and should be
  tuned before production use.
