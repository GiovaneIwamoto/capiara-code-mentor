import logging
import streamlit as st
from langchain_community.chat_models import ChatMaritalk
from langchain_community.chat_models.maritalk import MaritalkHTTPError
from langchain_core.messages import HumanMessage
from langchain.schema import ChatMessage
from langchain.callbacks.base import BaseCallbackHandler

# Configure logging
logging.basicConfig(level=logging.DEBUG, format='%(asctime)s [%(levelname)s] %(message)s')
logger = logging.getLogger(__name__)

# Configure Streamlit
st.set_page_config(page_title="Capiara Algorithm Mentor", layout="wide")
st.title(":material/network_intel_node: Capiara Algorithm Mentor")

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
    for msg in st.session_state.messages:
        st.chat_message(msg.role).write(msg.content)


def process_user_input(prompt: str, api_key: str):
    """Processes user input by sending it to the Maritalk model and streaming the response."""
    st.session_state.messages.append(ChatMessage(role="user", content=prompt))
    st.chat_message("user").write(prompt)

    if not api_key:
        st.info("Please add your Maritalk API key to continue.", icon=":material/passkey:")
        st.stop()

    try:
        llm = ChatMaritalk(
            model="sabia-3",
            api_key=api_key,
            max_tokens=1000,
            stream=True,
            callbacks=[],
        )

        messages = [HumanMessage(content=prompt)]
        # Test API key by fetching the first response
        next(llm.stream(messages))

    except MaritalkHTTPError as e:
        logger.error(f"API Error: {e}")
        st.error("Invalid Maritalk API key, please enter a valid one.", icon=":material/key_off:")
        st.stop()

    with st.chat_message("assistant"):
        stream_handler = StreamHandler(st.empty())

        llm.callbacks = [stream_handler]

        response = ""
        for chunk in llm.stream(messages):
            response += chunk.content

        st.session_state.messages.append(ChatMessage(role="assistant", content=response))
        logger.info("Response generated successfully")

# Main application logic
if __name__ == "__main__":
    maritalk_api_key = get_maritalk_api_key()
    initialize_chat_history()
    display_chat_history()
    
    if prompt := st.chat_input():
        process_user_input(prompt, maritalk_api_key)
