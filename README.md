# 🔐 Cybersecurity Chatbot

This is a simple web-based chatbot that helps users learn about cybersecurity topics in an interactive way. It’s built using Flask (Python), the Cohere AI API, and basic HTML/CSS/JS.
The chatbot can explain terms like “firewall”, “phishing”, “brute force attack”, and more — all in plain language.

---
🎯 What It Does

- ✅ Answers cybersecurity-related questions in simple words
- 🧠 Uses Cohere AI to generate real-time answers
- 🚫 Only responds to cybersecurity questions (filtered)

---
💻 Tech Used

- Frontend: HTML, CSS, JavaScript
- Backend: Python + Flask
- AI Model: Cohere's Command-Light
- Hosting: Render

---
📂 Folder Structure
cybersecurity-chatbot/
├── chatapp.py # Flask backend
├── templates/
│ └── index.html # Chat UI
├── static/
│ ├── style.css # Styling
│ └── script.js # Chat logic
├── .env # API key (not shared)
├── requirements.txt # Python packages
├── render.yaml # Render config (for deployment)
└── README.md


---
🧪 How It Works
1. You type a question (like "What is a DDoS attack?")
2. The frontend sends the question to the Flask server
3. Flask sends it to Cohere's API for an AI-generated answer
4. The answer is returned and shown in the chat window

---
🐍 Install dependencies:

pip install -r requirements.txt

To run:
python chatapp.py
