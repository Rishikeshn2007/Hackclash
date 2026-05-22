from flask import Flask, request, jsonify, render_template
from model import analyze_batch

app = Flask(__name__)

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/analyze", methods=["POST"])
def analyze():
    data = request.get_json()

    if not data or "posts" not in data:
        return jsonify({"error": "Send JSON with a 'posts' array"}), 400

    posts = data["posts"]

    if not isinstance(posts, list) or len(posts) == 0:
        return jsonify({"error": "'posts' must be a non-empty array"}), 400

    for i, post in enumerate(posts):
        if "id" not in post or "comment" not in post:
            return jsonify({"error": f"Post at index {i} missing 'id' or 'comment'"}), 400

    try:
        result = analyze_batch(posts)
        return jsonify(result)
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    app.run(debug=True)