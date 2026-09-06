---
title: FitBuddy AI Fitness Coach
emoji: 💪
colorFrom: "#e94560"
colorTo: "#f5a623"
sdk: docker
pinned: false
license: mit
---

# 🏋️ FitBuddy – AI Fitness Coach Chatbot

FitBuddy is a conversational AI fitness coach built with **LangChain** and **OpenAI GPT-4o-mini**. It remembers your fitness goals across a conversation, performs calorie/math calculations on the fly, and responds in a friendly, concise coaching style.

**Available as:**
- 🖥️ Terminal-based chatbot
- 🌐 Streamlit web app with modern UI

---

## Features

- 🧠 **Conversation Memory** – Remembers user-provided workout preferences and goals within a session using `ConversationBufferMemory`.
- 🔢 **Calculator Tool** – Answers calorie-math and arithmetic queries (e.g., *"If I burn 90 cal in 10 mins, how many in 1 hour?"*).
- 🤖 **Agent + Chain Fallback** – Uses a LangChain agent as the primary responder, with a simple prompt chain as a fallback if the agent encounters an error.
- 💬 **Two Modes** – Run a built-in demo conversation **or** launch an interactive chat loop in your terminal.

---

## Project Structure

```
FitnessApp/
├── Langchain_Fitness_ChatBuddy.py   # Terminal-based chatbot
├── streamlit_app.py                # Streamlit web app
├── Dockerfile                       # Docker configuration for deployment
├── requirements.txt                 # Python dependencies
├── .env                             # API keys (not committed to version control)
├── .env.example                     # Example environment file
└── README.md
```

---

## Prerequisites

- Python 3.12+
- An [OpenAI API key](https://platform.openai.com/api-keys)

---

## Setup

### 1. Clone / download the project

```bash
git clone <your-repo-url>
cd FitnessApp
```

### 2. Create and activate a virtual environment (recommended)

```bash
python -m venv venv
# Windows
venv\Scripts\activate
# macOS / Linux
source venv/bin/activate
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Configure environment variables

Create a `.env` file in the project root (or edit the existing one):

```env
OPENAI_API_KEY=your-openai-api-key-here
# Optional: only needed if using a custom OpenAI-compatible endpoint
OPENAI_API_BASE=https://api.openai.com/v1
```

> ⚠️ **Never commit your `.env` file to version control.** Add it to `.gitignore`.

---

## Running the App

### Option 1: Terminal-based Chatbot

```bash
python Langchain_Fitness_ChatBuddy.py
```

You will be prompted to choose a mode:

| Option | Mode | Description |
|--------|------|-------------|
| `1` | Demo | Runs 3 pre-scripted turns showing memory + calculator |
| `2` | Interactive | Live chat loop – type freely and press Enter |

### Interactive mode commands

| Input | Action |
|-------|--------|
| `memory` | Print the full conversation history |
| `quit` / `exit` / `q` | End the session |

---

### Option 2: Streamlit Web App

```bash
streamlit run streamlit_app.py
```

The web app features:
- 🎨 Modern dark-themed UI
- 💬 Chat interface with message history
- ⚡ Quick prompts sidebar
- 📊 Session statistics
- 🔧 API key configuration in sidebar

---

## Docker Deployment

### Local Docker Testing

```bash
# Build the image
docker build -t fitbuddy-app .

# Run the container
docker run -p 7860:7860 --env-file .env fitbuddy-app
```

Access the app at http://localhost:7860

---

### Deploy to Hugging Face Spaces

1. Create a new Space at [huggingface.co/spaces](https://huggingface.co/spaces)
   - **SDK**: Docker
   - **Visibility**: Public or Private

2. Upload these files:
   - `Dockerfile`
   - `requirements.txt`
   - `streamlit_app.py`
   - `README.md` (this file)

3. Set your `OPENAI_API_KEY` as a Space Secret:
   - Go to Settings → Repository secrets
   - Add secret name: `OPENAI_API_KEY`
   - Add your API key value

4. Hugging Face will automatically build and deploy your app!

---

## How It Works

```
User Input
    │
    ▼
LangChain Agent  ──(tool call)──▶  Calculator Tool
    │                                     │
    └──────────────◀─────────────────────┘
    │  (agent fails)
    ▼
Simple LLM Chain  (prompt | GPT-4o-mini | StrOutputParser)
    │  (chain fails + math detected)
    ▼
Direct Calculator Fallback
```

1. **Agent** – `create_agent` wraps GPT-4o-mini with the Calculator tool and a fitness-focused system prompt.  
2. **Chain** – A `ChatPromptTemplate | ChatOpenAI | StrOutputParser` pipeline is used as a fallback.  
3. **Memory** – `ConversationBufferMemory` stores all messages and injects history into every subsequent prompt.

---

## Dependencies

| Package | Purpose |
|---------|---------|
| `langchain` | Core agent / chain / memory framework |
| `langchain-openai` | OpenAI chat model integration |
| `langchain-community` | Community integrations |
| `langchain-classic` | `ConversationBufferMemory` |
| `python-dotenv` | Load `.env` into environment variables |

---

## Example Session

```
=== FitBuddy AI Fitness Coach ===
1. Run demo conversation
2. Start interactive chat

Enter your choice (1 or 2): 2

You: Hi FitBuddy, I like cardio and yoga.
FitBuddy: That's a great combo! Cardio boosts endurance while yoga improves flexibility and recovery. 💪

You: If I burn 90 calories in 10 minutes, how many in 1 hour?
FitBuddy: That works out to 540 calories in an hour – solid cardio session!

You: What workouts did I say I like?
FitBuddy: You mentioned you enjoy cardio and yoga!

You: quit
Goodbye! Stay fit! 💪
```

---

## License

This project is for educational and personal use. Refer to the course guidelines for any academic submission constraints.
