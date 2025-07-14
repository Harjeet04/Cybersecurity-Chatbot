from flask import Flask, render_template, request, jsonify
import cohere
import os
from dotenv import load_dotenv

load_dotenv()
co = cohere.Client(os.getenv("AJIQ3FvKZgGoJELjpZGyimqaYULBAXKe9gRkJwsg"))

app = Flask(__name__)

# Cybersecurity keyword filter
CYBER_KEYWORDS = [
    # Authentication & Access Control
    "password", "strong password", "password policy", "2fa", "two-factor authentication",
    "multi-factor authentication", "mfa", "otp", "one-time password", "biometrics",
    "access control", "identity theft", "login credentials", "authentication token",

    # Phishing & Social Engineering
    "phishing", "spear phishing", "vishing", "smishing", "social engineering",
    "email spoofing", "impersonation", "baiting", "malicious email", "fake website",
    "fake login", "credential harvesting", "spoofed link", "malicious link",

    # Malware & Threats
    "malware", "ransomware", "spyware", "trojan horse", "trojan", "computer virus",
    "worm", "adware", "botnet", "keylogger", "rootkit", "backdoor", "logic bomb",

    # Network Security
    "firewall", "vpn", "virtual private network", "ids", "ips", "intrusion detection system",
    "proxy", "ip address", "mac address", "packet sniffing", "port scanning", "dns spoofing",

    # Cyber Attacks
    "ddos", "distributed denial of service", "brute force", "brute force attack",
    "sql injection", "xss", "cross site scripting", "csrf", "session hijacking",
    "zero-day exploit", "zero day", "privilege escalation", "data breach",
    "man in the middle", "mitm", "spoofing attack", "dns poisoning",

    # Encryption & Privacy
    "encryption", "decryption", "symmetric encryption", "asymmetric encryption",
    "public key", "private key", "rsa", "aes", "hashing", "md5", "sha256", "digital signature",
    "pgp", "ssl", "tls", "https", "end-to-end encryption",

    # Cyber Hygiene
    "antivirus", "firewall", "backup", "software update", "security patch", "patch management",
    "safe browsing", "secure wifi", "secure connection", "password manager",

    # Compliance & Governance
    "gdpr", "hipaa", "iso 27001", "pci dss", "compliance", "cybersecurity policy",
    "data protection", "risk assessment", "audit", "security awareness",

    # Roles, Tools & Practices
    "cybersecurity", "ethical hacking", "penetration testing", "pentest",
    "cybersecurity analyst", "incident response", "forensic analysis", "siem",
    "ciso", "security operations center", "red team", "blue team", "cyber threat",
    "security breach", "threat hunting", "vulnerability", "exploit"
]

def is_cyber_question(user_input):
    return any(word.lower() in user_input.lower() for word in CYBER_KEYWORDS)

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/chat", methods=["POST"])
def chat():
    data = request.get_json()
    user_input = data.get("message")

    if not user_input or not user_input.strip():
        return jsonify({"reply": "❗ Please type a message."})

    if not is_cyber_question(user_input):
        return jsonify({"reply": "⚠️ Please ask cybersecurity-related questions only."})

    try:
        prompt = (
            "You are a helpful cybersecurity tutor. "
            "Explain clearly and simply. Here's a user's question:\n\n"
            f"Q: {user_input}\nA:"
        )

        response = co.generate(
            model='command-light',  # use 'command' or 'command-light'
            prompt=prompt,
            max_tokens=300,
            temperature=0.7
        )

        answer = response.generations[0].text.strip()
        return jsonify({"reply": answer})

    except Exception as e:
        print("Cohere API Error:", str(e))
        return jsonify({"reply": "⚠️ Error contacting AI service."})

if __name__ == "__main__":
    app.run(debug=True)
