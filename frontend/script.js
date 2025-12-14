const chatBox = document.getElementById("chatBox");

function addMessage(text, className) {
  const div = document.createElement("div");
  div.className = `message ${className}`;
  div.innerText = text;
  chatBox.appendChild(div);
  chatBox.scrollTop = chatBox.scrollHeight;
}

async function buildKB() {
  const url = document.getElementById("urlInput").value;

  addMessage("Building knowledge base...", "bot");

  await fetch("http://127.0.0.1:5000/build_kb", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ url })
  });

  addMessage("Knowledge base ready!", "bot");
}

async function ask() {
  const question = document.getElementById("questionInput").value;
  addMessage("You: " + question, "user");

  const res = await fetch("http://127.0.0.1:5000/ask", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ question })
  });

  const data = await res.json();
  addMessage("Bot: " + data.answer, "bot");
}
