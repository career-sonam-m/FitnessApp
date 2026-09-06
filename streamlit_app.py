# =============================================================================
# FitBuddy – AI Fitness Coach Chatbot  |  Streamlit UI
# Built with LangChain + OpenAI GPT-4o-mini + Streamlit
# =============================================================================

import os
import uuid
import streamlit as st
from dotenv import load_dotenv

from langchain_openai import ChatOpenAI
from langchain_core.tools import Tool
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser

# ─────────────────────────────────────────────────
# Page Configuration
# ─────────────────────────────────────────────────
st.set_page_config(
    page_title="FitBuddy – AI Fitness Coach",
    page_icon="💪",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ─────────────────────────────────────────────────
# Custom CSS – enhanced modern dark fitness theme
# ─────────────────────────────────────────────────
st.markdown("""
<style>
    /* ── Google Fonts ─────────────────────────────── */
    @import url('https://fonts.googleapis.com/css2?family=Poppins:wght@400;500;600;700;800&display=swap');

    html, body, [class*="css"] {
        font-family: 'Poppins', sans-serif;
    }

    /* ── Light background ──────────────────────────── */
    .stApp {
        background: #f4f6fb !important;
        min-height: 100vh;
    }

    /* Force main content area to be clean and readable */
    .main .block-container {
        background: #ffffff !important;
        box-shadow: 0 18px 45px rgba(15, 23, 42, 0.08) !important;
        border-radius: 24px !important;
        padding: 28px !important;
        border: 1px solid rgba(226, 232, 240, 0.85) !important;
    }

    /* ── Header banner with glow effect ────────────── */
    .fitbuddy-header {
        background: linear-gradient(135deg, #ff7a71 0%, #ffb37f 100%);
        border-radius: 18px;
        padding: 26px 30px;
        margin-bottom: 24px;
        text-align: center;
        box-shadow: 0 20px 60px rgba(15, 23, 42, 0.08);
    }

    .fitbuddy-header::before {
        display: none;
    }

    @keyframes shimmer {
        from { opacity: 0.9; }
        to { opacity: 0.9; }
    }

    .fitbuddy-header h1 {
        color: #ffffff;
        font-size: 2.8rem;
        font-weight: 800;
        margin: 0;
        letter-spacing: 2px;
        text-shadow: 2px 2px 4px rgba(0,0,0,0.2);
        position: relative;
        z-index: 1;
    }

    .fitbuddy-header p {
        color: rgba(255,255,255,0.95);
        font-size: 1.1rem;
        margin: 10px 0 0;
        font-weight: 500;
        position: relative;
        z-index: 1;
    }

    /* ── Chat message bubbles ───────────────────────── */

    /* Base reset */
    [data-testid="stChatMessage"] {
        border-radius: 20px !important;
        padding: 14px 20px !important;
        margin: 10px 4px !important;
    }

    /* ── User bubble — soft coral ─────────────────── */
    [data-testid="stChatMessage"]:has([data-testid="chatAvatarIcon-user"]) {
        background: #ffe5e8 !important;
        border-radius: 20px 20px 5px 20px !important;
        margin: 10px 0 10px 64px !important;
        box-shadow: 0 8px 20px rgba(255, 99, 132, 0.15) !important;
        border: 1px solid rgba(255, 99, 132, 0.2) !important;
        animation: none !important;
    }

    [data-testid="stChatMessage"]:has([data-testid="chatAvatarIcon-user"]) *,
    [data-testid="stChatMessage"]:has([data-testid="chatAvatarIcon-user"]) p,
    [data-testid="stChatMessage"]:has([data-testid="chatAvatarIcon-user"]) span,
    [data-testid="stChatMessage"]:has([data-testid="chatAvatarIcon-user"]) li,
    [data-testid="stChatMessage"]:has([data-testid="chatAvatarIcon-user"]) strong,
    [data-testid="stChatMessage"]:has([data-testid="chatAvatarIcon-user"]) em,
    [data-testid="stChatMessage"]:has([data-testid="chatAvatarIcon-user"]) div {
        color: #1f2937 !important;
        -webkit-text-fill-color: #1f2937 !important;
        font-size: 1rem !important;
        line-height: 1.7 !important;
    }

    /* ── Assistant bubble — soft white card ───────── */
    [data-testid="stChatMessage"]:has([data-testid="chatAvatarIcon-assistant"]) {
        background: #f8fafc !important;
        border-radius: 20px 20px 20px 5px !important;
        margin: 10px 60px 10px 0 !important;
        border: 1px solid rgba(148, 163, 184, 0.24) !important;
        box-shadow: 0 8px 22px rgba(15, 23, 42, 0.06) !important;
        animation: none !important;
    }

    /* Assistant text — dark charcoal, easy to read */
    [data-testid="stChatMessage"]:has([data-testid="chatAvatarIcon-assistant"]) *,
    [data-testid="stChatMessage"]:has([data-testid="chatAvatarIcon-assistant"]) p,
    [data-testid="stChatMessage"]:has([data-testid="chatAvatarIcon-assistant"]) span,
    [data-testid="stChatMessage"]:has([data-testid="chatAvatarIcon-assistant"]) li,
    [data-testid="stChatMessage"]:has([data-testid="chatAvatarIcon-assistant"]) div {
        color: #1a1a2e !important;
        -webkit-text-fill-color: #1a1a2e !important;
        font-size: 1rem !important;
        line-height: 1.8 !important;
    }

    /* Bold — coral red accent */
    [data-testid="stChatMessage"]:has([data-testid="chatAvatarIcon-assistant"]) strong {
        color: #c0392b !important;
        -webkit-text-fill-color: #c0392b !important;
        font-weight: 700 !important;
    }

    /* Italic */
    [data-testid="stChatMessage"]:has([data-testid="chatAvatarIcon-assistant"]) em {
        color: #555 !important;
        -webkit-text-fill-color: #555 !important;
        font-style: italic !important;
    }

    /* Headings */
    [data-testid="stChatMessage"]:has([data-testid="chatAvatarIcon-assistant"]) h1,
    [data-testid="stChatMessage"]:has([data-testid="chatAvatarIcon-assistant"]) h2,
    [data-testid="stChatMessage"]:has([data-testid="chatAvatarIcon-assistant"]) h3,
    [data-testid="stChatMessage"]:has([data-testid="chatAvatarIcon-assistant"]) h4 {
        color: #c0392b !important;
        -webkit-text-fill-color: #c0392b !important;
        font-weight: 700 !important;
        margin-top: 14px !important;
        margin-bottom: 8px !important;
    }

    /* Lists */
    [data-testid="stChatMessage"]:has([data-testid="chatAvatarIcon-assistant"]) ul,
    [data-testid="stChatMessage"]:has([data-testid="chatAvatarIcon-assistant"]) ol {
        margin-left: 22px !important;
        padding-left: 0 !important;
    }

    /* Inline code */
    [data-testid="stChatMessage"]:has([data-testid="chatAvatarIcon-assistant"]) code {
        background: #fff0f0 !important;
        color: #c0392b !important;
        -webkit-text-fill-color: #c0392b !important;
        padding: 2px 8px !important;
        border-radius: 6px !important;
        font-size: 0.92rem !important;
        font-family: 'Courier New', monospace !important;
    }

    /* ── Avatar icons ────────────────────────────────── */
    [data-testid="chatAvatarIcon-user"] {
        background: linear-gradient(135deg, #ff6b6b, #feca57) !important;
        border-radius: 50% !important;
        box-shadow: 0 4px 12px rgba(255,107,107,0.4) !important;
    }

    [data-testid="chatAvatarIcon-assistant"] {
        background: linear-gradient(135deg, #feca57, #ff6b6b) !important;
        border-radius: 50% !important;
        box-shadow: 0 4px 12px rgba(254,202,87,0.4) !important;
    }

    /* ── st.chat_input box ───────────────────────────── */
    [data-testid="stChatInput"] textarea {
        background: #ffffff !important;
        color: #1a1a2e !important;
        -webkit-text-fill-color: #1a1a2e !important;
        border: 2px solid #ff6b6b !important;
        border-radius: 16px !important;
        font-size: 1rem !important;
        font-family: 'Poppins', sans-serif !important;
    }

    [data-testid="stChatInput"] textarea:focus {
        box-shadow: 0 0 0 3px rgba(255,107,107,0.2) !important;
    }

    [data-testid="stChatInput"] textarea::placeholder {
        color: #aaa !important;
        -webkit-text-fill-color: #aaa !important;
    }

    @keyframes slideInRight {
        from { opacity: 0; transform: translateX(30px); }
        to { opacity: 1; transform: translateX(0); }
    }

    @keyframes slideInLeft {
        from { opacity: 0; transform: translateX(-30px); }
        to { opacity: 1; transform: translateX(0); }
    }

    /* ── Sidebar — clean light style ─────────────── */
    section[data-testid="stSidebar"] {
        background: #ffffff !important;
        border-right: 1px solid rgba(226, 232, 240, 0.9) !important;
        width: 300px !important;
        min-width: 280px !important;
        padding: 18px !important;
    }

    section[data-testid="stSidebar"] * {
        color: #1a1a2e !important;
        -webkit-text-fill-color: #1a1a2e !important;
    }

    section[data-testid="stSidebar"] h1,
    section[data-testid="stSidebar"] h2,
    section[data-testid="stSidebar"] h3 {
        color: #1f2937 !important;
        -webkit-text-fill-color: #1f2937 !important;
    }

    .sidebar-card {
        background: #f8fafc;
        border: 1px solid rgba(148, 163, 184, 0.18);
        border-radius: 16px;
        padding: 16px;
        margin-bottom: 14px;
        box-shadow: 0 10px 22px rgba(15, 23, 42, 0.05);
    }

    .sidebar-section {
        margin-bottom: 16px;
    }

    .sidebar-card p {
        margin: 8px 0 0;
        color: #475569 !important;
        font-size: 0.92rem;
        line-height: 1.5;
    }

    .sidebar-card .stat-chip {
        margin-bottom: 0 !important;
    }

    .quick-prompt-button button {
        min-height: 46px !important;
        padding: 10px 12px !important;
        font-size: 0.9rem !important;
        line-height: 1.3 !important;
        text-align: left !important;
    }

    .stSidebar .stButton button {
        background: linear-gradient(135deg, #ff8b7b 0%, #ffbb96 100%) !important;
        color: #1f2937 !important;
        border-radius: 14px !important;
        border: 1px solid rgba(255, 255, 255, 0.4) !important;
    }

    .stApp {
        max-width: 1100px;
        margin-left: auto;
        margin-right: auto;
    }

    .stat-chip {
        display: inline-block;
        background: linear-gradient(135deg, #ff6b6b, #feca57);
        color: #fff;
        font-size: 0.8rem;
        font-weight: 700;
        border-radius: 25px;
        padding: 6px 16px;
        margin: 6px 6px 0 0;
        box-shadow: 0 4px 15px rgba(255,107,107,0.3);
        transition: transform 0.2s, box-shadow 0.2s;
    }

    .stat-chip:hover {
        transform: translateY(-2px);
        box-shadow: 0 6px 20px rgba(255,107,107,0.4);
    }

    /* ── Enhanced input box ───────────────────────── */
    .stTextInput > div > div > input,
    .stTextInput > div > div > input:focus,
    .stTextInput > div > div > input::placeholder {
        color: #000000 !important;
        background: rgba(255,255,255,0.9) !important;
        border: 2px solid rgba(255,255,255,0.5) !important;
        border-radius: 16px !important;
        padding: 16px 20px !important;
        font-size: 1rem !important;
        backdrop-filter: blur(10px);
        transition: all 0.3s ease !important;
    }

    .stTextInput > div > div > input:focus {
        border-color: #ff6b6b !important;
        box-shadow: 0 0 0 4px rgba(255,107,107,0.2),
                    0 0 20px rgba(255,107,107,0.3) !important;
        background: rgba(255,255,255,1.0) !important;
    }

    .stTextInput > div > div > input::placeholder {
        color: rgba(0,0,0,0.5) !important;
    }

    /* ── Ensure text visibility in all states ──────── */
    .stTextInput input {
        color: #000000 !important;
        -webkit-text-fill-color: #000000 !important;
    }

    .stTextInput input::placeholder {
        color: rgba(0,0,0,0.5) !important;
        -webkit-text-fill-color: rgba(0,0,0,0.5) !important;
    }

    /* ── Enhanced buttons ─────────────────────────── */
    .stButton > button {
        background: linear-gradient(135deg, #ff7a6e 0%, #ffbc88 100%) !important;
        color: #1f2937 !important;
        border: none !important;
        border-radius: 14px !important;
        padding: 12px 22px !important;
        font-weight: 600 !important;
        font-size: 0.96rem !important;
        transition: all 0.25s ease !important;
        width: 100%;
        box-shadow: 0 10px 24px rgba(255, 122, 110, 0.18);
        text-transform: none;
        letter-spacing: 0.4px;
    }

    .stButton > button:hover {
        transform: translateY(-3px) scale(1.02) !important;
        box-shadow: 0 10px 30px rgba(255,107,107,0.5) !important;
    }

    .stButton > button:active {
        transform: translateY(-1px) scale(0.98) !important;
    }

    /* ── Divider ──────────────────────────────────── */
    hr {
        border-color: #ffd6d6 !important;
        border-style: solid !important;
    }

    /* ── Welcome banner ───────────────────────────── */
    .welcome-box {
        text-align: center;
        padding: 60px 30px;
        color: #555;
        background: #ffffff;
        border-radius: 24px;
        border: 2px dashed #ffd6d6;
        margin: 20px 0;
        box-shadow: 0 4px 20px rgba(255,107,107,0.08);
    }

    .welcome-box .icon {
        font-size: 5rem;
        margin-bottom: 20px;
        animation: bounce 2s infinite;
    }

    @keyframes bounce {
        0%, 100% { transform: translateY(0); }
        50% { transform: translateY(-10px); }
    }

    .welcome-box h3 {
        color: #1a1a2e !important;
        margin-bottom: 12px;
        font-size: 1.8rem;
        font-weight: 700;
    }

    .welcome-box p {
        font-size: 1rem;
        line-height: 1.7;
        color: #555;
    }

    /* ── Scrollbar styling ─────────────────────────── */
    ::-webkit-scrollbar {
        width: 10px;
    }

    ::-webkit-scrollbar-track {
        background: rgba(255,255,255,0.05);
    }

    ::-webkit-scrollbar-thumb {
        background: linear-gradient(135deg, #ff6b6b, #feca57);
        border-radius: 5px;
    }

    ::-webkit-scrollbar-thumb:hover {
        background: linear-gradient(135deg, #feca57, #ff6b6b);
    }

    /* ── Footer styling ───────────────────────────── */
    .footer {
        text-align: center;
        padding: 20px;
        color: rgba(255,255,255,0.4);
        font-size: 0.85rem;
        border-top: 1px solid rgba(255,255,255,0.1);
        margin-top: 40px;
    }
</style>
""", unsafe_allow_html=True)


# ─────────────────────────────────────────────────
# Load environment variables
# ─────────────────────────────────────────────────
load_dotenv()


# ============================================================================
# SESSION MEMORY MANAGEMENT (from capstone project)
# ============================================================================

_SESSION_MEMORY: dict[str, list[tuple[str, str]]] = {}


def get_session_memory(session_id: str) -> list[tuple[str, str]]:
    """Retrieve conversation memory for a session."""
    return _SESSION_MEMORY.setdefault(session_id, [])


def append_memory(
    session_id: str, *, user_text: str, assistant_summary: str, max_turns: int = 6
) -> None:
    """Append turn to session memory, maintaining a sliding window."""
    mem = get_session_memory(session_id)
    mem.append((user_text, assistant_summary))
    if len(mem) > max_turns:
        del mem[0 : len(mem) - max_turns]


def memory_context(session_id: str) -> str:
    """Format session memory as context string for LLM."""
    mem = get_session_memory(session_id)
    if not mem:
        return ""
    lines = []
    for i, (u, a) in enumerate(mem[-6:], start=1):
        lines.append(f"Turn {i} user: {u}")
        lines.append(f"Turn {i} assistant: {a}")
    return "\n".join(lines)


def format_conversation_history(
    conversation_history: list[dict[str, str]] | None, max_messages: int = 8
) -> str:
    """Format recent UI chat history for prompt context."""
    if not conversation_history:
        return ""

    lines = []
    for item in conversation_history[-max_messages:]:
        role = str(item.get("role", "")).strip().lower()
        content = str(item.get("content", "")).strip()
        if role not in {"user", "assistant"} or not content:
            continue
        lines.append(f"{role.capitalize()}: {content}")
    return "\n".join(lines)


# ─────────────────────────────────────────────────
# Session-state initialisation (persists across reruns)
# ─────────────────────────────────────────────────
if "session_id" not in st.session_state:
    st.session_state.session_id = str(uuid.uuid4())

if "messages" not in st.session_state:
    st.session_state.messages = []          # list of {"role": "user"/"assistant", "content": "..."}

if "user_input_message" not in st.session_state:
    st.session_state.user_input_message = ""

if "pending_input" not in st.session_state:
    st.session_state.pending_input = ""


# ─────────────────────────────────────────────────
# Initialise LLM, tools, and agent (once per session)
# ─────────────────────────────────────────────────
@st.cache_resource(show_spinner=False)
def init_fitbuddy(api_key: str, base_url: str | None):
    """
    Creates and caches the LLM, calculator tool, prompt chain, and agent.
    Re-runs only when the API key or base URL changes.
    """
    llm = ChatOpenAI(
        temperature=0.7,
        model="gpt-4o-mini",
        api_key=api_key,
        base_url=base_url or None,
    )

    # ── Calculator tool ────────────────────────────
    def simple_calculator(expression: str) -> str:
        try:
            return str(eval(expression))
        except Exception:
            return "Invalid math expression."

    calculator = Tool(
        name="Calculator",
        func=simple_calculator,
        description="Performs basic arithmetic, e.g., '3 * 4 + 2'.",
    )

    # ── Fallback chain ─────────────────────────────
    prompt = ChatPromptTemplate.from_messages([
        ("system",
         "You are FitBuddy, a friendly AI fitness coach. "
         "Remember what the user says about their workouts or goals. "
         "Use the calculator tool when math is required. "
         "Give helpful fitness advice in complete responses, ideally 2–3 sentences with practical next steps."),
        ("system", "Previous conversation:\n{chat_history}"),
        ("human", "{input}"),
    ])
    chain = prompt | llm | StrOutputParser()

    return llm, calculator, chain




def chat_with_fitbuddy(
    user_input: str,
    chain,
    session_id: str,
    conversation_history: list[dict[str, str]] | None,
    calculator,
) -> str:
    """
    Sends user_input to FitBuddy and returns its response.
    Uses only the main chain path with conversation history.
    """
    conversation_ctx = format_conversation_history(conversation_history)
    memory_ctx = memory_context(session_id)

    try:
        # Combine both conversation history and memory context
        context_parts = []
        if memory_ctx:
            context_parts.append(f"Session Memory:\n{memory_ctx}")
        if conversation_ctx:
            context_parts.append(f"Recent Chat:\n{conversation_ctx}")
        full_context = "\n\n".join(context_parts)

        response = chain.invoke({"input": user_input, "chat_history": full_context})
        response_text = str(response).strip() if response is not None else ""
        if not response_text:
            raise ValueError("Empty response from chain")

        append_memory(session_id, user_text=user_input, assistant_summary=response_text)
        return response_text
    except Exception as e:
        print(f"DEBUG: Chain error: {e}")
        return f"Sorry, I couldn't process that request. Please try again."
# ─────────────────────────────────────────────────
with st.sidebar:
    st.markdown("""
    <div style="padding: 16px 0 10px; text-align: left;">
        <h2 style="margin: 0; color: #1f2937;">FitBuddy</h2>
        <p style="margin: 6px 0 0; color: #475569; font-size: 0.95rem;">Quick fitness guidance and planning.</p>
    </div>
    """, unsafe_allow_html=True)

    session_mem = get_session_memory(st.session_state.session_id)
    st.markdown(f"""
    <div class="sidebar-card sidebar-section">
        <div style="display: flex; flex-wrap: wrap; gap: 8px;">
            <span class="stat-chip">💬 {len(st.session_state.messages)} msgs</span>
            <span class="stat-chip">🧠 {len(session_mem)} turns</span>
        </div>
        <p>Session ID: {st.session_state.session_id[:8]}…</p>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("""
    <div class="sidebar-card sidebar-section">
        <div style="font-weight: 700; margin-bottom: 12px; color: #1f2937;">⚡ Quick Prompts</div>
    """, unsafe_allow_html=True)

    quick_prompts = [
        {"icon": "🏃", "text": "30-min workout plan"},
        {"icon": "🔥", "text": "Calories burned running"},
        {"icon": "🥗", "text": "Recovery meal ideas"},
        {"icon": "📅", "text": "Weekly workout schedule"},
    ]
    cols = st.columns(2)
    for idx, qp in enumerate(quick_prompts):
        with cols[idx % 2]:
            if st.button(f"{qp['icon']} {qp['text']}", key=f"qp_{idx}", use_container_width=True):
                st.session_state["user_input_message"] = qp['text']
                st.session_state.pending_input = ""
                st.experimental_rerun()

    st.markdown("""
        <p style="margin: 10px 0 0; color: #475569; font-size: 0.9rem;">Tap a prompt to ask FitBuddy quickly.</p>
    </div>
    """, unsafe_allow_html=True)

    with st.expander("Actions", expanded=False):
        if st.button("Clear chat", key="clear_btn", use_container_width=True):
            st.session_state.messages = []
            st.session_state.session_id = str(uuid.uuid4())
            st.experimental_rerun()
        if st.button("Reset memory", key="reset_memory_btn", use_container_width=True):
            st.session_state.session_id = str(uuid.uuid4())
            st.success("Memory reset!")
            st.experimental_rerun()

    st.markdown("""
    <div style="padding-top: 12px; color: #64748b; font-size: 0.9rem;">
        Powered by GPT-4o-mini • Clean coaching UI
    </div>
    """, unsafe_allow_html=True)


# ─────────────────────────────────────────────────
# Main Page – Header
# ─────────────────────────────────────────────────
st.markdown("""
<div class="fitbuddy-header">
    <h1>💪 FitBuddy</h1>
    <p>Your AI-powered personal fitness coach — ask me anything about workouts, nutrition, and goals!</p>
</div>
""", unsafe_allow_html=True)


# ─────────────────────────────────────────────────
# Initialise FitBuddy components (lazy initialization)
# ─────────────────────────────────────────────────
effective_api_key = os.getenv("OPENAI_API_KEY", "")
effective_base_url = os.getenv("OPENAI_API_BASE", "")

if not effective_api_key:
    st.error("⚠️ **OpenAI API Key not found!** Please set the `OPENAI_API_KEY` environment variable or add it to your `.env` file.", icon="🔑")
    st.stop()

# Lazy initialization - only load when first message is sent
if "fitbuddy_initialized" not in st.session_state:
    st.session_state.fitbuddy_initialized = False
    st.session_state.llm = None
    st.session_state.calculator = None
    st.session_state.chain = None
    st.session_state.agent = None


# ─────────────────────────────────────────────────
# Chat display area
# ─────────────────────────────────────────────────
chat_container = st.container()

with chat_container:
    if not st.session_state.messages:
        st.markdown("""
        <div class="welcome-box">
            <div class="icon">🏋️</div>
            <h3>Hey there, I'm FitBuddy!</h3>
            <p>Ask me about workouts, nutrition, calorie math, or your fitness goals.<br>
            Use the <b>Quick Prompts</b> in the sidebar to get started instantly.</p>
            <div style="margin-top: 20px; font-size: 0.9rem; opacity: 0.7;">
                ✨ Powered by GPT-4o-mini<br>
                💬 Conversation memory enabled<br>
                🔢 Built-in calculator for fitness math
            </div>
        </div>
        """, unsafe_allow_html=True)
    else:
        for msg in st.session_state.messages:
            if msg["role"] == "user":
                with st.chat_message("user", avatar="👤"):
                    st.markdown(msg["content"])
            else:
                with st.chat_message("assistant", avatar="💪"):
                    st.markdown(msg["content"])


# ─────────────────────────────────────────────────
# Chat input area
with st.container():
    user_message = st.chat_input(
        "Ask FitBuddy anything about workouts, nutrition, or fitness math...",
        key="fitbuddy_input",
    )
    if user_message:
        st.session_state.pending_input = user_message
        st.session_state.user_input_message = ""
        st.experimental_rerun()

# ─────────────────────────────────────────────────
# Process pending input (survives the rerun caused by clear_on_submit)
if st.session_state.pending_input or st.session_state.user_input_message:
    user_text = st.session_state.pending_input or st.session_state.user_input_message
    st.session_state.pending_input = ""
    st.session_state.user_input_message = ""

    print(f"DEBUG: Processing input: {user_text}")
    print(f"DEBUG: Current messages count: {len(st.session_state.messages)}")

    # Initialize FitBuddy on first message (lazy loading)
    if not st.session_state.fitbuddy_initialized:
        print("DEBUG: Initializing FitBuddy...")
        with st.spinner("🚀 Initializing FitBuddy (first time only)…"):
            try:
                llm, calculator, chain = init_fitbuddy(
                    effective_api_key,
                    effective_base_url or None,
                )
                st.session_state.llm = llm
                st.session_state.calculator = calculator
                st.session_state.chain = chain
                st.session_state.fitbuddy_initialized = True
                print("DEBUG: FitBuddy initialized successfully")
            except Exception as e:
                print(f"DEBUG: FitBuddy initialization failed: {e}")
                st.error(f"❌ Failed to initialise FitBuddy: {e}")
                st.stop()

    # Add user message to state
    st.session_state.messages.append({"role": "user", "content": user_text})
    print(f"DEBUG: Added user message. Total messages: {len(st.session_state.messages)}")

    # Get FitBuddy response with enhanced spinner
    with st.spinner("💪 FitBuddy is thinking…"):
        print("DEBUG: Calling chat_with_fitbuddy...")
        # Pass messages WITHOUT the current user message to avoid duplication
        messages_for_context = st.session_state.messages[:-1]
        response = chat_with_fitbuddy(
            user_text,
            st.session_state.chain,
            st.session_state.session_id,
            messages_for_context,
            st.session_state.calculator,
        )
        print(f"DEBUG: Got response: {response[:100] if response else 'None'}...")

    # Add assistant message to state
    st.session_state.messages.append({"role": "assistant", "content": response})
    print(f"DEBUG: Added assistant message. Total messages: {len(st.session_state.messages)}")

    st.rerun()

# ─────────────────────────────────────────────────
# Footer
# ─────────────────────────────────────────────────
st.markdown("""
<div class="footer">
    <p style="margin: 0;">FitBuddy AI Fitness Coach · Built with ❤️ using LangChain & GPT-4o-mini</p>
</div>
""", unsafe_allow_html=True)
