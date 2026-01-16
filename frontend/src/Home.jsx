import React from "react";
import "./Home.css";

const bots = [
  { name: "Ana_raw", tagline: "Empathetic advisor", avatar: "https://ui-avatars.com/api/?name=Ana&background=005a9e&color=fff" },
  { name: "Blaze_raw", tagline: "Energetic motivator", avatar: "https://ui-avatars.com/api/?name=Blaze&background=005a9e&color=fff" },
  { name: "Dav_raw", tagline: "Strategic thinker", avatar: "https://ui-avatars.com/api/?name=Dav&background=005a9e&color=fff" },
  { name: "Dude_raw", tagline: "Casual companion", avatar: "https://ui-avatars.com/api/?name=Dude&background=005a9e&color=fff" },
  { name: "Lori_raw", tagline: "Creative muse", avatar: "https://ui-avatars.com/api/?name=Lori&background=005a9e&color=fff" },
  { name: "Mick_raw", tagline: "Wise mentor", avatar: "https://ui-avatars.com/api/?name=Mick&background=005a9e&color=fff" },
  { name: "Tori_raw", tagline: "Futuristic guide", avatar: "https://ui-avatars.com/api/?name=Tori&background=005a9e&color=fff" },
];

export default function Home() {
  return (
    <div className="ocean-bg home-victorian">
      <div className="banner">
        <h1>Welcome to Bot Kingdom</h1>
      </div>
      <div className="bot-grid">
        {bots.map((bot) => (
          <div className="bot-slot" key={bot.name}>
            <img src={bot.avatar} alt={bot.name} className="bot-avatar" />
            <div className="bot-name">{bot.name}</div>
            <div className="bot-tagline">{bot.tagline}</div>
          </div>
        ))}
      </div>
    </div>
  );
}
