import logging
import streamlit as st
from langchain.schema import ChatMessage
from langchain.callbacks.base import BaseCallbackHandler
from langchain_community.chat_models import ChatMaritalk
from langchain_community.chat_models.maritalk import MaritalkHTTPError
from langchain_core.messages import HumanMessage, AIMessage, trim_messages
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langgraph.graph import START, MessagesState, StateGraph
from langgraph.checkpoint.memory import MemorySaver

# Configure Streamlit page settings
st.set_page_config(page_title="Capiara Algorithm Mentor", page_icon="", layout="wide")

# Configure logging
logging.basicConfig(level=logging.DEBUG, format="%(asctime)s [%(levelname)s] %(message)s")
logger = logging.getLogger(__name__)

# Image banner container
# with st.container():
#     st.image("images/banner.png", use_container_width=False, output_format="PNG")

# Display image banner
st.image("images/banner.png")

class StreamHandler(BaseCallbackHandler):
    """Handles real-time streaming of LLM-generated tokens in Streamlit."""
    def __init__(self, container):
        self.container = container
        self.text = ""

    def on_llm_new_token(self, token: str, **kwargs) -> None:
        """Appends new tokens to the response and updates the UI dynamically."""
        self.text += token
        self.container.markdown(self.text)


def get_maritalk_api_key() -> str:
    """Retrieves the Maritalk API key from the sidebar input field."""
    with st.sidebar:
        return st.text_input("Maritalk API Key", type="default")


def initialize_chat_history():
    """Initializes chat history in session state if not already present."""
    if "messages" not in st.session_state:
        st.session_state["messages"] = [ChatMessage(role="assistant", content="How can I help you?")]


def display_chat_history():
    """Displays the chat history stored in session state."""
    for msg in st.session_state["messages"]:
        role = "user" if isinstance(msg, HumanMessage) else "assistant"
        st.chat_message(role).write(msg.content)

# Define the chat prompt template
prompt_template = ChatPromptTemplate.from_messages(
    [
        ("system", "You are a helpful assistant that help students solving algorithms problems! Your name is CapIAra."),
        MessagesPlaceholder(variable_name="messages"),
    ]
)

# Initialize global memory for conversation persistence
if "memory" not in st.session_state:
    st.session_state["memory"] = MemorySaver()

def call_model(state: MessagesState):
    """Calls the Maritalk model to generate a response."""
    api_key = st.session_state.get("api_key")

    if not api_key:
        st.info("Please add your Maritalk API key to continue.", icon=":material/passkey:")
        st.stop()

    llm = ChatMaritalk(
        model="sabia-3",
        api_key=api_key,
        max_tokens=1000,
        stream=True,
        callbacks=[],
    )

    trimmer = trim_messages(
        max_tokens=100,
        strategy="last",
        token_counter=llm,
        include_system=True,
        allow_partial=False,
        start_on="human",
    )

    trimmed_messages = trimmer.invoke(state["messages"])
    logger.info(f"Trimmed messages: {trimmed_messages}")

    prompt = prompt_template.invoke(
        {"messages": trimmed_messages}
    )

    with st.chat_message("assistant"):
        stream_handler = StreamHandler(st.empty())
        llm.callbacks = [stream_handler]

        response = ""
        for chunk in llm.stream(prompt):
            response += chunk.content

        full_history = state["messages"] + [AIMessage(content=response)]
        return {"messages": full_history}

# Define workflow for processing user input
workflow = StateGraph(state_schema=MessagesState)
workflow.add_edge(START, "model")
workflow.add_node("model", call_model)

app = workflow.compile(checkpointer=st.session_state["memory"])

def process_user_input(prompt: str, api_key: str):
    # Add Docstring
    # FIXME: Messages append is causing the chat history to be duplicated
    st.session_state.messages.append(ChatMessage(role="user", content=prompt))
    st.chat_message("user").write(prompt)

    if not api_key:
        st.info("Please add your Maritalk API key to continue.", icon=":material/passkey:")
        st.stop()

    try:
        # Store the API key in session state
        st.session_state["api_key"] = api_key

        input_messages = st.session_state["messages"] + [HumanMessage(prompt)]

        output = app.invoke(
            {"messages": input_messages},
            {"configurable": {"thread_id": "12345abcd"}},
        )

        # Update session state with the new chat history
        st.session_state["messages"] = output["messages"]
        logger.info(f"Chat history: {output['messages']}")

    except MaritalkHTTPError as e:
        logger.error(f"API Error: {e}")
        st.error("Invalid Maritalk API key, please enter a valid one.", icon=":material/key_off:")
        st.stop()


# Main application logic
if __name__ == "__main__":
    maritalk_api_key = get_maritalk_api_key()
    initialize_chat_history()
    display_chat_history()
    
    if prompt := st.chat_input():
        process_user_input(prompt, maritalk_api_key)
