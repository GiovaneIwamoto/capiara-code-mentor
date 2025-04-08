<img width="1033" alt="image" src="https://github.com/user-attachments/assets/2e877b62-077a-48e4-8ecc-175788ec1a4b" />

# Installation Guide

- Install required dependencies
```shell
pip install -r requirements.txt
```

- Run Streamlit
```shell
streamlit run app.py
```

# Documentation - Langchain

- Conceptual Guide

https://python.langchain.com/v0.2/docs/concepts/

- Callbacks

https://python.langchain.com/v0.2/docs/concepts/#callbacks

- Streaming

https://python.langchain.com/v0.2/docs/concepts/#streaming

- Message Persistence

https://python.langchain.com/docs/tutorials/chatbot/#message-persistence

- Managing Conversation History

https://python.langchain.com/docs/tutorials/chatbot/#managing-conversation-history

- Trim Messages

https://python.langchain.com/api_reference/core/messages/langchain_core.messages.utils.trim_messages.html

- Retrieval Augmented Generation

https://python.langchain.com/docs/tutorials/rag/#setup

https://python.langchain.com/docs/tutorials/qa_chat_history/

- Retrieval Concept

https://python.langchain.com/docs/concepts/retrieval/

- Retrievers

https://python.langchain.com/docs/concepts/retrievers/

- Vector Store

https://python.langchain.com/docs/concepts/vectorstores/

- Embedding Models

https://python.langchain.com/docs/concepts/embedding_models/

- Ollama Embeddings

https://python.langchain.com/docs/integrations/text_embedding/ollama/

- Pinecone Vector Store

https://python.langchain.com/api_reference/pinecone/vectorstores/langchain_pinecone.vectorstores.PineconeVectorStore.html#langchain_pinecone.vectorstores.PineconeVectorStore

- Recursive Text Splitter

https://python.langchain.com/docs/how_to/recursive_text_splitter/

- Document Base

https://python.langchain.com/api_reference/core/documents/langchain_core.documents.base.Document.html

- Tool Calling

https://python.langchain.com/docs/concepts/tool_calling/

https://blog.langchain.dev/tool-calling-with-langchain/

- Tool Artifacts

https://python.langchain.com/docs/how_to/tool_artifacts/

# Documentation - Maritalk

- Models

https://docs.maritaca.ai/pt/modelos

- Rate Limits

https://docs.maritaca.ai/pt/rate-limits

- Embedding and RAG

https://docs.maritaca.ai/pt/embeddings+Sabia-3+RAG

- Tool Calling

https://docs.maritaca.ai/pt/chamada-funcao

# Documentation - Ollama

- Meta Llama 3

https://ollama.com/library/llama3/blobs/6a0746a1ec1a

```shell
ollama run llama3
```
- Nomic Embed Text

https://ollama.com/library/nomic-embed-text

```shell
ollama pull nomic-embed-text
```

# Documentation - Nomic

- HuggingFace 

https://huggingface.co/nomic-ai/nomic-embed-text-v1.5

- Blog

https://www.nomic.ai/blog/posts/nomic-embed-text-v1

# Documentation - LangSmith

https://docs.smith.langchain.com

# Info - AI Powered Search

- The Basics of AI-Powered Vector Search

https://cameronrwolfe.substack.com/p/the-basics-of-ai-powered-vector-search?utm_source=profile&utm_medium=reader2

- LLM Powered Autonomous Agents

https://lilianweng.github.io/posts/2023-06-23-agent/

# Documentation - Prompt Engineering 

- AWS Prompt Engineering Best Practices

https://docs.aws.amazon.com/prescriptive-guidance/latest/llm-prompt-engineering-best-practices/introduction.html

- AWS Common prompt injection attacks

https://docs.aws.amazon.com/prescriptive-guidance/latest/llm-prompt-engineering-best-practices/common-attacks.html

- IBM Prompt Injection

https://www.ibm.com/think/topics/prompt-injection

# About 

| **Use Case**          | **chunk_size**    | **chunk_overlap** | **Justification** |
|-----------------------|-------------------|-------------------|--------------------|
| **Short Queries**     | 500 - 1000        | 100 - 200         | Improves semantic search accuracy without overly fragmenting the context. |
| **Long Documents**    | 1000 - 2000       | 200 - 300         | Prevents context loss when splitting large documents. |
| **Source Code**       | 300 - 600         | 50 - 100          | Smaller chunks help avoid losing critical information. |