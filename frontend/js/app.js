const API_BASE = "https://ecolifestyle-backend.onrender.com";

let loading = false;
const history = [];

const tips = [
  "Carry a cloth bag everywhere — prevents 700 plastic bags per year.",
  "Switch one bulb to LED today — saves 350 rupees per year.",
  "Fix any dripping tap — wastes 20 litres of water per day.",
  "Buy loose vegetables at sabji mandi — zero packaging, cheaper.",
  "Unplug chargers when not in use — they draw power even idle.",
  "Compost vegetable peels — free fertiliser in 45 days.",
  "Use both sides of paper before recycling.",
  "Walk or cycle for trips under 2 km.",
];
document.getElementById("tip-text").textContent =
  tips[Math.floor(Math.random() * tips.length)];

checkBackend();

async function checkBackend() {
  try {
    const res = await fetch(API_BASE + "/health");
    if (res.ok) {
      document.getElementById("status-dot").classList.add("on");
      document.getElementById("status-lbl").textContent = "AI Ready";
    }
  } catch {
    document.getElementById("status-lbl").textContent = "Start Flask first";
  }
}

function onInput(el) {
  el.style.height = "auto";
  el.style.height = Math.min(el.scrollHeight, 120) + "px";
  const l = el.value.length;
  document.getElementById("char-count").textContent = l + " / 500";
}

function handleKey(e) {
  if (e.key === "Enter" && !e.shiftKey) {
    e.preventDefault();
    sendMessage();
  }
}

function fillQ(text) {
  const box = document.getElementById("user-input");
  box.value = text;
  onInput(box);
  box.focus();
}

function fireQ(btn) {
  fillQ(btn.innerText.trim());
  sendMessage();
}

function appendMsg(role, content, isHtml) {
  const msgs = document.getElementById("messages");
  const row = document.createElement("div");
  row.className = "msg-row " + role;
  const av = document.createElement("div");
  av.className = "avatar " + role;
  av.textContent = role === "bot" ? "🌿" : "👤";
  const bub = document.createElement("div");
  bub.className = "bubble " + role;
  if (isHtml) {
    bub.innerHTML = content;
  } else {
    bub.textContent = content;
  }
  row.appendChild(av);
  row.appendChild(bub);
  msgs.appendChild(row);
  msgs.scrollTop = msgs.scrollHeight;
}

function showTyping() {
  const msgs = document.getElementById("messages");
  const row = document.createElement("div");
  row.className = "msg-row bot";
  row.id = "typing-row";
  row.innerHTML =
    '<div class="avatar bot">🌿</div>' +
    '<div class="bubble bot"><div class="typing">' +
    "<span></span><span></span><span></span>" +
    "</div></div>";
  msgs.appendChild(row);
  msgs.scrollTop = msgs.scrollHeight;
}

function hideTyping() {
  const el = document.getElementById("typing-row");
  if (el) el.remove();
}

function formatResponse(text) {
  return text
    .replace(/\*\*(.*?)\*\*/g, "<strong>$1</strong>")
    .replace(
      /^[•\-\*] (.+)$/gm,
      '<div style="display:flex;gap:6px;margin:3px 0">' +
        '<span style="color:#1a6b3c;flex-shrink:0">•</span>' +
        "<span>$1</span></div>"
    )
    .replace(
      /^\d+\. (.+)$/gm,
      '<div style="display:flex;gap:6px;margin:3px 0">' +
        '<span style="color:#1a6b3c;font-weight:600;flex-shrink:0">→</span>' +
        "<span>$1</span></div>"
    )
    .replace(/\n\n/g, "<br><br>")
    .replace(/\n/g, "<br>");
}

async function sendMessage() {
  if (loading) return;
  const inp = document.getElementById("user-input");
  const msg = inp.value.trim();
  if (!msg) {
    inp.focus();
    return;
  }
  if (msg.length > 500) {
    alert("Please keep your question under 500 characters.");
    return;
  }

  const city = document.getElementById("city-sel").value;
  appendMsg("user", msg, false);
  history.push({ role: "user", content: msg });
  inp.value = "";
  onInput(inp);

  loading = true;
  document.getElementById("send-btn").disabled = true;
  document.getElementById("status-lbl").textContent = "EcoBot thinking...";
  showTyping();

  try {
    const res = await fetch(API_BASE + "/chat", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ message: msg, location: city }),
    });
    const data = await res.json();
    if (data.error) throw new Error(data.error);
    const reply = data.response;
    history.push({ role: "assistant", content: reply });
    hideTyping();
    appendMsg("bot", formatResponse(reply), true);
  } catch (err) {
    hideTyping();
    appendMsg(
      "bot",
      "Could not connect. Make sure Flask is running — open terminal, go to backend folder, run: python app.py",
      false
    );
    console.error(err);
  } finally {
    loading = false;
    document.getElementById("send-btn").disabled = false;
    document.getElementById("status-lbl").textContent = "AI Ready";
    document.getElementById("user-input").focus();
  }
}