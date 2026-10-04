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
├── .gitignore                       # Excludes local secrets and virtual environment
├── .env                             # Optional local-only environment config (never commit)
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
LANGSMITH_ENDPOINT="https://apac.api.smith.langchain.com"
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

## 🌐 Live Demo

FitBuddy is deployed on Streamlit Community Cloud, so **anyone can use it directly in the browser with no installation or API key**:

**https://fitnessapp-h7klc2mc92mjeifcy7qnf5.streamlit.app/**

Source code: https://github.com/career-sonam-m/FitnessApp

> If the app has been idle, Streamlit may show a "wake up" button. Click it and wait a few seconds.

## ☁️ Deploying on Streamlit Community Cloud

Streamlit Community Cloud deploys this app from a GitHub repository and gives it a public URL that you can share. Visitors can use the app, but requests use **your configured OpenAI API key** and may incur charges on your OpenAI account.

### 1. Push the project to GitHub

Create a GitHub repository and push the project files. Do **not** upload `.env`, `.venv`, or API keys. The repository should include at least:

```text
Langchain_Fitness_ChatBuddy.py
streamlit_app.py
requirements.txt
README.md
```

### 2. Create the Streamlit app

1. Sign in at [share.streamlit.io](https://share.streamlit.io/) with GitHub.
2. Select **Create app**, then choose your repository, branch, and `streamlit_app.py` as the main file.
3. In the app's advanced settings, select **Python 3.12**.
4. Before launching, open the app's **Settings → Secrets** and add the TOML below, replacing the example values with your own:

```toml
OPENAI_API_KEY = "your-openai-api-key"
LANGSMITH_TRACING = "true"
LANGSMITH_API_KEY = "your-langsmith-api-key"
LANGSMITH_PROJECT = "fitness-app"
LANGSMITH_ENDPOINT = "https://apac.api.smith.langchain.com"
```

`LANGSMITH_API_KEY`, `LANGSMITH_PROJECT`, and `LANGSMITH_ENDPOINT` are optional if you do not need tracing. For a LangSmith workspace outside APAC, use its [regional endpoint](https://docs.langchain.com/langsmith/trace-with-langchain).

5. Save the secrets and deploy. Once the app reports that it is running, open its **App URL** and send a message to verify it.
6. Use **Share** in Streamlit Community Cloud to copy the URL for other people.

The app reads credentials from Streamlit Cloud Secrets (or a local `.env` file when running locally). Never commit your secrets or put them in the source code. Since the app uses your API key for every visitor, monitor usage and disable or restrict the app if you need to control costs.

### Sample questions to try

The Streamlit app includes clickable samples for the calculator, workout and nutrition advice, and multi-turn memory. To test memory, send the **Remember my goals** prompt first, then send **Test follow-up memory** in the same conversation.

You can also try:

- “If rowing burns 120 calories every 15 minutes, calculate my burn for 45 minutes. Then estimate 50 minutes at a 10% lower burn rate and show the arithmetic.”
- “I weigh 165 lb. Convert that to kilograms, estimate a daily protein target at 1.6 grams per kg, then suggest three vegetarian meal ideas to help reach it.”
- “Build a 30-minute beginner dumbbell workout for home. I have sensitive knees, so suggest low-impact moves, modifications, and a warm-up.”

---

## 🔍 Observing Agent Execution in LangSmith

### Setting up LangSmith

1. Sign up at **[smith.langchain.com](https://smith.langchain.com)** (free tier is enough).
2. Go to **Settings → API Keys** and create a key (starts with `lsv2_`). Put it in `LANGSMITH_API_KEY`.
3. Set `LANGSMITH_TRACING="true"` and a project name in `LANGSMITH_PROJECT` (it is created automatically on the first trace).
4. **Region matters:** if your LangSmith URL is `apac.smith.langchain.com` (or `eu.smith.langchain.com`), set `LANGSMITH_ENDPOINT` to `https://apac.api.smith.langchain.com` (or `https://eu.api.smith.langchain.com`). US accounts can omit it. A wrong region causes `403 Forbidden` errors in the logs and no traces appear.
5. Restart the app after editing `.env`, since it is read only at startup.
6. On Streamlit Community Cloud, put the same keys in **Secrets** (see the deployment section above).

### Viewing traces

1. Ensure `LANGSMITH_TRACING="true"` is set in your `.env`.
2. Start the Streamlit app or CLI and ask a tool-requiring prompt:
   > *"If I burn 120 calories in 15 minutes of rowing, how many calories will I burn in 45 minutes?"*
3. Log into **[smith.langchain.com](https://smith.langchain.com)**.
4. Select the **`fitness-app`** project to view the agent trace showing:
   - Agent reasoning steps
   - Tool call inputs/outputs (`Calculator`)
   - Model latency and token usage metrics
