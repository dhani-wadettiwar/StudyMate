import os
import tempfile
from typing import List
from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_core.documents import Document

def load_pdf(uploaded_file) -> List[Document]:
    """
    Saves an uploaded PDF file temporarily, loads its contents using PyPDFLoader,
    and returns a list of Document objects preserving page metadata.
    """
    if uploaded_file is None:
        raise ValueError("No file provided.")

    # Create a temporary file to store the uploaded PDF bytes
    with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as tmp_file:
        tmp_file.write(uploaded_file.getvalue())
        tmp_path = tmp_file.name

    try:
        loader = PyPDFLoader(tmp_path)
        documents = loader.load()

        # Check if text was extracted from PDF
        total_text_length = sum(len(doc.page_content.strip()) for doc in documents)
        if total_text_length == 0:
            raise ValueError("Unable to extract readable text from this PDF.")

        # Update metadata to preserve original filename if available
        original_name = getattr(uploaded_file, "name", "uploaded_syllabus.pdf")
        for doc in documents:
            doc.metadata["source"] = original_name

        return documents
    finally:
        # Clean up temporary file
        if os.path.exists(tmp_path):
            os.remove(tmp_path)

def split_documents(documents: List[Document], chunk_size: int = 800, chunk_overlap: int = 100) -> List[Document]:
    """
    Splits document pages into smaller manageable chunks using RecursiveCharacterTextSplitter.
    """
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=chunk_size,
        chunk_overlap=chunk_overlap,
        separators=["\n\n", "\n", " ", ""]
    )
    chunks = text_splitter.split_documents(documents)
    return chunks
