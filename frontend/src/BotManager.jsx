import React, { useState, useEffect } from "react";

export default function BotManager() {
  const [bots, setBots] = useState([]);
  const [form, setForm] = useState({ id: "", name: "", description: "", bot_avatar: "" });
  const [editing, setEditing] = useState(null);

  useEffect(() => {
    fetch("/bots")
      .then((res) => res.json())
      .then((data) => setBots(data));
  }, []);

  const handleChange = (e) => {
    setForm({ ...form, [e.target.name]: e.target.value });
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    const method = editing ? "POST" : "POST";
    await fetch("/bots", {
      method,
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(form)
    });
    setEditing(null);
    setForm({ id: "", name: "", description: "", bot_avatar: "" });
    // Refresh bots (ideally fetch all)
  };

  const handleEdit = (bot) => {
    setForm({
      id: bot.id,
      name: bot.name,
      description: bot.description || "",
      bot_avatar: bot.bot_avatar || ""
    });
    setEditing(bot.id);
  };

  const handleRemove = async (botId) => {
    await fetch(`/bots/${botId}`, { method: "DELETE" });
    setBots(bots.filter((b) => b.id !== botId));
  };

  return (
    <div className="bot-manager">
      <h2>Bot Management</h2>
      <form onSubmit={handleSubmit} className="bot-form">
        <input name="id" value={form.id} onChange={handleChange} placeholder="Bot ID" required />
        <input name="name" value={form.name} onChange={handleChange} placeholder="Bot Name" required />
        <input name="description" value={form.description} onChange={handleChange} placeholder="Description" />
        <input name="bot_avatar" value={form.bot_avatar} onChange={handleChange} placeholder="Avatar URL" />
        <button type="submit">{editing ? "Update Bot" : "Add Bot"}</button>
      </form>
      <div className="bot-list">
        {bots.map((bot) => (
          <div key={bot.id} className="bot-item">
            <img src={bot.bot_avatar || "https://ui-avatars.com/api/?name=Bot"} alt={bot.name} className="avatar-img" />
            <div>
              <strong>{bot.name}</strong>
              <p>{bot.description}</p>
            </div>
            <button onClick={() => handleEdit(bot)}>Edit</button>
            <button onClick={() => handleRemove(bot.id)}>Remove</button>
          </div>
        ))}
      </div>
    </div>
  );
}
