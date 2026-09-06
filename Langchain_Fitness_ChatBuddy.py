# =============================================================================
# FitBuddy – AI Fitness Coach Chatbot
# Built with LangChain + OpenAI GPT-4o-mini
# =============================================================================

# ─────────────────────────────────────────────────
# STEP 1: Import Required Libraries
# ─────────────────────────────────────────────────
import os                                            # For reading environment variables
from dotenv import load_dotenv                       # For loading .env file variables into the environment

# LangChain OpenAI integration – wraps GPT-4o-mini as a chat model
from langchain_openai import ChatOpenAI

# ConversationBufferMemory keeps the entire chat history in memory (not summarised)
from langchain_classic.memory import ConversationBufferMemory

# Tool – wraps a plain Python function so the LangChain agent can call it
from langchain_core.tools import Tool

# ChatPromptTemplate – structures the system prompt + conversation history + user query
from langchain_core.prompts import ChatPromptTemplate

# create_agent – builds a ReAct-style agent that can decide when to use tools
from langchain.agents import create_agent

# Message types used when passing structured chat history to the model
from langchain_core.messages import SystemMessage, HumanMessage

# RunnablePassthrough – passes input data through unchanged in a chain
from langchain_core.runnables import RunnablePassthrough

# StrOutputParser – converts the model's AIMessage object into a plain string
from langchain_core.output_parsers import StrOutputParser


# ─────────────────────────────────────────────────
# STEP 2: Load API Credentials from .env File
# ─────────────────────────────────────────────────
load_dotenv()  # Reads the .env file and sets all key=value pairs as environment variables

openai_api_key = os.getenv("OPENAI_API_KEY")  # Retrieve the OpenAI key safely (returns None if missing)

# Initialise the LLM (Large Language Model)
# - temperature=0.7  → slightly creative / conversational responses (0 = deterministic, 1 = very creative)
# - model            → GPT-4o-mini is fast and cost-effective for chat use-cases
# - api_key          → passed explicitly for clarity (LangChain also reads it from the environment)
# - base_url         → supports custom OpenAI-compatible endpoints (e.g., Azure, local proxies)
llm = ChatOpenAI(
    temperature=0.7,
    model="gpt-4o-mini",
    api_key=os.environ.get("OPENAI_API_KEY"),    # Use .get() so it returns None instead of raising an error
    base_url=os.getenv("OPENAI_API_BASE")        # Optional: override the default https://api.openai.com/v1
)


# ─────────────────────────────────────────────────
# STEP 3: Define the Calculator Tool
# ─────────────────────────────────────────────────
def simple_calculator(expression: str) -> str:
    """
    Safely evaluates a basic arithmetic expression string and returns the result.

    Args:
        expression (str): A math expression such as '90 * 6' or '3 * 4 + 2'.

    Returns:
        str: The numeric result as a string, or an error message if evaluation fails.
    """
    try:
        # eval() computes the result of the arithmetic string.
        # WARNING: eval() can be unsafe with untrusted input; restrict to simple math only.
        return str(eval(expression))
    except Exception:
        return "Invalid math expression."

# Wrap the Python function as a LangChain Tool so the agent can discover and invoke it.
# - name        → how the agent refers to the tool in its reasoning
# - func        → the underlying Python callable
# - description → natural-language hint the agent uses to decide when to call this tool
calculator = Tool(
    name="Calculator",
    func=simple_calculator,
    description="Performs basic arithmetic, e.g., '3 * 4 + 2'."
)


# ─────────────────────────────────────────────────
# STEP 4: Set Up Conversation Memory
# ─────────────────────────────────────────────────
# ConversationBufferMemory stores every message in full (no truncation/summarisation).
# - memory_key    → the key name used when injecting history into the prompt template
# - input_key     → tells memory which field in the input dict is the user's message
# - return_messages=True → stores messages as LangChain message objects (HumanMessage / AIMessage)
memory = ConversationBufferMemory(
    memory_key="chat_history",
    input_key="user_input",
    return_messages=True
)


# ─────────────────────────────────────────────────
# STEP 5: Create the Prompt Template
# ─────────────────────────────────────────────────
# ChatPromptTemplate structures the conversation sent to the model.
# Order matters: system instructions first, then history, then the current user message.
prompt = ChatPromptTemplate.from_messages([
    # Primary system message: sets FitBuddy's personality and instructions
    ("system",
     "You are FitBuddy, a friendly AI fitness coach. "
     "Remember what the user says about their workouts or goals. "
     "Use the calculator tool when math is required. "
     "Keep responses short and natural."),
    # Secondary system message: injects the stored conversation history dynamically
    ("system", "Previous conversation:\n{chat_history}"),
    # Human turn: the user's current question / message
    ("human", "{input}")
])


# ─────────────────────────────────────────────────
# STEP 5.5: Build a Simple Fallback LLM Chain
# ─────────────────────────────────────────────────
# This chain is used as a fallback if the main agent fails.
# The | operator pipes data: prompt formats input → llm generates a response → parser converts to string
output_parser = StrOutputParser()           # Converts AIMessage → plain text string
chain = prompt | llm | output_parser       # Full pipeline: Prompt ➜ GPT-4o-mini ➜ String


# ─────────────────────────────────────────────────
# STEP 6: Build the LangChain Agent
# ─────────────────────────────────────────────────
# The agent can autonomously decide whether to answer directly OR call a tool first.
tools = [calculator]   # List of tools available to the agent

# create_agent constructs a ReAct-style agent:
# - model         → the LLM that drives reasoning and tool selection
# - tools         → the set of tools the agent can invoke
# - system_prompt → a plain-English instruction that shapes the agent's personality/behaviour
agent = create_agent(
    model=llm,
    tools=tools,
    system_prompt=(
        "You are FitBuddy, a friendly AI fitness coach. "
        "Remember what the user says about their workouts or goals. "
        "Use the calculator tool when math is required. "
        "Keep responses short and natural."
    )
)


# ─────────────────────────────────────────────────
# STEP 7: Core Chat Function
# ─────────────────────────────────────────────────
def chat_with_agent(user_input=None):
    """
    Sends a user message to FitBuddy and returns the AI response.

    Fallback order:
        1. LangChain Agent (with tool support)
        2. Simple LLM Chain (prompt | GPT-4o-mini | parser)
        3. Direct Calculator (if the input contains arithmetic symbols)

    Args:
        user_input (str | None): The user's message. If None, prompts via terminal input().

    Returns:
        str: FitBuddy's text response.
    """
    # If no input was passed programmatically, ask the user to type something
    if user_input is None:
        user_input = input("You: ")

    try:
        # ── Build conversation history string from memory ──────────────────
        chat_history = ""
        if hasattr(memory, 'chat_memory') and memory.chat_memory.messages:
            history_messages = []
            for msg in memory.chat_memory.messages:
                # Prefix each stored message with the speaker's role
                if msg.type == "human":
                    history_messages.append(f"User: {msg.content}")
                else:
                    history_messages.append(f"Assistant: {msg.content}")
            chat_history = "\n".join(history_messages)

        # ── Construct the message list for the agent ───────────────────────
        messages = []
        if chat_history:
            # Inject prior conversation so the agent is aware of the context
            messages.append({"role": "system", "content": f"Previous conversation:\n{chat_history}"})

        # Append the current user message as the latest turn
        messages.append({"role": "user", "content": user_input})

        # ── Invoke the agent ───────────────────────────────────────────────
        # The agent decides internally whether to call the Calculator tool or answer directly
        response = agent.invoke({"messages": messages})

        # ── Extract the text from the agent's response ─────────────────────
        if response and "messages" in response:
            last_message = response["messages"][-1]                  # Agent's final reply is the last message
            agent_response = last_message.content if hasattr(last_message, 'content') else str(last_message)

            # Persist both sides of the turn into memory for future context
            memory.chat_memory.add_user_message(user_input)
            memory.chat_memory.add_ai_message(agent_response)

            return agent_response

        return "No response received"

    except Exception as e:
        # ── Fallback 1: Simple LLM Chain ───────────────────────────────────
        # If the agent raises an exception, try the lighter prompt | llm | parser chain
        try:
            # Re-build history string (same logic as above, needed again for the chain)
            chat_history = ""
            if hasattr(memory, 'chat_memory') and memory.chat_memory.messages:
                history_messages = []
                for msg in memory.chat_memory.messages:
                    if msg.type == "human":
                        history_messages.append(f"User: {msg.content}")
                    else:
                        history_messages.append(f"Assistant: {msg.content}")
                chat_history = "\n".join(history_messages)

            # Run the chain – passes both the user's question and full history
            response = chain.invoke({
                "input": user_input,
                "chat_history": chat_history
            })

            # Save to memory so future turns remain contextual
            memory.chat_memory.add_user_message(user_input)
            memory.chat_memory.add_ai_message(response)

            return response

        except Exception as chain_error:
            # ── Fallback 2: Direct Calculator ──────────────────────────────
            # If the chain also fails AND the input looks like an arithmetic expression,
            # call the calculator function directly as a last resort
            if any(op in user_input for op in ["+", "-", "*", "/"]):
                try:
                    result = "Result: " + calculator.invoke(user_input)
                    # Still save the exchange to memory
                    memory.chat_memory.add_user_message(user_input)
                    memory.chat_memory.add_ai_message(result)
                    return result
                except:
                    return "Sorry, I couldn't process that request."

            # If none of the fallbacks applied, surface the error message
            return f"Error: {str(chain_error)}"


# ─────────────────────────────────────────────────
# STEP 8: Interactive Chat Loop
# ─────────────────────────────────────────────────
def interactive_chat():
    """
    Runs a real-time terminal chat loop so users can have a live conversation
    with FitBuddy. Continues until the user types 'quit', 'exit', or 'q'.
    """
    print("=== FitBuddy AI Fitness Coach ===")
    print("Type 'quit', 'exit', or 'q' to end the conversation")
    print("Type 'memory' to see conversation history")
    print("-" * 40)

    while True:
        try:
            user_input = input("\nYou: ").strip()   # Read and trim whitespace from user input

            # ── Exit commands ──────────────────────────────────────────────
            if user_input.lower() in ['quit', 'exit', 'q']:
                print("Goodbye! Stay fit! 💪")
                break

            # ── Show stored conversation history ───────────────────────────
            if user_input.lower() == 'memory':
                print("\n--- Conversation History ---")
                if hasattr(memory, 'chat_memory') and memory.chat_memory.messages:
                    for i, msg in enumerate(memory.chat_memory.messages, 1):
                        print(f"{i}. {msg.type}: {msg.content}")
                else:
                    print("No conversation history yet.")
                continue   # Skip to the next loop iteration (don't call the agent)

            # ── Guard against empty input ──────────────────────────────────
            if not user_input:
                print("Please enter a message.")
                continue

            # ── Get and display FitBuddy's response ───────────────────────
            response = chat_with_agent(user_input)
            print(f"\nFitBuddy: {response}")

        except KeyboardInterrupt:
            # Gracefully handle Ctrl+C
            print("\n\nGoodbye! Stay fit! 💪")
            break
        except Exception as e:
            print(f"\nError: {e}")
            print("Please try again.")


# ─────────────────────────────────────────────────
# ENTRY POINT – Runs when script is executed directly
# ─────────────────────────────────────────────────
if __name__ == "__main__":
    print("=== FitBuddy AI Fitness Coach ===")
    print("Choose an option:")
    print("1. Run demo conversation")
    print("2. Start interactive chat")

    choice = input("\nEnter your choice (1 or 2): ").strip()

    if choice == "2":
        # Launch live interactive session
        interactive_chat()
    else:
        # Run a scripted 3-turn demo that showcases: goal memory, calculator, and recall
        print("\n--- Demo Conversation Start ---\n")

        # Turn 1: User shares workout preferences → tests memory storage
        print("User:", "Hi FitBuddy, I like cardio and yoga workouts.")
        print("Agent:", chat_with_agent("Hi FitBuddy, I like cardio and yoga workouts."))

        # Turn 2: Calorie math question → tests the Calculator tool
        print("\nUser:", "If I burn 90 calories in 10 mins, how many in 1 hour?")
        print("Agent:", chat_with_agent("If I burn 90 calories in 10 mins, how many in 1 hour?"))

        # Turn 3: Asks agent to recall earlier info → tests ConversationBufferMemory
        print("\nUser:", "Remind me what workouts I said I like?")
        print("Agent:", chat_with_agent("Remind me what workouts I said I like?"))

        print("\n--- Demo Conversation End ---")
