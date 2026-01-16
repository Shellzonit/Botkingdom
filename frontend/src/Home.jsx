import React from "react";
import "./Home.css";

const bots = [
  { name: "Ana", file: "Ana_raw.png", tagline: "Empathetic advisor" },
  { name: "Blaze", file: "Blaze_raw.png", tagline: "Energetic motivator" },
  { name: "Dav", file: "Dav_raw.png", tagline: "Strategic thinker" },
  { name: "Dude", file: "Dude_raw.png", tagline: "Casual companion" },
  { name: "Lori", file: "Lori_raw.png", tagline: "Creative muse" },
  { name: "Mick", file: "Mick_raw.png", tagline: "Wise mentor" },
  { name: "Tori", file: "Tori_raw.png", tagline: "Futuristic guide" },
];

export default function Home({ setPage, setActiveBot }) {
  // If setPage/setActiveBot not provided, fallback to no-op
  const handleTalk = (bot) => {
    if (setActiveBot) setActiveBot(bot);
    if (setPage) setPage("chat");
  };
  return (
    <div className="ocean-bg home-victorian">
      <div className="banner">
        <h1>Welcome to Bot Kingdom</h1>
        <p className="intro">Meet the royal family of bots, each with a unique personality and role. Click a bot to start a conversation!</p>
      </div>
      <div className="bot-grid">
        {bots.map((bot) => (
          <div className="bot-slot" key={bot.name}>
            <img src={process.env.PUBLIC_URL + '/' + bot.file} alt={bot.name} className="bot-avatar" />
            <div className="bot-name">{bot.name}</div>
            <div className="bot-tagline">{bot.tagline}</div>
            <button className="talk-btn" onClick={() => handleTalk(bot)}>
              Talk to {bot.name}
            </button>
          </div>
        ))}
      </div>
    </div>
  );
}
