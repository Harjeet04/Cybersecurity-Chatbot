from flask import Flask, render_template, request, jsonify, session
import cohere
import os
from dotenv import load_dotenv

load_dotenv()
api_key = os.getenv("COHERE_API_KEY")

if not api_key:
    raise ValueError("No COHERE_API_KEY found in environment variables")

co = cohere.Client(api_key)

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
    "2. **Always format your answer in clean, readable Markdown**:\n"
    "   - Use bullet points for lists (`- item`)\n"
    "   - Use headings or bold for key terms (`**term:** explanation`)\n"
    "   - Each new heading will start from a new line and have a colon after the key term "
    "   - Use line breaks between ideas for better readability\n"
    "3. Keep answers short and easy to read (avoid big walls of text).\n"
    "4. Encourage curiosity but avoid dangerous step-by-step hacking instructions.\n"
    "5. When asked about learning resources, suggest:\n"
    "   - Cybrary, SANS Institute, Coursera (Cybersecurity courses), OWASP\n"
    "   - Hands-on practice: TryHackMe, Hack The Box, OverTheWire, PortSwigger Web Security Academy\n"
    "   - Community spaces: Reddit r/netsec, OWASP Slack, Infosec Discords\n"
    "   -Youtube channels: The Cyber Mentor, John Hammond, HackerSploit, NetworkChuck, David Bombal"
    "6. Be motivational — encourage learning, practice, and responsible security research."
)


        # Get existing chat history from session
        chat_history = session.get("chat_history", [])
        
        # Add user message to history
        chat_history.append({"role": "USER", "message": user_input})
        
        # Generate response using Cohere API
        response = co.chat(
            model="command-r-plus",
            preamble=system_prompt,
            message=user_input,
            chat_history=chat_history[:-1]  # All but the current message
        )

        answer = response.text.strip()
        
        # Add assistant response to history
        chat_history.append({"role": "CHATBOT", "message": answer})
        
        # Update session with new chat history (truncate if too long)
        if len(chat_history) > 20:  # Keep last 10 exchanges
            chat_history = chat_history[-20:]
        session["chat_history"] = chat_history
        
        return jsonify({"reply": answer})

    except cohere.CohereAPIError as e:
        print("Cohere API Error:", str(e))
        return jsonify({"reply": "⚠️ Error with the AI service. Please try again later."})
    except Exception as e:
        print("Unexpected Error:", str(e))
        return jsonify({"reply": "⚠️ An unexpected error occurred. Please try again."})

@app.route("/clear", methods=["POST"])
def clear_chat():
    """Clear the chat history"""
    session["chat_history"] = []
    return jsonify({"status": "success"})

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port, debug=True)
