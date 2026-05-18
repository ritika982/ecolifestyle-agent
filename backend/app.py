from flask import Flask, request, jsonify
from flask_cors import CORS
from agent.eco_agent import EcoAgent
import os
from dotenv import load_dotenv

load_dotenv()
app = Flask(__name__)
CORS(app)
agent = EcoAgent()

@app.route("/chat", methods=["POST"])
def chat():
    data = request.json
    user_message = data.get("message", "").strip()
    location = data.get("location", "India")
    if not user_message:
        return jsonify({"error": "No message"}), 400
    response = agent.run(user_message, location=location)
    return jsonify({"response": response})

@app.route("/eco-tips", methods=["GET"])
def eco_tips():
    return jsonify({"tips": agent.get_daily_tips()})

@app.route("/health", methods=["GET"])
def health():
    return jsonify({"status": "ok"})

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port, debug=False)