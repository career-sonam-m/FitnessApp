# =============================================================================
# FitBuddy – AI Fitness Coach Chatbot  |  Streamlit UI
# Built with LangChain + OpenAI GPT-4o-mini + Streamlit
# =============================================================================

import os
import uuid
import streamlit as st
from dotenv import load_dotenv

# Load environment variables (including LangSmith tracing configs)
load_dotenv()

from Langchain_Fitness_ChatBuddy import (
    init_fitbuddy as backend_init_fitbuddy,
    chat_with_fitbuddy,
    get_session_memory,
)

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
# Modern Clean Styling & Layout Fixes
# ─────────────────────────────────────────────────
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;500;600;700;800&display=swap');

    html, body, [class*="css"] {
        font-family: 'Plus Jakarta Sans', -apple-system, sans-serif;
    }

    .stApp,
    [data-testid="stAppViewContainer"],
    [data-testid="stMain"] {
        background:
            radial-gradient(ellipse at 55% 0%, rgba(14, 116, 144, 0.16), transparent 42%),
            #0b1220 !important;
        color: #f8fafc !important;
    }

    .main .block-container {
        max-width: 1020px !important;
        padding: 2.25rem 2.25rem 6rem !important;
    }

    [data-testid="stHeader"] {
        background: rgba(11, 18, 32, 0.88) !important;
        backdrop-filter: blur(12px);
    }

    [data-testid="stHeader"] button,
    [data-testid="stHeader"] svg {
        color: #cbd5e1 !important;
        fill: #cbd5e1 !important;
    }

    .fitbuddy-header {
        position: relative;
        overflow: hidden;
        background:
            radial-gradient(circle at 12% 5%, rgba(34, 211, 238, 0.18), transparent 30%),
            linear-gradient(135deg, #172554 0%, #102033 55%, #0f172a 100%);
        border: 1px solid rgba(125, 211, 252, 0.22);
        border-radius: 24px;
        padding: 32px 34px;
        margin-bottom: 28px;
        text-align: center;
        box-shadow: 0 18px 44px rgba(2, 8, 23, 0.3);
    }

    .fitbuddy-eyebrow {
        color: #67e8f9;
        font-size: 0.72rem;
        font-weight: 800;
        letter-spacing: 0.16em;
        text-transform: uppercase;
        margin-bottom: 8px;
    }

    .fitbuddy-header h1 {
        color: #f8fafc !important;
        font-size: clamp(1.8rem, 4vw, 2.55rem) !important;
        font-weight: 800 !important;
        margin: 0 !important;
        letter-spacing: -0.04em;
    }

    .fitbuddy-header p {
        color: #cbd5e1 !important;
        font-size: 1.02rem !important;
        margin: 10px 0 0 0 !important;
    }

    [data-testid="stMarkdownContainer"] h1,
    [data-testid="stMarkdownContainer"] h2,
    [data-testid="stMarkdownContainer"] h3,
    [data-testid="stMarkdownContainer"] h4 {
        color: #f1f5f9;
        letter-spacing: -0.025em;
    }

    [data-testid="stChatMessage"] {
        background: transparent !important;
        border: none !important;
        padding: 10px 0 !important;
        margin-bottom: 14px !important;
    }

    [data-testid="stChatMessage"]:has([data-testid="chatAvatarIcon-user"]) {
        background: linear-gradient(135deg, #1e3a5f, #172554) !important;
        border: 1px solid rgba(96, 165, 250, 0.24) !important;
        border-radius: 20px 20px 6px 20px !important;
        padding: 15px 20px !important;
        margin-left: 3rem !important;
    }

    [data-testid="stChatMessage"]:has([data-testid="chatAvatarIcon-assistant"]) {
        background: linear-gradient(135deg, #123b50 0%, #0e293e 100%) !important;
        border: 1px solid rgba(45, 212, 191, 0.2) !important;
        border-radius: 20px 20px 20px 6px !important;
        padding: 17px 22px !important;
        margin-right: 2rem !important;
        box-shadow: 0 10px 28px rgba(2, 8, 23, 0.2) !important;
    }

    [data-testid="stChatMessage"] p,
    [data-testid="stChatMessage"] div,
    [data-testid="stChatMessage"] span {
        color: #f8fafc !important;
        font-size: 1rem !important;
        line-height: 1.6 !important;
    }

    .welcome-box {
        position: relative;
        text-align: center;
        padding: 38px 26px;
        background:
            radial-gradient(circle at 50% 0%, rgba(34, 211, 238, 0.1), transparent 55%),
            linear-gradient(145deg, #142238, #101a2a);
        border: 1px solid rgba(148, 163, 184, 0.18);
        border-radius: 24px;
        margin: 18px 0;
        box-shadow: 0 16px 36px rgba(2, 8, 23, 0.2);
    }

    .welcome-box h3 {
        color: #f8fafc !important;
        font-size: 1.4rem;
        margin: 0 0 8px;
    }

    .welcome-box p {
        color: #cbd5e1 !important;
        margin: 0;
    }

    section[data-testid="stSidebar"] {
        background: linear-gradient(180deg, #0c1524 0%, #090d16 100%) !important;
        border-right: 1px solid rgba(148, 163, 184, 0.14) !important;
        padding-top: 1rem !important;
    }

    section[data-testid="stSidebar"] [data-testid="stMarkdownContainer"] p,
    section[data-testid="stSidebar"] [data-testid="stCaptionContainer"] p {
        color: #cbd5e1 !important;
    }

    section[data-testid="stSidebar"] h1,
    section[data-testid="stSidebar"] h2,
    section[data-testid="stSidebar"] h3,
    section[data-testid="stSidebar"] h4,
    section[data-testid="stSidebar"] label {
        color: #f8fafc !important;
    }

    section[data-testid="stSidebar"] .stSelectbox [data-baseweb="select"],
    section[data-testid="stSidebar"] .stSelectbox [data-baseweb="select"] > div {
        background-color: #1e293b !important;
        border: 1px solid #64748b !important;
    }

    section[data-testid="stSidebar"] .stSelectbox [data-baseweb="select"],
    section[data-testid="stSidebar"] .stSelectbox [data-baseweb="select"] *,
    section[data-testid="stSidebar"] .stSelectbox [data-baseweb="select"] input {
        color: #f8fafc !important;
        -webkit-text-fill-color: #f8fafc !important;
    }

    [data-baseweb="popover"] ul,
    [data-baseweb="popover"] li {
        background-color: #1e293b !important;
        color: #f8fafc !important;
    }

    [data-baseweb="popover"] li:hover {
        background-color: #334155 !important;
    }

    section[data-testid="stSidebar"] [data-testid="stBaseButton-secondary"] {
        color: #f8fafc !important;
        background-color: #1e293b !important;
        border-color: #64748b !important;
    }

    section[data-testid="stSidebar"] [data-testid="stBaseButton-secondary"]:hover {
        color: #ffffff !important;
        background-color: #334155 !important;
        border-color: #38bdf8 !important;
    }

    .sidebar-card {
        background: linear-gradient(145deg, #18263a, #111c2d);
        border: 1px solid rgba(148, 163, 184, 0.17);
        border-radius: 18px;
        padding: 15px;
        margin-bottom: 18px;
        box-shadow: 0 10px 24px rgba(0, 0, 0, 0.16);
    }

    .stat-chip {
        display: inline-block;
        background: rgba(8, 145, 178, 0.2);
        border: 1px solid rgba(103, 232, 249, 0.18);
        color: #cffafe !important;
        font-size: 0.8rem;
        font-weight: 700;
        border-radius: 999px;
        padding: 5px 11px;
        margin-right: 6px;
    }

    section[data-testid="stSidebar"] .stSelectbox [data-baseweb="select"] {
        border-radius: 12px !important;
        min-height: 44px;
    }

    section[data-testid="stSidebar"] [data-testid="stBaseButton-primary"],
    section[data-testid="stSidebar"] [data-testid="stBaseButton-secondary"] {
        border-radius: 12px !important;
        min-height: 42px;
        font-weight: 700 !important;
        transition: transform 120ms ease, box-shadow 120ms ease, background 120ms ease;
    }

    section[data-testid="stSidebar"] [data-testid="stBaseButton-primary"] {
        color: #ecfeff !important;
        background: linear-gradient(135deg, #0891b2, #0369a1) !important;
        border: 1px solid rgba(103, 232, 249, 0.35) !important;
        box-shadow: 0 8px 18px rgba(8, 145, 178, 0.2);
    }

    section[data-testid="stSidebar"] [data-testid="stBaseButton-primary"]:hover,
    section[data-testid="stSidebar"] [data-testid="stBaseButton-secondary"]:hover {
        transform: translateY(-1px);
    }

    [data-testid="stBottom"] {
        background: linear-gradient(180deg, rgba(11, 18, 32, 0), #0b1220 24%) !important;
    }

    [data-testid="stBottom"] > div {
        background: linear-gradient(180deg, rgba(11, 18, 32, 0.94), #0b1220) !important;
    }

    [data-testid="stBottomBlockContainer"] {
        padding-top: 0.8rem !important;
        padding-bottom: 1.2rem !important;
    }

    [data-testid="stChatInput"] > div {
        background: #142238;
        border: 1px solid #475569;
        border-radius: 18px;
        box-shadow: 0 14px 34px rgba(0, 0, 0, 0.34);
        padding: 5px 8px;
    }

    [data-testid="stChatInput"] textarea {
        color: #f8fafc !important;
        -webkit-text-fill-color: #f8fafc !important;
        caret-color: #38bdf8 !important;
        background-color: #1e293b !important;
        line-height: 1.5 !important;
    }

    [data-testid="stChatInput"] [data-testid="stChatInputTextArea"],
    [data-testid="stChatInput"] [data-testid="stChatInputTextArea"] > div,
    [data-testid="stChatInput"] div:has(textarea) {
        background-color: #1e293b !important;
    }

    [data-testid="stChatInput"] textarea::placeholder {
        color: #94a3b8 !important;
        -webkit-text-fill-color: #94a3b8 !important;
        opacity: 1 !important;
    }

    [data-testid="stChatInput"] > div:focus-within {
        border-color: #22d3ee;
        box-shadow: 0 0 0 3px rgba(34, 211, 238, 0.16), 0 14px 34px rgba(0, 0, 0, 0.34);
    }

    [data-testid="stChatInput"] button {
        color: #f8fafc !important;
        fill: #ffffff !important;
        background: linear-gradient(135deg, #0891b2, #0369a1) !important;
        border-radius: 12px !important;
        border: 1px solid rgba(103, 232, 249, 0.25) !important;
    }

    [data-testid="stChatInput"] button:disabled {
        color: #cbd5e1 !important;
        background: #334155 !important;
    }

    @media (max-width: 640px) {
        .main .block-container {
            padding: 1.25rem 1rem 5.5rem !important;
        }

        .fitbuddy-header {
            border-radius: 18px;
            padding: 26px 18px;
        }

        [data-testid="stChatMessage"]:has([data-testid="chatAvatarIcon-user"]),
        [data-testid="stChatMessage"]:has([data-testid="chatAvatarIcon-assistant"]) {
            margin-left: 0 !important;
            margin-right: 0 !important;
        }
    }
</style>
""", unsafe_allow_html=True)

# ─────────────────────────────────────────────────
# Session State Setup
# ─────────────────────────────────────────────────
if "session_id" not in st.session_state:
    st.session_state.session_id = str(uuid.uuid4())

if "messages" not in st.session_state:
    st.session_state.messages = []

if "fitbuddy_initialized" not in st.session_state:
    st.session_state.fitbuddy_initialized = False

sample_prompts = [
    (
        "🧮 Calculator challenge",
        "If rowing burns 120 calories every 15 minutes, calculate my burn for 45 minutes. "
        "Then estimate 50 minutes at a 10% lower burn rate and show the arithmetic.",
    ),
    (
        "🏋️ Adapt a workout",
        "Build a 30-minute beginner dumbbell workout for home. I have sensitive knees, "
        "so suggest low-impact moves, modifications, and a warm-up.",
    ),
    (
        "🥗 Convert & plan protein",
        "I weigh 165 lb. Convert that to kilograms, estimate a daily protein target at "
        "1.6 grams per kg, then suggest three vegetarian meal ideas to help reach it.",
    ),
    (
        "🧠 Remember my goals",
        "Please remember this for our next messages: I'm a beginner, want to lose fat, "
        "eat vegetarian, have sensitive knees, and can exercise at home three days a week "
        "for 30 minutes.",
    ),
    (
        "🔁 Test follow-up memory",
        "Using the goals and limitations I just shared, suggest a simple three-day plan "
        "and one vegetarian post-workout snack.",
    ),
]

# ─────────────────────────────────────────────────
# Sidebar Setup
# ─────────────────────────────────────────────────
with st.sidebar:
    st.markdown("""
    <div style="padding: 10px 0 16px;">
        <h2 style="margin:0; color:#f8fafc; font-size:1.4rem;">🏋️ FitBuddy AI</h2>
        <p style="margin:4px 0 0; color:#94a3b8; font-size:0.88rem;">ReAct Agent Fitness Coach</p>
    </div>
    """, unsafe_allow_html=True)

    session_mem = get_session_memory(st.session_state.session_id)
    st.markdown(f"""
    <div class="sidebar-card">
        <div style="display:flex; gap:6px; margin-bottom:8px;">
            <span class="stat-chip">💬 {len(st.session_state.messages)} Msgs</span>
            <span class="stat-chip">🧠 {len(session_mem)} Turns</span>
        </div>
        <div style="font-size:0.8rem; color:#64748b;">Session: {st.session_state.session_id[:8]}…</div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("#### Try a sample")
    selected_sample = st.selectbox(
        "Choose a prompt",
        options=sample_prompts,
        format_func=lambda sample: sample[0],
        label_visibility="collapsed",
        key="selected_sample",
    )
    if st.button("Send sample", key="send_sample", use_container_width=True):
        st.session_state.pending_prompt = selected_sample[1]
        st.rerun()
    st.caption("For the memory demo, send “Remember my goals” before “Test follow-up memory”.")

    if st.button("🗑️ Clear Conversation", type="secondary"):
        st.session_state.messages = []
        get_session_memory(st.session_state.session_id).clear()
        st.rerun()

# ─────────────────────────────────────────────────
# Main App Header
# ─────────────────────────────────────────────────
st.markdown("""
<div class="fitbuddy-header">
    <div class="fitbuddy-eyebrow">Your personal training companion</div>
    <h1>🏋️ FitBuddy AI Coach</h1>
    <p>Practical workouts, nutrition guidance, and accurate fitness calculations.</p>
</div>
""", unsafe_allow_html=True)

# ─────────────────────────────────────────────────
# Initialize Backend Agent
# ─────────────────────────────────────────────────
effective_api_key = os.getenv("OPENAI_API_KEY", "")
effective_base_url = os.getenv("OPENAI_API_BASE", "")

if not effective_api_key:
    st.error("⚠️ **OpenAI API Key missing!** Please check your `.env` file.", icon="🔑")
    st.stop()

if not st.session_state.fitbuddy_initialized:
    try:
        llm, calculator, agent = backend_init_fitbuddy(
            effective_api_key,
            effective_base_url or None,
        )
        st.session_state.llm = llm
        st.session_state.calculator = calculator
        st.session_state.agent = agent
        st.session_state.fitbuddy_initialized = True
    except Exception as e:
        st.error(f"❌ Initialization Failed: {e}")
        st.stop()

# ─────────────────────────────────────────────────
# Render Messages
# ─────────────────────────────────────────────────
if not st.session_state.messages:
    st.markdown("""
    <div class="welcome-box">
        <div style="font-size: 3.5rem; margin-bottom: 12px;">🏋️</div>
        <h3>Welcome to FitBuddy!</h3>
        <p>Ask about workouts, nutrition, or calculations.<br>
        Choose a sample prompt from the sidebar, or type your own message below.</p>
    </div>
    """, unsafe_allow_html=True)
else:
    for msg in st.session_state.messages:
        avatar = "👤" if msg["role"] == "user" else "💪"
        with st.chat_message(msg["role"], avatar=avatar):
            st.markdown(msg["content"])

# ─────────────────────────────────────────────────
# Direct Streamlined Chat Input Flow
# ─────────────────────────────────────────────────
user_message = st.chat_input(
    "Message FitBuddy — ask about training, nutrition, or calculations",
    max_chars=2000,
)
sample_message = st.session_state.pop("pending_prompt", None)
submitted_message = sample_message or user_message

if submitted_message:
    # Display the submitted question before the blocking agent call starts.
    st.session_state.messages.append({"role": "user", "content": submitted_message})
    with st.chat_message("user", avatar="👤"):
        st.markdown(submitted_message)

    with st.chat_message("assistant", avatar="💪"):
        with st.spinner("FitBuddy is thinking..."):
            messages_for_context = st.session_state.messages[:-1]
            response = chat_with_fitbuddy(
                submitted_message,
                st.session_state.agent,
                st.session_state.session_id,
                messages_for_context,
                calculator=st.session_state.calculator,
            )
    st.session_state.messages.append({"role": "assistant", "content": response})
    
    st.rerun()
