from flask import Flask, request, jsonify, render_template
from model import predict_emotions

app = Flask(__name__)

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/analyze", methods=["POST"])
def analyze():
    data = request.get_json()
    text = data.get("text", "").strip()

    if not text:
        return jsonify({"error": "No text provided"}), 400

    if len(text) > 512:
        return jsonify({"error": "Text too long (max 512 characters)"}), 400

    try:
        result = predict_emotions(text)
        return jsonify(result)
    except Exception as e:
        return jsonify({"error": str(e)}), 500  # ← add this

if __name__ == "__main__":
    app.run(debug=True)