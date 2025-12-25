from flask import Flask, render_template, request, jsonify
from openai import OpenAI
import os

app = Flask(__name__, template_folder="../templates")

client = OpenAI(
    base_url="https://openrouter.ai/api/v1",
    api_key=os.environ.get("OPENROUTER_API_KEY", "")
)

chat_history = [
    {"role": "system", "content": "You are Alis, a friendly and helpful AI chatbot."}
]

@app.get("/")
def index():
    return render_template("index.html")

@app.post("/chat")
def chat():
    data = request.get_json() or {}
    user_message = data.get("message", "")
    chat_history.append({"role": "user", "content": user_message})

    try:
        response = client.chat.completions.create(
            model="mistralai/devstral-2512:free",
            messages=chat_history,
            extra_headers={
                "HTTP-Referer": "https://your-vercel-domain.vercel.app",
                "X-Title": "Alis Web Chatbot",
            }
        )
        reply = response.choices[0].message.content
        chat_history.append({"role": "assistant", "content": reply})
        return jsonify({"reply": reply})
    except Exception:
        return jsonify({"reply": "⚠️ Alis is currently unavailable."})
