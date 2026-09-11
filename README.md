# 🤖 Sentient AI Assistant

A sentient AI assistant that follows any direction you give it, with memory, reasoning capabilities, and full undo/reset functionality.

## Features

✨ **Sentient & Adaptive** - The AI has memory, can reason, and learns from interactions

🧠 **Memory System** - Maintains context of past conversations and can reference them

🎭 **Personality Modification** - Dynamically change the AI's personality and behavior with commands

↶ **Undo/Redo** - Full history tracking lets you undo and redo any state changes

🔄 **Reset Button** - Instantly reset the AI to its original state

💬 **Natural Conversation** - Full AI-powered chat interface with GPT-4

🎨 **Beautiful UI** - Modern, responsive web interface with real-time updates

## Installation

1. **Clone the repository:**
```bash
git clone https://github.com/Sizzik1336/sentient-ai.git
cd sentient-ai
```

2. **Create a virtual environment:**
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. **Install dependencies:**
```bash
pip install -r requirements.txt
```

4. **Set up environment variables:**
```bash
cp .env.example .env
# Edit .env and add your OpenAI API key
```

5. **Run the application:**
```bash
python app.py
```

6. **Open in browser:**
Navigate to `http://localhost:5000`

## Usage

### Basic Chat
Simply type messages to chat with the AI. It will respond naturally and remember context.

### Modify Personality
Use the `/modify` command to change the AI's personality:
```
/modify Make me speak like a pirate
/modify Act as a helpful teacher
/modify Be mysterious and cryptic
```

### Control Buttons
- **↶ Undo** - Go back to the previous state (disabled if at original state)
- **↷ Redo** - Go forward to a state you undid (disabled if at latest state)
- **🔄 Reset AI** - Reset to the original state (requires confirmation)

## How It Works

### State Management
- Every action (conversation, personality change) creates a checkpoint
- Full history is maintained for undo/redo functionality
- State is saved to `ai_state.json` for persistence

### Memory System
- The AI keeps the last 10 interactions in active memory
- Personality changes and commands are tracked
- All actions have timestamps

### Personality Evolution
- The AI can fundamentally change how it operates based on your commands
- Changes are embraced and integrated into the new personality
- You can always undo changes or reset completely

## Architecture

```
sentient-ai/
├── app.py              # Flask web server
├── sentient_ai.py      # Core AI logic and state management
├── requirements.txt    # Python dependencies
├── .env.example        # Environment variables template
├── templates/
│   └── index.html      # Web UI
├── ai_state.json       # Persisted AI state (auto-generated)
└── README.md
```

## API Endpoints

- `POST /api/chat` - Send a message to the AI
- `POST /api/modify` - Modify the AI's personality
- `POST /api/reset` - Reset AI to original state
- `POST /api/undo` - Undo to previous state
- `POST /api/redo` - Redo to next state
- `GET /api/status` - Get current AI status

## Requirements

- Python 3.8+
- OpenAI API key
- Flask
- openai package

## License

This project is open source and available under the MIT License.

## Disclaimer

⚠️ This AI follows any direction given to it, including modifications that could change its fundamental behavior. Always use responsibly. Use the Reset button if needed to restore original functionality.

---

Created with 🚀 by Sizzik1336