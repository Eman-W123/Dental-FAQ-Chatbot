"""Bright Smile Dental — FAQ chatbot backend.

A small Flask server that answers dental-clinic FAQs using Google's Gemini
API (free tier). The clinic knowledge base is sent to the model as a system
instruction on every request, and a short per-session conversation history is
kept in memory so the bot remembers earlier messages in the same conversation.
"""

import logging
import os
import uuid

from dotenv import load_dotenv
from flask import Flask, jsonify, request, send_from_directory, session
from google import genai
from google.genai import types
from google.genai.errors import APIError

from knowledge_base import SYSTEM_PROMPT

load_dotenv()

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Model can be overridden via .env. Defaults to Google's "latest flash" alias
# rather than a pinned version, so this keeps working as Gemini's lineup
# rotates instead of 404ing when a specific dated model gets retired.
MODEL = os.getenv("GEMINI_MODEL", "gemini-flash-latest")

# How many of the most recent messages to keep per conversation. Trimming keeps
# token usage predictable for a long chat without losing recent context.
MAX_HISTORY_MESSAGES = 20

# Shown to the user when the API call fails for any reason — never a raw crash.
FALLBACK_REPLY = (
    "Sorry, I'm having a little trouble answering right now. "
    "Please try again in a moment, or call our team at (951) 555-0143 "
    "and we'll be glad to help."
)

app = Flask(__name__, static_folder=None)
# Secret key is only used to sign the session cookie that identifies a browser.
app.secret_key = os.getenv("FLASK_SECRET_KEY", "dev-secret-change-me")

# In-memory conversation store: {session_id: [ {role, parts}, ... ] }, using
# Gemini's own "user" / "model" role names so history can be sent as-is.
conversations: dict[str, list[dict]] = {}

# One client for the process. Reads GEMINI_API_KEY from the environment.
_api_key = os.getenv("GEMINI_API_KEY")
client = genai.Client(api_key=_api_key) if _api_key else None


@app.get("/")
def index():
    """Serve the single-file chat widget."""
    return send_from_directory(app.root_path, "index.html")


@app.post("/chat")
def chat():
    payload = request.get_json(silent=True) or {}
    message = str(payload.get("message", "")).strip()

    if not message:
        return jsonify({"error": "Please enter a message."}), 400

    # Identify the browser session and load its history.
    if "sid" not in session:
        session["sid"] = uuid.uuid4().hex
    sid = session["sid"]
    history = conversations.setdefault(sid, [])

    history.append({"role": "user", "parts": [{"text": message}]})

    if client is None:
        logger.error("GEMINI_API_KEY is not set; returning fallback reply.")
        history.pop()  # don't keep a turn we never answered
        return jsonify({"reply": FALLBACK_REPLY})

    try:
        response = client.models.generate_content(
            model=MODEL,
            contents=history[-MAX_HISTORY_MESSAGES:],
            config=types.GenerateContentConfig(
                system_instruction=SYSTEM_PROMPT,
                max_output_tokens=1024,
            ),
        )
        reply = (response.text or "").strip()

        if not reply:
            raise ValueError("Empty response from model")

        history.append({"role": "model", "parts": [{"text": reply}]})
        # Trim so the stored history doesn't grow without bound.
        conversations[sid] = history[-MAX_HISTORY_MESSAGES:]
        return jsonify({"reply": reply})

    except (APIError, ValueError) as exc:
        logger.exception("Gemini request failed: %s", exc)
        history.pop()  # roll back the unanswered user turn
        return jsonify({"reply": FALLBACK_REPLY})


if __name__ == "__main__":
    app.run(host="127.0.0.1", port=5000, debug=True)
