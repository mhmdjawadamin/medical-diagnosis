from flask import Flask, request, jsonify
from main import analyze_text

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

        result = analyze_text(user_text)

        return jsonify(result)

    except Exception as e:
        return jsonify({"error": str(e)}), 500


if __name__ == "__main__":
    app.run(debug=True)