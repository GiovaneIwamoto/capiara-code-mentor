from langchain_openai import OpenAIEmbeddings
from langchain_pinecone import PineconeVectorStore
from pinecone import Pinecone, PineconeException

def initialize_vectorstore(pinecone_api_key: str, pinecone_index_name: str, embedding_model: str, openai_api_key: str) -> PineconeVectorStore:
    """
    Initialize the vector store using Pinecone and OpenAI embeddings.
    
    Args:
        pinecone_api_key (str): Pinecone API key.
        pinecone_index_name (str): Name of the Pinecone index.
        embedding_model (str): OpenAI embedding model name.
        openai_api_key (str): OpenAI API key for embedding generation.
    
    Returns:
        PineconeVectorStore: Initialized vector store.
    
    Raises:
        ValueError: If any of the required parameters are missing.
        RuntimeError: If initialization of Pinecone or index fails.
    """
    # Validate parameters
    if not pinecone_api_key:
        raise ValueError("Pinecone API key is required.")
    if not pinecone_index_name:
        raise ValueError("Pinecone index name is required.")
    if not embedding_model:
        raise ValueError("Embedding model name is required.")
    if not openai_api_key:
        raise ValueError("OpenAI API key is required.")

    # Initialize Pinecone client
    try:
        pinecone = Pinecone(api_key=pinecone_api_key)
    except Exception as e:
        raise RuntimeError(f"Failed to initialize Pinecone client: {str(e)}") from e

    # Connect to existing index
    try:
        index = pinecone.Index(pinecone_index_name)
    except PineconeException as e:
        raise RuntimeError(f"Failed to connect to Pinecone index '{pinecone_index_name}'.") from e

    # Initialize embeddings
    try:
        embeddings = OpenAIEmbeddings(model=embedding_model, openai_api_key=openai_api_key)
    except Exception as e:
        raise RuntimeError(f"Failed to initialize embeddings with model '{embedding_model}'.") from e

    # Initialize vector store
    try:
        vectorstore = PineconeVectorStore(embedding=embeddings, index=index)
    except Exception as e:
        raise RuntimeError(f"Failed to initialize PineconeVectorStore: {str(e)}") from e

    return vectorstore
