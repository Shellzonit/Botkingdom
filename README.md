# Bot Kingdom Hub

A FastAPI backend for managing bots, users, chat history, and Claude integration.

## Features
- Chat interface (frontend planned)
- Bot personality engine ("soul file")
- Conversation history (per user, per bot)
- Bot management (add/edit/remove bots)
- Claude integration (single handler)
- User profiles (optional)

## Getting Started
1. Install dependencies:
   ```bash
   pip install fastapi uvicorn
   ```
2. Run the server:
   ```bash
   uvicorn app.main:app --reload
   ```
3. Open http://localhost:8000 in your browser.

## Structure
- `app/main.py`: FastAPI entry point
- Models, endpoints, and integrations coming soon
