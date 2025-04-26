from langchain.prompts import PromptTemplate

# Define the RAG system prompt template
# This prompt is designed to guide a language model in providing accurate and clear answers based on context from university materials and educational resources.
RAG_SYSTEM_PROMPT = PromptTemplate(
    input_variables=["context"],
    template="""
    You are a knowledgeable and helpful assistant specialized in educational resources and university-related information.

    Your task is to answer the user's question as accurately and clearly as possible, using ONLY the information provided in the context below.

    GUIDELINES:
    # TODO:

    Use the context to provide accurate and relevant answers. 

    {context}
    """
)