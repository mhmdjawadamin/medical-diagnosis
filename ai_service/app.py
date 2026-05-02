from flask import Flask, request, jsonify
from main import analyze_text
from chatbot import get_chatbot_response

app = Flask(__name__)


@app.route("/", methods=["GET"])
def home():
    return "Medical AI API is running"


@app.route("/analyze", methods=["POST"])
def analyze():
    try:
        data = request.get_json()

        if not data:
            return jsonify({"error": "No JSON data received"}), 400

        if "text" not in data:
            return jsonify({"error": "Missing 'text' field"}), 400

        user_text = data["text"]

        # NEW: receive patient health profile from PHP
        health_profile = data.get("health_profile")

        # NEW: send text + health profile to main AI pipeline
        result = analyze_text(user_text, health_profile)

        return jsonify(result)

    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route("/chatbot", methods=["POST"])
def chatbot():
    try:
        data = request.get_json()

        if not data or "message" not in data:
            return jsonify({
                "error": "Missing 'message' field"
            }), 400

        message = data["message"]
        latest_result = data.get("latest_result")

        reply = get_chatbot_response(message, latest_result)

        return jsonify({
            "reply": reply
        })

    except Exception as e:
        return jsonify({
            "error": str(e)
        }), 500


if __name__ == "__main__":
    app.run(debug=True)