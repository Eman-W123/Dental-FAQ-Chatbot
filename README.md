# Bright Smile Dental — AI FAQ Chatbot

A polished demo of an **AI-powered FAQ chatbot** for a dental clinic, built with
Flask and Google's Gemini API (free tier). It answers real front-desk questions —
services, hours, pricing, insurance, and appointment booking — using only the
clinic's own knowledge base, in a warm, professional tone.

This is a portfolio piece showcasing a clean, embeddable chat widget backed by a
small, well-structured Python backend.

## Demo Screenshots

| Home Screen | Hours / Availability | Services | Team / Booking |
| --- | --- | --- | --- |
| ![Home screen showing the Bright Smile Dental landing page and chat widget](docs/screenshot-1.png) | ![Chatbot answering a question about Sunday hours](docs/screenshot-2.png) | ![Chatbot listing available dental services](docs/screenshot-3.png) | ![Chatbot describing staff and booking information](docs/screenshot-4.png) |

## Features

- **Grounded answers** — Gemini is given the clinic's knowledge base as a
  system instruction and told to answer *only* from it. It never invents prices,
  hours, or policies, and politely redirects anything it can't answer to the
  clinic's phone number.
- **Conversation memory** — a per-session history means the bot remembers
  earlier messages, so follow-up questions ("How much is that?") work naturally.
- **Warm front-desk persona** — a carefully written system prompt keeps the tone
  friendly, concise, and reassuring.
- **Graceful error handling** — if the API call fails, the user gets a polite
  fallback message instead of a crash.
- **Modern chat widget** — a floating bubble in the bottom-right corner that
  expands into a chat window, with smooth open/close animation, an animated
  typing indicator, distinct user/bot bubbles, auto-scroll, and a fully
  responsive, mobile-friendly layout.
- **Zero front-end dependencies** — the entire widget is a single, self-contained
  `index.html` (HTML/CSS/JS, no frameworks).

## Tech Stack

| Layer      | Technology                                             |
| ---------- | ------------------------------------------------------ |
| Backend    | Python, [Flask](https://flask.palletsprojects.com/)    |
| AI         | [Google Gemini](https://ai.google.dev/) (`gemini-flash-latest`, free tier) via the official `google-genai` SDK |
| Config     | `python-dotenv` for environment variables              |
| Front end  | Vanilla HTML / CSS / JavaScript (no frameworks)        |

## Project Structure

```
dental-faq-bot/
├── app.py               # Flask server: serves the widget + /chat endpoint
├── knowledge_base.py    # Clinic knowledge base + the system prompt
├── index.html           # Self-contained chat widget (front end)
├── requirements.txt     # Python dependencies
├── .env.example         # Template for your environment variables
├── .gitignore
└── README.md
```

## Running It Locally

### 1. Prerequisites

- Python 3.9+
- A free Gemini API key ([get one here](https://aistudio.google.com/apikey)) — no credit card required

### 2. Set up the environment

```bash
# From the project folder
python -m venv venv

# Activate it
# macOS / Linux:
source venv/bin/activate
# Windows (PowerShell):
venv\Scripts\Activate.ps1

# Install dependencies
pip install -r requirements.txt
```

### 3. Add your API key

```bash
# Copy the template, then edit .env and paste in your real key
cp .env.example .env
```

Open `.env` and set `GEMINI_API_KEY` to your key.

### 4. Run the server

```bash
python app.py
```

Open **http://127.0.0.1:5000** in your browser, click the chat bubble in the
bottom-right corner, and start asking questions.

## Try Asking

- "What are your hours?"
- "Do you offer teeth whitening, and how much is it?"
- "Which insurance plans do you accept?"
- "How do I book an appointment as a new patient?"
- "I chipped a tooth — can you see me today?"
- "Where are you located and is there parking?"

Try an off-topic or out-of-scope question too (e.g. "Should I get a root canal?"
or "What's the weather?") to see the bot stay in its lane and redirect you to the
clinic.

## Customizing for a Real Clinic

All of the clinic's content lives in **`knowledge_base.py`** — swap in a real
practice's services, hours, pricing, and policies, and the bot adapts with no
other code changes. Adjust the persona or rules in the `SYSTEM_PROMPT` in the
same file.

## Notes

- Conversation history is stored in memory, which is perfect for a demo. For
  production, back it with a shared store (e.g. Redis) so history survives
  restarts and works across multiple workers.
- The knowledge base and clinic details in this demo are fictional.
