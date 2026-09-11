"""Flask entry point for SentimentScope."""

from flask import Flask, jsonify, request, send_from_directory

from backend.config import MAX_REQUEST_BYTES, MAX_TEXT_LENGTH
from backend.sentiment import analyze_text

app = Flask(__name__, static_folder="frontend")
app.config["MAX_CONTENT_LENGTH"] = MAX_REQUEST_BYTES


@app.get("/")
def index():
    return send_from_directory(app.static_folder, "index.html")


@app.post("/api/analyze")
def analyze():
    data = request.get_json(silent=True)
    if not isinstance(data, dict):
        return jsonify(error="Request body must be valid JSON."), 400
    if "text" not in data:
        return jsonify(error="Text is required."), 400
    text = data["text"]
    if not isinstance(text, str):
        return jsonify(error="Text must be a string."), 400
    if not text.strip():
        return jsonify(error="Text cannot be empty."), 400
    if len(text) > MAX_TEXT_LENGTH:
        return jsonify(error="Text exceeds the 10,000 character limit."), 400
    return jsonify(analyze_text(text))


@app.errorhandler(413)
def request_too_large(_error):
    return jsonify(error="Request is too large."), 413


if __name__ == "__main__":
    app.run(debug=True)
