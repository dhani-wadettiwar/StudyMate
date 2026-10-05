# StudyMate – RAG-Based Intelligent Syllabus Assistant

## Problem Statement
Students often need to search lengthy syllabus PDFs to find specific information such as course topics, unit details, or evaluation criteria. StudyMate allows students to upload their syllabus PDF and ask natural-language questions to immediately retrieve accurate, grounded information.

## Solution
StudyMate uses **Retrieval-Augmented Generation (RAG)** to index syllabus content into a local vector database and feed relevant excerpts into Google's Gemini LLM to generate precise answers backed by page citations.

## Features
* 📄 **PDF Upload**: Upload any academic syllabus PDF document.
* 🔍 **Automatic Text Extraction & Chunking**: Preserves page metadata while breaking text into manageable contexts.
* ⚡ **Local Vector Search**: Uses FAISS for ultra-fast vector search.
* 🤖 **Grounded Q&A**: Employs Gemini LLM with strict context prompting to prevent hallucinations.
* 📌 **Source Citations**: Displays exact page numbers and excerpts for full transparency.
* 🎯 **Suggested Questions**: Pre-configured sample questions for quick testing.

## Technology Stack
* **Python**: Core application language
* **Streamlit**: Web interface
* **LangChain**: RAG orchestration framework
* **FAISS**: Local vector database
* **Google Generative AI (Gemini)**: Embeddings & LLM Q&A engine
* **PyPDF**: PDF document loader

## How RAG Works
```text
PDF Upload 
   ↓
Text Extraction & Metadata Preservation (PyPDFLoader)
   ↓
Text Chunking (RecursiveCharacterTextSplitter)
   ↓
Embedding Generation (GoogleGenerativeAIEmbeddings)
   ↓
Local Vector Storage (FAISS)
   ↓
Similarity Search (k=4)
   ↓
Context + User Question → LLM (Gemini 1.5 Flash)
   ↓
Answer + Page Source Display
```

## How to Run

1. **Clone/Navigate to the Project Directory**:
   ```bash
   cd StudyMate
   ```

2. **Create and Activate Virtual Environment**:
   ```bash
   python -m venv .venv
   # On Windows PowerShell:
   .venv\Scripts\Activate.ps1
   # On macOS/Linux:
   source .venv/bin/activate
   ```

3. **Install Dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

4. **Configure Environment Variables**:
   Copy `.env.example` to `.env` and set your Google Gemini API key:
   ```env
   GEMINI_API_KEY=your_gemini_api_key_here
   ```

5. **Run Application**:
   ```bash
   streamlit run app.py
   ```
