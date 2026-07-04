/**
 * Ajudante do Prof. Rodrigo — Frontend Logic
 * Handles chat interaction, session management, and UI updates.
 */

(() => {
    "use strict";

    // ── DOM Elements ──────────────────────────────────
    const chatMessages = document.getElementById("chat-messages");
    const chatForm = document.getElementById("chat-form");
    const messageInput = document.getElementById("message-input");
    const btnSend = document.getElementById("btn-send");
    const btnReset = document.getElementById("btn-reset");
    const typingIndicator = document.getElementById("typing-indicator");
    const toastContainer = document.getElementById("toast-container");

    // ── Session ───────────────────────────────────────
    let sessionId = localStorage.getItem("session_id");
    if (!sessionId) {
        sessionId = crypto.randomUUID();
        localStorage.setItem("session_id", sessionId);
    }

    // ── Helpers ───────────────────────────────────────

    /** Convert basic markdown-like formatting to HTML */
    function formatMessage(text) {
        return text
            // Images ![alt](url)
            .replace(/!\[([^\]]*)\]\(([^)]+)\)/g,
                '<div class="msg-image"><img src="$2" alt="$1" loading="lazy" onerror="this.parentElement.innerHTML=\'<span class=img-fallback>🖼️ Imagem indisponível</span>\'"><span class="img-caption">$1</span></div>')
            // Links [text](url)
            .replace(/\[([^\]]+)\]\(([^)]+)\)/g, '<a href="$2" target="_blank" rel="noopener">$1</a>')
            // Headers (### text)
            .replace(/^### (.+)$/gm, "<h3>$1</h3>")
            // Bold (**text**)
            .replace(/\*\*(.+?)\*\*/g, "<strong>$1</strong>")
            // Italic (*text*)
            .replace(/(?<!\*)\*([^*]+)\*(?!\*)/g, "<em>$1</em>")
            // Unordered list items (- text)
            .replace(/^- (.+)$/gm, "<li>$1</li>")
            // Wrap consecutive <li> in <ul>
            .replace(/((?:<li>.*<\/li>\n?)+)/g, "<ul>$1</ul>")
            // Line breaks (double newline → paragraph break)
            .replace(/\n\n/g, "</p><p>")
            // Single newlines → <br>
            .replace(/\n/g, "<br>")
            // Wrap in paragraph
            .replace(/^(.+)$/, "<p>$1</p>");
    }

    /** Append a message bubble to the chat */
    function addMessage(content, role) {
        const msgDiv = document.createElement("div");
        msgDiv.className = `message ${role}`;

        const avatarEmoji = role === "bot" ? "🐉" : "👤";

        msgDiv.innerHTML = `
            <div class="msg-avatar">${avatarEmoji}</div>
            <div class="msg-content">${formatMessage(content)}</div>
        `;

        chatMessages.appendChild(msgDiv);
        scrollToBottom();
    }

    /** Scroll chat to bottom */
    function scrollToBottom() {
        requestAnimationFrame(() => {
            chatMessages.scrollTop = chatMessages.scrollHeight;
        });
    }

    /** Show/hide typing indicator */
    function setTyping(show) {
        typingIndicator.classList.toggle("active", show);
        if (show) scrollToBottom();
    }

    /** Toggle input state */
    function setInputEnabled(enabled) {
        messageInput.disabled = !enabled;
        btnSend.disabled = !enabled;
        if (enabled) messageInput.focus();
    }

    /** Show a toast notification */
    function showToast(message, type = "success") {
        const toast = document.createElement("div");
        toast.className = `toast ${type}`;
        toast.textContent = message;
        toastContainer.appendChild(toast);

        setTimeout(() => toast.remove(), 4200);
    }

    // ── API Communication ─────────────────────────────

    async function sendMessage(text) {
        addMessage(text, "user");
        setInputEnabled(false);
        setTyping(true);

        try {
            const res = await fetch("/api/chat", {
                method: "POST",
                headers: { "Content-Type": "application/json" },
                body: JSON.stringify({
                    message: text,
                    session_id: sessionId,
                }),
            });

            const data = await res.json();

            setTyping(false);

            if (data.status === "success") {
                addMessage(data.response, "bot");

                // Detect action confirmations for toasts
                if (data.response.includes("✅")) {
                    showToast("Planilha atualizada com sucesso!", "success");
                }
                if (data.response.includes("📧")) {
                    showToast("E-mail enviado com sucesso!", "success");
                }
            } else {
                addMessage(data.response || "Ocorreu um erro. Tente novamente.", "bot");
                showToast("Erro no processamento", "error");
            }
        } catch (err) {
            setTyping(false);
            addMessage("😕 Não foi possível conectar ao servidor. Verifique sua conexão.", "bot");
            showToast("Erro de conexão", "error");
            console.error("Chat error:", err);
        } finally {
            setInputEnabled(true);
        }
    }

    // ── Event Listeners ───────────────────────────────

    chatForm.addEventListener("submit", (e) => {
        e.preventDefault();
        const text = messageInput.value.trim();
        if (!text) return;
        messageInput.value = "";
        sendMessage(text);
    });

    btnReset.addEventListener("click", () => {
        // New session
        sessionId = crypto.randomUUID();
        localStorage.setItem("session_id", sessionId);

        // Clear chat
        chatMessages.innerHTML = "";

        // Trigger welcome message
        sendWelcome();
        showToast("Nova conversa iniciada!", "success");
    });

    // ── Init ──────────────────────────────────────────

    /** Send an initial greeting to trigger the bot's welcome message */
    async function sendWelcome() {
        setInputEnabled(false);
        setTyping(true);

        try {
            const res = await fetch("/api/chat", {
                method: "POST",
                headers: { "Content-Type": "application/json" },
                body: JSON.stringify({
                    message: "Olá",
                    session_id: sessionId,
                }),
            });
            const data = await res.json();
            setTyping(false);
            addMessage(data.response, "bot");
        } catch (err) {
            setTyping(false);
            addMessage("😕 Não foi possível conectar ao servidor.", "bot");
        } finally {
            setInputEnabled(true);
        }
    }

    // Auto-start
    sendWelcome();
})();
