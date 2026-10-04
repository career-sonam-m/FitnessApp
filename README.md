# 🏋️ FitBuddy – ReAct Agent AI Fitness Coach

**FitBuddy** is your personal 24/7 AI-powered fitness and nutrition assistant. Built on a 100% **Agentic ReAct Architecture (`create_agent`)**, **OpenAI GPT-4o-mini**, and **LangSmith**, FitBuddy goes beyond static chatbot responses to actively reason, compute math, and remember your personal health journey.

---

### 💡 What is this App for?

FitBuddy is designed to solve common personal training challenges by serving as an intelligent, interactive companion for:

1. **🏋️ Customized Workout & Training Guidance**:
   - Get personalized routine recommendations for strength training, cardio, HIIT, yoga, and active recovery tailored to your fitness level.
2. **🥗 Nutrition & Macro Planning Advice**:
   - Receive meal tips, protein/macro allocation guidance, and dietary recommendations aligned with your fitness objectives (weight loss, muscle gain, maintenance).
3. **🔢 Exact Calorie & Fitness Math Calculations**:
   - Unlike basic LLMs that hallucinate arithmetic, FitBuddy's **ReAct Agent** autonomously invokes a built-in Python **Calculator Tool** to compute exact calorie burns, target heart rate zones, macro splits, and unit conversions (e.g. *lbs to kg* or *burn rate projections*).
4. **🧠 Multi-Turn Goal Memory**:
   - FitBuddy remembers your workout preferences, injuries, and health targets across the conversation so you never have to repeat your goals.
5. **📊 Full Agent Observability**:
   - Built with native **LangSmith** tracing so developers and users can inspect the agent's step-by-step reasoning loop, tool execution inputs/outputs, latency, and token metrics.

---

**Available Interfaces:**
- 🌐 **Streamlit Web App** (`streamlit_app.py`) – Interactive graphical user interface with responsive dark styling and quick prompt buttons.
- 🖥️ **Command-Line Interface** (`Langchain_Fitness_ChatBuddy.py`) – Terminal-based interactive agent loop for developers and command-line execution.

---

## 📚 Key LangChain Concepts & Topics Covered

This project demonstrates modern **LangChain** architecture patterns:

1. **ReAct Agent Architecture (`create_agent`)**:
   - Building a 100% fully agentic tool-calling ReAct agent that loops through reasoning steps to decide whether to call tools (e.g. `Calculator`) or respond directly.
2. **Tools & Tool Wrappers (`Tool`)**:
   - Encapsulating Python functions into LangChain `Tool` objects with natural language descriptions for model tool selection.
3. **LLM Integration (`ChatOpenAI`)**:
   - Initializing Chat Model wrappers with temperature control (`0.7`), specific model routing (`gpt-4o-mini`), API keys, and custom endpoints.
4. **Memory Management (Sliding Window Session Memory)**:
   - Managing multi-turn state across user interactions using sliding window session context formatting.
5. **Observability & Tracing (`LangSmith`)**:
   - Automated tracing of agent decision loops, prompt inputs, tool calls, execution latency, and token consumption using standard environment variables (`LANGSMITH_TRACING="true"`).

---

## 🌟 Features

- 🤖 **100% Agentic ReAct Agent** – Dynamically invokes tools for calorie & arithmetic calculations.
- 🧠 **Multi-Turn Session Memory** – Retains user goal history across turns using a sliding window memory manager.
- 🔢 **Arithmetic Calculator Tool** – Evaluates math and calorie calculations accurately.
- 📊 **LangSmith Observability** – Automatic tracing of runs, agent steps, latency, and token usage metrics.

---

## 📂 Project Structure

```
FitnessApp/
├── Langchain_Fitness_ChatBuddy.py   # Core backend AI engine (ReAct Agent) & CLI script
├── streamlit_app.py                # Streamlit UI application
├── requirements.txt                 # Python dependencies
├── .env                             # Environment config (API keys & tracing settings)
└── README.md                        # Project Documentation
```

---

## ⚙️ Setup & Installation

### 1. Prerequisites
- Python **3.12+**
- OpenAI API key
- LangSmith API key *(for tracing)*

### 2. Virtual Environment Setup

```bash
# Create virtual environment
python -m venv .venv

# Activate environment (Windows PowerShell)
.\.venv\Scripts\Activate.ps1

# Activate environment (macOS / Linux)
source .venv/bin/activate
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

### 4. Environment Configuration (`.env`)

Configure your keys in the `.env` file located at the project root:

```env
OPENAI_API_KEY="sk-proj-your-openai-key"
LANGSMITH_TRACING="true"
LANGSMITH_API_KEY="lsv2_pt_your-langsmith-key"
LANGSMITH_PROJECT="fitness-app"
```

---

## 🚀 Running the Application

### Option 1: Streamlit Web UI (Recommended)

```bash
streamlit run streamlit_app.py
```
*Access the Web UI at http://localhost:8501*

### Option 2: Command-Line (CLI) Chatbot

```bash
python Langchain_Fitness_ChatBuddy.py
```

### Sample questions to try

The Streamlit app includes clickable samples for the calculator, workout and nutrition advice, and multi-turn memory. To test memory, send the **Remember my goals** prompt first, then send **Test follow-up memory** in the same conversation.

You can also try:

- “If rowing burns 120 calories every 15 minutes, calculate my burn for 45 minutes. Then estimate 50 minutes at a 10% lower burn rate and show the arithmetic.”
- “I weigh 165 lb. Convert that to kilograms, estimate a daily protein target at 1.6 grams per kg, then suggest three vegetarian meal ideas to help reach it.”
- “Build a 30-minute beginner dumbbell workout for home. I have sensitive knees, so suggest low-impact moves, modifications, and a warm-up.”

---

## 🔍 Observing Agent Execution in LangSmith

1. Ensure `LANGSMITH_TRACING="true"` is set in your `.env`.
2. Start the Streamlit app or CLI and ask a tool-requiring prompt:
   > *"If I burn 120 calories in 15 minutes of rowing, how many calories will I burn in 45 minutes?"*
3. Log into **[smith.langchain.com](https://smith.langchain.com)**.
4. Select the **`fitness-app`** project to view the agent trace showing:
   - Agent reasoning steps
   - Tool call inputs/outputs (`Calculator`)
   - Model latency and token usage metrics
