// Send message to bot
function sendMessage() {
    const input = document.getElementById("user-input");
    const chatBox = document.getElementById("chat-box");
    const userText = input.value.trim();

    if (!userText) return;

    chatBox.innerHTML += `<div class='user-msg'><b>You:</b> ${userText}</div>`;
    input.value = "";

    fetch("/chat", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ message: userText })
    })
    .then(response => response.json())
    .then(data => {
        chatBox.innerHTML += `<div class='bot-msg'><b>Bot:</b> ${data.reply}</div>`;
        chatBox.scrollTop = chatBox.scrollHeight;
    })
    .catch(() => {
        chatBox.innerHTML += `<div class='bot-msg'><b>Bot:</b> ⚠️ Error contacting AI service.</div>`;
    });
}

// Add greeting and Enter key support
document.addEventListener("DOMContentLoaded", function () {
    const chatBox = document.getElementById("chat-box");
    chatBox.innerHTML += `<div class='bot-msg'><b>Bot:</b> 👋 Hello! I'm your cybersecurity chatbot. Ask me any question related to cybersecurity.</div>`;

    const input = document.getElementById("user-input");
    input.addEventListener("keypress", function (e) {
        if (e.key === "Enter") {
            sendMessage();
        }
    });
});
