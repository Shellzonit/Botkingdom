import React, { useState } from "react";
import Chat from "./Chat";
import BotManager from "./BotManager";
import Home from "./Home";

export default function App() {
  const [page, setPage] = useState("home");
  return (
    <div className="app-container">
      <nav style={{ marginBottom: 24 }}>
        <button onClick={() => setPage("home")}>Home</button>
        <button onClick={() => setPage("chat")}>Chat</button>
        <button onClick={() => setPage("bots")}>Bot Management</button>
      </nav>
      {page === "home" && <Home />}
      {page === "chat" && <Chat />}
      {page === "bots" && <BotManager />}
    </div>
  );
}
