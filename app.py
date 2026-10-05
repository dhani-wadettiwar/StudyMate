import os
import streamlit as st
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

from utils.pdf_processor import load_pdf, split_documents
from utils.rag_pipeline import create_vector_store, retrieve_documents, generate_answer

# Page Configuration
st.set_page_config(
    page_title="StudyMate - Syllabus Assistant",
    page_icon="📚",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS styling for modern, clean academic theme
st.markdown("""
    <style>
    .main-title {
        font-size: 2.3rem;
        font-weight: 700;
        color: #1E293B;
        margin-bottom: 0.2rem;
    }
    .sub-title {
        font-size: 1.1rem;
        color: #64748B;
        margin-bottom: 1.5rem;
    }
    .answer-card {
        background-color: #F8FAFC;
        border-left: 4px solid #3B82F6;
        padding: 1.2rem;
        border-radius: 8px;
        margin-top: 1rem;
        margin-bottom: 1.5rem;
    }
    .source-card {
        background-color: #FFFFFF;
        border: 1px solid #E2E8F0;
        padding: 0.9rem;
        border-radius: 6px;
        margin-bottom: 0.8rem;
    }
    .source-header {
        font-weight: 600;
        color: #2563EB;
        font-size: 0.95rem;
        margin-bottom: 0.3rem;
    }
    .source-excerpt {
        font-size: 0.9rem;
        color: #334155;
        font-style: italic;
    }
    .stButton button {
        border-radius: 6px;
    }
    </style>
""", unsafe_allow_html=True)

# Helper function to get API Key safely
def get_gemini_api_key() -> str:
    api_key = os.getenv("GEMINI_API_KEY", "").strip()
    # Check if missing or default placeholder
    if not api_key or "your_api_key" in api_key.lower() or "your_gemini_api_key" in api_key.lower():
        return ""
    return api_key

# Initialize Session State Variables
if "vector_store" not in st.session_state:
    st.session_state["vector_store"] = None
if "processed_filename" not in st.session_state:
    st.session_state["processed_filename"] = None
if "last_answer" not in st.session_state:
    st.session_state["last_answer"] = None
if "last_sources" not in st.session_state:
    st.session_state["last_sources"] = []
if "last_query" not in st.session_state:
    st.session_state["last_query"] = ""

# Sidebar: Syllabus Upload & Processing
with st.sidebar:
    st.image("https://img.icons8.com/color/96/000000/open-book.png", width=64)
    st.title("Upload Syllabus")
    st.markdown("Select a PDF syllabus file to index.")

    uploaded_pdf = st.file_uploader("Upload PDF file", type=["pdf"], help="Select a syllabus PDF document")
    process_btn = st.button("⚡ Process PDF", use_container_width=True, type="primary")

    if process_btn:
        if uploaded_pdf is None:
            st.error("Please select a PDF file first.")
        else:
            api_key = get_gemini_api_key()
            if not api_key:
                st.error("⚠️ `GEMINI_API_KEY` is not configured in `.env`. Please add your API key to process the PDF.")
            else:
                with st.spinner("Processing PDF, extracting text & building vector embeddings..."):
                    try:
                        # 1. Extract documents
                        docs = load_pdf(uploaded_pdf)
                        # 2. Chunk documents
                        chunks = split_documents(docs, chunk_size=800, chunk_overlap=100)
                        # 3. Build FAISS vector store
                        vector_store = create_vector_store(chunks, api_key)

                        # Store in session state
                        st.session_state["vector_store"] = vector_store
                        st.session_state["processed_filename"] = uploaded_pdf.name
                        st.session_state["last_answer"] = None
                        st.session_state["last_sources"] = []
                        st.session_state["last_query"] = ""

                        st.success(f"✅ Success! Processed **{len(docs)}** pages into **{len(chunks)}** chunks.")
                    except Exception as e:
                        st.error(f"Error processing PDF: {str(e)}")

    if st.session_state["processed_filename"]:
        st.divider()
        st.markdown(f"📄 **Current Active Syllabus:**\n`{st.session_state['processed_filename']}`")

# Main Interface
st.markdown('<div class="main-title">📚 StudyMate</div>', unsafe_allow_html=True)
st.markdown('<div class="sub-title">RAG-Based Intelligent Syllabus Assistant</div>', unsafe_allow_html=True)

st.markdown("### Ask Your Syllabus")

# Suggested Sample Questions
st.markdown("**Suggested Questions:**")
col1, col2 = st.columns(2)
suggested_query = None

with col1:
    if st.button("📌 What topics are covered in Unit 1?", use_container_width=True):
        suggested_query = "What topics are covered in Unit 1?"
    if st.button("📌 What is the syllabus for this subject?", use_container_width=True):
        suggested_query = "What is the syllabus for this subject?"

with col2:
    if st.button("📌 What are the important topics in Unit 3?", use_container_width=True):
        suggested_query = "What are the important topics in Unit 3?"
    if st.button("📌 Which topics are related to CNN?", use_container_width=True):
        suggested_query = "Which topics are related to CNN?"

# Question Input Form
query_input = st.text_input(
    "Ask a question about your syllabus...",
    value=suggested_query if suggested_query else "",
    placeholder="e.g. What is the evaluation scheme for this course?"
)

ask_btn = st.button("🔍 Ask Question", type="primary")

# Execute RAG Q&A
target_query = suggested_query if suggested_query else (query_input.strip() if ask_btn else None)

if target_query:
    api_key = get_gemini_api_key()
    
    if not api_key:
        st.error("⚠️ **GEMINI_API_KEY is missing or invalid.** Please configure `GEMINI_API_KEY` in your `.env` file.")
    elif st.session_state["vector_store"] is None:
        st.warning("Please upload a syllabus PDF first.")
    else:
        with st.spinner("Searching syllabus & generating answer..."):
            try:
                # 1. Retrieve top 4 relevant chunks
                retrieved_docs = retrieve_documents(st.session_state["vector_store"], target_query, k=4)
                # 2. Generate grounded answer from LLM
                answer, sources = generate_answer(target_query, retrieved_docs, api_key)
                
                st.session_state["last_query"] = target_query
                st.session_state["last_answer"] = answer
                st.session_state["last_sources"] = sources
            except Exception as e:
                st.error(f"Error generating answer: {str(e)}")

# Render Answer & Sources if available
if st.session_state["last_answer"]:
    st.divider()
    st.markdown("### Answer")
    st.markdown(f'<div class="answer-card">{st.session_state["last_answer"]}</div>', unsafe_allow_html=True)

    if st.session_state["last_sources"]:
        st.markdown("### Sources")
        for idx, doc in enumerate(st.session_state["last_sources"], start=1):
            page_num = doc.metadata.get("page", 0) + 1
            source_file = doc.metadata.get("source", "Syllabus PDF")
            # Truncate content to a short excerpt
            excerpt = doc.page_content.strip()
            if len(excerpt) > 280:
                excerpt = excerpt[:280] + "..."
            
            st.markdown(f"""
                <div class="source-card">
                    <div class="source-header">Source {idx} — Page {page_num} ({source_file})</div>
                    <div class="source-excerpt">"{excerpt}"</div>
                </div>
            """, unsafe_allow_html=True)
