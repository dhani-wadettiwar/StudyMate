import os
from typing import List, Tuple
from langchain_community.vectorstores import FAISS
from langchain_google_genai import GoogleGenerativeAIEmbeddings, ChatGoogleGenerativeAI
from langchain_core.documents import Document
from langchain_core.prompts import PromptTemplate

# Explicit RAG System Prompt to enforce document grounding and avoid hallucination
RAG_PROMPT_TEMPLATE = """You are StudyMate, an academic syllabus assistant.

Answer the user's question using ONLY the provided syllabus context.

If the answer is not present in the context, clearly say:

'I could not find this information in the uploaded syllabus.'

Do not invent information.

Keep the answer clear, short, and student-friendly.

Context:
{context}

Question:
{question}"""

def get_embeddings(api_key: str):
    """
    Initializes Google Generative AI embeddings with the provided API key.
    """
    return GoogleGenerativeAIEmbeddings(
        model="models/embedding-001",
        google_api_key=api_key
    )

def create_vector_store(chunks: List[Document], api_key: str) -> FAISS:
    """
    Generates embeddings for document chunks and creates a local FAISS vector store.
    """
    embeddings = get_embeddings(api_key)
    vector_store = FAISS.from_documents(chunks, embeddings)
    return vector_store

def retrieve_documents(vector_store: FAISS, query: str, k: int = 4) -> List[Document]:
    """
    Retrieves the top k most relevant document chunks from the FAISS vector store for a query.
    """
    if vector_store is None:
        return []
    retrieved_docs = vector_store.similarity_search(query, k=k)
    return retrieved_docs

def generate_answer(query: str, retrieved_docs: List[Document], api_key: str) -> Tuple[str, List[Document]]:
    """
    Generates an answer using Gemini LLM based strictly on retrieved syllabus context.
    Returns a tuple of (answer_string, retrieved_docs).
    """
    if not retrieved_docs:
        return "I could not find this information in the uploaded syllabus.", []

    # Combine text from retrieved documents to build context string
    context_text = "\n\n---\n\n".join([doc.page_content for doc in retrieved_docs])

    # Format the prompt
    prompt = PromptTemplate(
        template=RAG_PROMPT_TEMPLATE,
        input_variables=["context", "question"]
    )
    formatted_prompt = prompt.format(context=context_text, question=query)

    # Initialize Gemini LLM
    llm = ChatGoogleGenerativeAI(
        model="gemini-1.5-flash",
        google_api_key=api_key,
        temperature=0.2
    )

    # Query LLM
    response = llm.invoke(formatted_prompt)
    answer_text = response.content.strip()

    return answer_text, retrieved_docs
