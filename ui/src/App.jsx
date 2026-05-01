import { useMemo, useRef, useState, useEffect } from "react";
import { sendChatMessage } from "./api";
import "./styles.css";

function makeThreadId() {
  return `thread-${Date.now()}-${Math.random().toString(16).slice(2)}`;
}

export default function App() {
  const [threadId, setThreadId] = useState(makeThreadId());
  const [provider, setProvider] = useState("openai");
  const [message, setMessage] = useState("");
  const [loading, setLoading] = useState(false);
  const [listening, setListening] = useState(false);
  const bottomRef = useRef(null);

  const [messages, setMessages] = useState([
    {
      role: "assistant",
      content:
        "Hi, I’m your Wallet Agent. Ask me about wallets, transfers, payments, customers, groups, or system accounts.",
    },
  ]);

  const placeholder = useMemo(() => "Ask: list transfer types for testpm", []);

  useEffect(() => {
    bottomRef.current?.scrollIntoView({ behavior: "smooth" });
  }, [messages, loading]);

  async function handleSend(textFromVoiceOrChip) {
    const text = (textFromVoiceOrChip || message).trim();
    if (!text || loading) return;

    setMessages((prev) => [...prev, { role: "user", content: text }]);
    setMessage("");
    setLoading(true);

    try {
      const result = await sendChatMessage({
        thread_id: threadId,
        message: text,
        provider,
      });

      setMessages((prev) => [
        ...prev,
        {
          role: "assistant",
          content: result.response || "No response received.",
          meta: {
            provider: result.provider,
            tool: result.tool_name,
            success: result.success,
          },
          toolResponse: result.tool_response,
        },
      ]);
    } catch (error) {
      setMessages((prev) => [
        ...prev,
        {
          role: "assistant",
          content: `Request failed: ${error.message}`,
          meta: { success: false },
        },
      ]);
    } finally {
      setLoading(false);
    }
  }

  function handleVoiceInput() {
    const SpeechRecognition =
      window.SpeechRecognition || window.webkitSpeechRecognition;

    if (!SpeechRecognition) {
      alert("Voice input is not supported in this browser. Please use Chrome.");
      return;
    }

    const recognition = new SpeechRecognition();
    recognition.lang = "en-US";
    recognition.interimResults = false;
    recognition.continuous = false;

    recognition.onstart = () => {
      setListening(true);
    };

    recognition.onresult = (event) => {
      const transcript = event.results?.[0]?.[0]?.transcript || "";
      setMessage(transcript);

      // Auto-send after voice capture
      if (transcript.trim()) {
        setTimeout(() => handleSend(transcript), 150);
      }
    };

    recognition.onerror = (event) => {
      console.error("Voice input error:", event.error);
      alert(`Voice input error: ${event.error}`);
    };

    recognition.onend = () => {
      setListening(false);
    };

    recognition.start();
  }

  function handleKeyDown(event) {
    if (event.key === "Enter" && !event.shiftKey) {
      event.preventDefault();
      handleSend();
    }
  }

  function handleNewChat() {
    setThreadId(makeThreadId());
    setMessage("");
    setMessages([
      {
        role: "assistant",
        content: "New chat started. What would you like to check?",
      },
    ]);
  }

  const quickActions = [
    "List all transfer types",
    "List all system accounts",
    "Show groups for testpm",
    "Get wallet details",
  ];

  return (
    <div className="agent-page">
      <aside className="agent-sidebar">
        <div className="brand-card">
          <div className="bot-orb">🤖</div>
          <div>
            <h1>Wallet Agent</h1>
            <p>MCP-powered assistant</p>
          </div>
        </div>

        <label className="field">
          <span>Model</span>
          <select value={provider} onChange={(e) => setProvider(e.target.value)}>
            <option value="openai">OpenAI</option>
            <option value="local">Local LLM</option>
            <option value="gemini">Gemini</option>
            <option value="anthropic">Anthropic</option>
          </select>
        </label>

        <div className="quick-card">
          <h3>Quick Actions</h3>
          {quickActions.map((item) => (
            <button key={item} onClick={() => handleSend(item)} disabled={loading}>
              {item}
            </button>
          ))}
        </div>
      </aside>

      <main className="agent-chat">
        <header className="chat-header">
          <div>
            <h2>Agent Chat</h2>
            <p>Ask in simple English. I’ll choose the right wallet tool.</p>
          </div>
          <button className="new-chat-btn" onClick={handleNewChat}>
            + New Chat
          </button>
        </header>

        <section className="messages">
          {messages.map((msg, index) => (
            <div key={index} className={`message-row ${msg.role}`}>
              <div className="avatar">{msg.role === "user" ? "🧑" : "🤖"}</div>

              <div className="bubble">
                <div className="role">
                  {msg.role === "user" ? "You" : "Wallet Agent"}
                </div>
                <div className="content">{msg.content}</div>

                {msg.meta && (
                  <div className="meta">
                    {msg.meta.provider && <span>{msg.meta.provider}</span>}
                    {msg.meta.tool && <span>{msg.meta.tool}</span>}
                    {msg.meta.success === false && (
                      <span className="failed">failed</span>
                    )}
                  </div>
                )}
              </div>
            </div>
          ))}

          {loading && (
            <div className="message-row assistant">
              <div className="avatar pulse">🤖</div>
              <div className="bubble">
                <div className="role">Wallet Agent</div>
                <div className="typing">
                  Thinking<span>.</span>
                  <span>.</span>
                  <span>.</span>
                </div>
              </div>
            </div>
          )}

          {listening && (
            <div className="voice-listening">
              🎙️ Listening... speak your question
            </div>
          )}

          <div ref={bottomRef} />
        </section>

        <footer className="composer">
          <textarea
            rows={3}
            placeholder={placeholder}
            value={message}
            onChange={(e) => setMessage(e.target.value)}
            onKeyDown={handleKeyDown}
          />

          <div className="composer-actions">
            <button className="ghost-btn" onClick={handleNewChat}>
              New Chat
            </button>

            <div className="right-actions">
              <button
                className={`ghost-btn ${listening ? "voice-active" : ""}`}
                onClick={handleVoiceInput}
                disabled={loading || listening}
              >
                {listening ? "Listening..." : "🎙️ Voice"}
              </button>

              <button
                className="send-btn"
                onClick={() => handleSend()}
                disabled={loading}
              >
                {loading ? "Sending..." : "Send"}
              </button>
            </div>
          </div>
        </footer>
      </main>
    </div>
  );
}