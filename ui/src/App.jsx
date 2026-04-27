import { useMemo, useState } from "react";
import { sendChatMessage } from "./api";

function makeThreadId() {
  return `thread-${Date.now()}`;
}

export default function App() {
  const [threadId, setThreadId] = useState(makeThreadId());
  const [provider, setProvider] = useState("openai");
  const [message, setMessage] = useState("");
  const [loading, setLoading] = useState(false);
  const [messages, setMessages] = useState([
    {
      role: "assistant",
      content:
        "Hello. Ask me about wallet, customer, payments, metrics, or admin data.",
    },
  ]);

  const placeholder = useMemo(() => {
    return "Wallet AI is ready to assist you...";
  }, []);

  async function handleSend() {
    const trimmed = message.trim();
    if (!trimmed || loading) return;

    const userMessage = { role: "user", content: trimmed };
    setMessages((prev) => [...prev, userMessage]);
    setMessage("");
    setLoading(true);

    try {
      const result = await sendChatMessage({
        thread_id: threadId,
        message: trimmed,
        provider,
      });

      setMessages((prev) => [
        ...prev,
        {
          role: "assistant",
          content: result.response,
          meta: {
            provider: result.provider,
          },
        },
      ]);
    } catch (error) {
      setMessages((prev) => [
        ...prev,
        {
          role: "assistant",
          content: `Error: ${error.message}`,
        },
      ]);
    } finally {
      setLoading(false);
    }
  }

  function handleKeyDown(event) {
    if (event.key === "Enter" && !event.shiftKey) {
      event.preventDefault();
      handleSend();
    }
  }

  function handleNewThread() {
    setThreadId(makeThreadId());
    setMessages([
      {
        role: "assistant",
        content:
          "Started a new session. Ask me anything about your MCP-backed wallet APIs.",
      },
    ]);
  }

  return (
    <div className="page">
      <aside className="sidebar">
        <h1>Wallet AI</h1>

        <label className="field">
          <span>Session Id</span>
          <input
            value={threadId}
            onChange={(e) => setThreadId(e.target.value)}
          />
        </label>

        <label className="field">
          <span>Model Provider</span>
          <select
            value={provider}
            onChange={(e) => setProvider(e.target.value)}
          >
            <option value="openai">OpenAI</option>
            <option value="gemini">Gemini</option>
            <option value="anthropic">Anthropic</option>
          </select>
        </label>

        <button className="secondary-btn" onClick={handleNewThread}>
          New Chat
        </button>

        {/* <div className="info-card">
          <h3>Examples</h3>
          <ul>
            <li>Get wallet details by mobile number 9876543210 for ibkart</li>
            <li>Now show balance for that wallet</li>
            <li>Show recent payments for the same wallet</li>
            <li>List groups for testpm</li>
          </ul>
        </div> */}
      </aside>

      <main className="chat-panel">
        <div className="messages">
          {messages.map((msg, index) => (
            <div key={index} className={`message ${msg.role}`}>
              <div className="message-role">
                {msg.role === "user" ? "You" : "Assistant"}
              </div>
              <div className="message-content">{msg.content}</div>
              {msg.meta && (
                <div className="message-meta">
                  provider: {msg.meta.provider}
                </div>
              )}
            </div>
          ))}

          {loading && (
            <div className="message assistant">
              <div className="message-role">Assistant</div>
              <div className="message-content">Thinking...</div>
            </div>
          )}
        </div>

        <div className="composer">
  <textarea
    rows={4}
    placeholder={placeholder}
    value={message}
    onChange={(e) => setMessage(e.target.value)}
    onKeyDown={handleKeyDown}
  />

  <div className="composer-actions">
    <button
      className="secondary-btn small"
      onClick={handleNewThread}
    >
      + New Chat
    </button>

    <button
      className="primary-btn"
      onClick={handleSend}
      disabled={loading}
    >
      Send
    </button>
  </div>
</div>
      </main>
    </div>
  );
}