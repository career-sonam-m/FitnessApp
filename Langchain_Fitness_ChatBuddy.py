# Step 1: Imports
import os
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from langchain_classic.memory import ConversationBufferMemory
from langchain_core.tools import Tool
from langchain_core.prompts import ChatPromptTemplate
from langchain.agents import create_agent
from langchain_core.messages import SystemMessage, HumanMessage
from langchain_core.runnables import RunnablePassthrough
from langchain_core.output_parsers import StrOutputParser


# Step 2: Load API Key from environment (no hardcoding)
load_dotenv()
openai_api_key = os.getenv("OPENAI_API_KEY")
# Initialize OpenAI chat with direct environment variable access
llm = ChatOpenAI(
    temperature=0.7,
    model="gpt-4o-mini",
    api_key=os.environ.get("OPENAI_API_KEY"),  # Use get() for safety
    base_url=os.getenv("OPENAI_API_BASE")
)


# -------------------------
# Step 3: Define a Simple Tool (Calculator)
# -------------------------
def simple_calculator(expression: str) -> str:
    """Safely evaluate arithmetic."""
    try:
        return str(eval(expression))
    except Exception:
        return "Invalid math expression."

calculator = Tool(
    name="Calculator",
    func=simple_calculator,
    description="Performs basic arithmetic, e.g., '3 * 4 + 2'."
)

# -------------------------
# Step 4: Setup Memory
# -------------------------
memory = ConversationBufferMemory(
    memory_key="chat_history",
    input_key="user_input",
    return_messages=True
)

# -------------------------
# Step 5: Create Prompt Template
# -------------------------
prompt = ChatPromptTemplate.from_messages([
    ("system", 
     "You are FitBuddy, a friendly AI fitness coach. "
     "Remember what the user says about their workouts or goals. "
     "Use the calculator tool when math is required. "
     "Keep responses short and natural."),
    ("system", "Previous conversation:\n{chat_history}"),
    ("human", "{input}")
])

# -------------------------
# Step 5.5: Create a Simple Chain
# -------------------------
output_parser = StrOutputParser()
chain = prompt | llm | output_parser

# -------------------------
# Step 6: Build the Agent
# -------------------------
# Create tools list
tools = [calculator]

# Create agent
agent = create_agent(
    model=llm,
    tools=tools,
    system_prompt="You are FitBuddy, a friendly AI fitness coach. Remember what the user says about their workouts or goals. Use the calculator tool when math is required. Keep responses short and natural."
)

# -------------------------
# Step 7: Simulate Conversation
# -------------------------
def chat_with_agent(user_input=None):
    # If no input provided, ask user for input
    if user_input is None:
        user_input = input("You: ")
    
    try:
        # Get chat history from memory to include in agent context
        chat_history = ""
        if hasattr(memory, 'chat_memory') and memory.chat_memory.messages:
            # Format conversation history for context
            history_messages = []
            for msg in memory.chat_memory.messages:
                if msg.type == "human":
                    history_messages.append(f"User: {msg.content}")
                else:
                    history_messages.append(f"Assistant: {msg.content}")
            chat_history = "\n".join(history_messages)
        
        # Use the agent with conversation history
        messages = []
        if chat_history:
            # Add conversation history as context
            messages.append({"role": "system", "content": f"Previous conversation:\n{chat_history}"})
        
        # Add current user message
        messages.append({"role": "user", "content": user_input})
        
        response = agent.invoke({"messages": messages})
        
        # Extract the last message content
        if response and "messages" in response:
            last_message = response["messages"][-1]
            agent_response = last_message.content if hasattr(last_message, 'content') else str(last_message)
            
            # Save conversation to memory
            memory.chat_memory.add_user_message(user_input)
            memory.chat_memory.add_ai_message(agent_response)
            
            return agent_response
        return "No response received"
        
    except Exception as e:
        # Fallback to simple chain if agent fails
        try:
            # Get chat history from memory
            chat_history = ""
            if hasattr(memory, 'chat_memory') and memory.chat_memory.messages:
                history_messages = []
                for msg in memory.chat_memory.messages:
                    if msg.type == "human":
                        history_messages.append(f"User: {msg.content}")
                    else:
                        history_messages.append(f"Assistant: {msg.content}")
                chat_history = "\n".join(history_messages)
            
            # Use the chain
            response = chain.invoke({
                "input": user_input,
                "chat_history": chat_history
            })
            
            # Save to memory
            memory.chat_memory.add_user_message(user_input)
            memory.chat_memory.add_ai_message(response)
            
            return response
        except Exception as chain_error:
            # Final fallback for simple math
            if any(op in user_input for op in ["+", "-", "*", "/"]):
                try:
                    result = "Result: " + calculator.invoke(user_input)
                    # Save to memory
                    memory.chat_memory.add_user_message(user_input)
                    memory.chat_memory.add_ai_message(result)
                    return result
                except:
                    return "Sorry, I couldn't process that request."
            return f"Error: {str(chain_error)}"

def interactive_chat():
    """Interactive chat loop for dynamic user queries"""
    print("=== FitBuddy AI Fitness Coach ===")
    print("Type 'quit', 'exit', or 'q' to end the conversation")
    print("Type 'memory' to see conversation history")
    print("-" * 40)
    
    while True:
        try:
            user_input = input("\nYou: ").strip()
            
            if user_input.lower() in ['quit', 'exit', 'q']:
                print("Goodbye! Stay fit! 💪")
                break
            
            if user_input.lower() == 'memory':
                print("\n--- Conversation History ---")
                if hasattr(memory, 'chat_memory') and memory.chat_memory.messages:
                    for i, msg in enumerate(memory.chat_memory.messages, 1):
                        print(f"{i}. {msg.type}: {msg.content}")
                else:
                    print("No conversation history yet.")
                continue
            
            if not user_input:
                print("Please enter a message.")
                continue
            
            # Get agent response
            response = chat_with_agent(user_input)
            print(f"\nFitBuddy: {response}")
            
        except KeyboardInterrupt:
            print("\n\nGoodbye! Stay fit! 💪")
            break
        except Exception as e:
            print(f"\nError: {e}")
            print("Please try again.")

if __name__ == "__main__":
    print("=== FitBuddy AI Fitness Coach ===")
    print("Choose an option:")
    print("1. Run demo conversation")
    print("2. Start interactive chat")
    
    choice = input("\nEnter your choice (1 or 2): ").strip()
    
    if choice == "2":
        interactive_chat()
    else:
        print("\n--- Demo Conversation Start ---\n")
        
        # Turn 1: user gives info
        print("User:", "Hi FitBuddy, I like cardio and yoga workouts.")
        print("Agent:", chat_with_agent("Hi FitBuddy, I like cardio and yoga workouts."))

        # Turn 2: numeric query (uses calculator)
        print("\nUser:", "If I burn 90 calories in 10 mins, how many in 1 hour?")
        print("Agent:", chat_with_agent("If I burn 90 calories in 10 mins, how many in 1 hour?"))

        # Turn 3: memory recall
        print("\nUser:", "Remind me what workouts I said I like?")
        print("Agent:", chat_with_agent("Remind me what workouts I said I like?"))

        print("\n--- Demo Conversation End ---")
