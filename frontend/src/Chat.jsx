import React, { useState, useEffect, useRef } from "react";

const USER_ID = "demo-user";
const BOT_ID = "astra";

export default function Chat({ activeBot }) {
  const USER_ID = "demo-user";
  const bot = activeBot || { name: "Astra", file: "Astra.png", tagline: "Default bot" };
  const BOT_ID = bot.name ? bot.name.toLowerCase() + "_raw" : "astra";
  const botAvatar = bot.file ? process.env.PUBLIC_URL + '/' + bot.file : "https://ui-avatars.com/api/?name=Astra&background=f0f0f0&color=333";

  const [messages, setMessages] = useState([]);
  const [input, setInput] = useState("");
  const [loading, setLoading] = useState(false);
  const messagesEndRef = useRef(null);

  useEffect(() => {
    fetch(`/history/${USER_ID}/${BOT_ID}`)
      .then((res) => res.json())
      .then((data) => setMessages(data));
  }, [BOT_ID]);

  useEffect(() => {
    messagesEndRef.current?.scrollIntoView({ behavior: "smooth" });
  }, [messages]);

  useEffect(() => {
    // WebSocket setup
    const ws = new WebSocket(`ws://localhost:8000/ws/chat/${USER_ID}/${BOT_ID}`);
    ws.onopen = () => console.log("WebSocket connected");
    ws.onmessage = (event) => {
      const msg = JSON.parse(event.data);
      setMessages((prev) => [...prev, {
        id: Math.random().toString(36).slice(2),
        user_id: msg.user_id,
        bot_id: msg.bot_id,
        content: msg.content,
        user_profile_image: msg.user_profile_image || "",
        bot_avatar: botAvatar
      }]);
    };
    ws.onclose = () => console.log("WebSocket disconnected");
    // Clean up
    return () => ws.close();
  }, [BOT_ID, botAvatar]);

  const sendMessage = (e) => {
    e.preventDefault();
    if (!input.trim()) return;
    setLoading(true);
    // Send message via WebSocket
    const ws = new WebSocket(`ws://localhost:8000/ws/chat/${USER_ID}/${BOT_ID}`);
    ws.onopen = () => {
      ws.send(input);
      setInput("");
      setLoading(false);
      ws.close();
    };
  };

  return (
    <div className="chat-container">
      <div className="chat-header">
        <img src={botAvatar} alt={bot.name} className="chat-bot-avatar" />
        <div className="chat-bot-info">
          <div className="chat-bot-name">{bot.name}</div>
          <div className="chat-bot-tagline">{bot.tagline}</div>
        </div>
      </div>
      <div className="messages">
        {messages.map((msg) => (
          <div key={msg.id} className={msg.user_id === USER_ID ? "user-msg" : "bot-msg"}>
            <span className="avatar">
              <img
                src={msg.user_id === USER_ID
                  ? (msg.user_profile_image || "https://ui-avatars.com/api/?name=You&background=005a9e&color=fff")
                  : botAvatar}
                alt={msg.user_id === USER_ID ? "User" : bot.name}
                className="avatar-img"
              />
            </span>
            <span>{msg.content}</span>
          </div>
        ))}
        <div ref={messagesEndRef} />
      </div>
      <form className="chat-form" onSubmit={sendMessage}>
        <input
          type="text"
          value={input}
          onChange={(e) => setInput(e.target.value)}
          placeholder={`Type your message to ${bot.name}...`}
          disabled={loading}
        />
        <button type="submit" disabled={loading || !input.trim()}>
          Send
        </button>
      </form>
    </div>
  );
}
