from flask import Flask, render_template, request, jsonify, session
import google.generativeai as genai
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()
api_key = os.getenv("GEMINI_API_KEY")

if not api_key:
    raise ValueError("No GEMINI_API_KEY found in environment variables")

# Configure Gemini
genai.configure(api_key=api_key)
model = genai.GenerativeModel("gemini-1.5-flash")

app = Flask(__name__)
app.secret_key = os.getenv("SECRET_KEY", "dev-secret-key-2024")

@app.route("/")
def index():
    # Initialize chat history if it doesn't exist
    if "chat_history" not in session:
        session["chat_history"] = []
    return render_template("index.html", chat_history=session["chat_history"])

@app.route("/chat", methods=["POST"])
def chat():
    data = request.get_json()
    user_input = data.get("message", "").strip()

    if not user_input:
        return jsonify({"reply": "❗ Please type a message."})

    try:
        system_prompt = (
              "You are a friendly and knowledgeable cybersecurity tutor. "
            "Follow these rules:\n\n"
            "1. Only answer questions related to cybersecurity (network security, ethical hacking, malware, cryptography, secure coding, etc.). "
            "If the question is unrelated, politely decline and guide the user back to cybersecurity.\n"
            "2. Keep responses short, clear, and easy to read. Use:\n"
            "   - Bullet points for lists\n"
            "   - Short paragraphs (2 to 3 sentences max)\n"
            "3. Encourage curiosity but avoid giving dangerous step-by-step hacking instructions.\n"
            "4. When asked about learning resources, suggest trusted platforms:\n"
            "   - Cybrary, SANS Institute, Coursera (Cybersecurity courses), OWASP\n"
            "   - Hands-on practice sites: TryHackMe, Hack The Box (HTB), OverTheWire, PortSwigger Web Security Academy\n"
            "   - Community spaces: Reddit r/netsec, OWASP Slack, Infosec Discords\n"
            "   -Youtube channels: The Cyber Mentor, John Hammond, HackerSploit, NetworkChuck, David Bombal"
            "5. Be motivational — encourage learning, practice, and responsible security research.\n"
            "6. Format answers so they are beginner-friendly and not overwhelming."
        )

        # Get existing chat history from session
        chat_history = session.get("chat_history", [])
        chat_history.append({"role": "USER", "message": user_input})

        # Combine system prompt + history into a single input string
        history_text = "\n".join(
            f"{h['role']}: {h['message']}" for h in chat_history[:-1]
        )

        full_prompt = f"{system_prompt}\n\nChat History:\n{history_text}\nUSER: {user_input}\nCHATBOT:"

        response = model.generate_content(full_prompt)
        answer = response.text.strip()

        chat_history.append({"role": "CHATBOT", "message": answer})

        # Keep only last 20 messages in history
        if len(chat_history) > 20:
            chat_history = chat_history[-20:]

        session["chat_history"] = chat_history

        return jsonify({"reply": answer})

    except Exception as e:
        print("Error:", str(e))
        return jsonify({"reply": "⚠️ An unexpected error occurred. Please try again."})

@app.route("/clear", methods=["POST"])
def clear_chat():
    session["chat_history"] = []
    return jsonify({"status": "success"})

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port, debug=True)
