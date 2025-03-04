import logging
import streamlit as st
from langchain_community.chat_models import ChatMaritalk
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts.chat import ChatPromptTemplate

# Logger config
logging.basicConfig(level=logging.DEBUG, format='%(asctime)s [%(levelname)s] %(message)s')
logger = logging.getLogger(__name__)

# Streamlit config
st.set_page_config(page_title="🦜🔗 Quickstart App")
st.title('🦜🔗 Quickstart App')

maritalk_api_key = st.sidebar.text_input('Maritalk API Key')

def generate_response(input_text):
    if not maritalk_api_key:
        logger.warning("User did not provide API key")
        st.warning("Please provide your API key", icon="⚠")
        return

    try:
        logger.info("Generating response for input")

        llm = ChatMaritalk(
            model="sabia-3",
            api_key=maritalk_api_key,
            max_tokens=1000,
        )

        output_parser = StrOutputParser()
        chat_prompt = ChatPromptTemplate.from_messages(
            [
                ("system", "You are a helpful assistant."),
                ("human", input_text)
            ]
        )
        chain = chat_prompt | llm | output_parser

        response = chain.invoke({})

        logger.info("Response generated successfully")
        st.info(response)

    except Exception as e:
        logger.error(f"An error occurred while generating response: {e}")
        st.error("An error occurred while generating response.")

with st.form('my_form'):
    text = st.text_area('Enter text:', 'How can I help you?')
    submitted = st.form_submit_button('Submit')
    
    if submitted:
        logger.info("User submitted text for generating response")
        generate_response(text)