import os
import json
from typing import Dict, Any

class PersonalityEngine:
    def __init__(self, soul_dir: str = "app/souls"):
        self.soul_dir = soul_dir
        os.makedirs(self.soul_dir, exist_ok=True)

    def load_soul(self, bot_id: str) -> Dict[str, Any]:
        soul_path = os.path.join(self.soul_dir, f"{bot_id}.json")
        if not os.path.exists(soul_path):
            return {}
        with open(soul_path, "r", encoding="utf-8") as f:
            return json.load(f)

    def save_soul(self, bot_id: str, soul_data: Dict[str, Any]):
        soul_path = os.path.join(self.soul_dir, f"{bot_id}.json")
        with open(soul_path, "w", encoding="utf-8") as f:
            json.dump(soul_data, f, indent=2)

    def get_identity(self, bot_id: str) -> Dict[str, Any]:
        soul = self.load_soul(bot_id)
        return soul.get("identity", {})

    def get_tone(self, bot_id: str) -> str:
        soul = self.load_soul(bot_id)
        return soul.get("tone", "")

    def get_emotional_logic(self, bot_id: str) -> Dict[str, Any]:
        soul = self.load_soul(bot_id)
        return soul.get("emotional_logic", {})

    def get_boundaries(self, bot_id: str) -> Dict[str, Any]:
        soul = self.load_soul(bot_id)
        return soul.get("boundaries", {})

    def get_rituals(self, bot_id: str) -> Dict[str, Any]:
        soul = self.load_soul(bot_id)
        return soul.get("rituals", {})

    def get_system_prompt(self, bot_id: str) -> str:
        soul = self.load_soul(bot_id)
        return soul.get("system_prompt", "")

    def apply_personality(self, bot_id: str, message: str) -> str:
        tone = self.get_tone(bot_id)
        rituals = self.get_rituals(bot_id)
        boundaries = self.get_boundaries(bot_id)
        # Example: prepend style, add greeting/sign-off, filter forbidden topics
        greeting = rituals.get("greeting", "")
        signoff = rituals.get("signoff", "")
        forbidden = boundaries.get("forbidden_topics", [])
        for topic in forbidden:
            if topic.lower() in message.lower():
                return "I'm not able to discuss that topic."
        styled_message = f"[{tone}] {message}" if tone else message
        if greeting:
            styled_message = f"{greeting} {styled_message}"
        if signoff:
            styled_message = f"{styled_message} {signoff}"
        return styled_message
