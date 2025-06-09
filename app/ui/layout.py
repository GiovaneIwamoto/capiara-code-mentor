import os
import streamlit as st
from langchain_core.messages import HumanMessage
from langchain.schema import ChatMessage

def set_page_config():
    """Set the Streamlit page configuration."""
    st.set_page_config(
        page_title="Capiara Code Mentor",
        page_icon=":material/collections_bookmark:",
        layout="centered",
        initial_sidebar_state="expanded",
        menu_items={
            'Get Help': 'https://github.com/GiovaneIwamoto/capiara-code-mentor',
            'Report a bug': "https://github.com/GiovaneIwamoto/capiara-code-mentor/issues",
            'About': """
            ### Thanks for checking out the project!
            If you find it useful, please consider giving it a ★ on [GitHub](https://github.com/GiovaneIwamoto/capiara-code-mentor).
            It really helps support the project and keeps it growing! Your feedback and support are greatly appreciated!"""
        }
    )

def display_banner():
    """Display the banner image at the top of the app."""
    current_dir = os.path.dirname(__file__)
    image_path = os.path.join(current_dir, "../assets/banner.png")
    st.image(image_path)

def initialize_chat_history():
    """Initialize chat history in session state."""
    if "messages" not in st.session_state:
        st.session_state["messages"] = [
            ChatMessage(role="assistant", content="How can I assist you with coding and algorithms today?"),
        ]

def display_chat_history():
    """Display the chat history in the Streamlit app."""
    for msg in st.session_state["messages"]:
        if isinstance(msg, HumanMessage):
            st.chat_message(name="user", avatar=":material/face:").write(msg.content)
        else:
            st.chat_message(name="assistant", avatar=":material/smart_toy:").write(msg.content)
