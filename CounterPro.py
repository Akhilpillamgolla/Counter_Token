import streamlit as st
import os
from PyPDF2 import PdfReader
import docx

def count_text_metrics(text):
    """
    Given a text string, compute:
      - words, characters, sentences, paragraphs,
      - reading time in minutes (200 words/min)
      - speaking time in minutes (130 words/min)
    """
    words = len(text.split())
    characters = len(text)
    # Count sentence end markers (. ! ?)
    sentences = text.count('.') + text.count('!') + text.count('?')
    # Count paragraph breaks; if none, assume the entire text is a single paragraph.
    paragraphs = text.count('\n\n') + (1 if text.strip() else 0)
    reading_time = round(words / 200)  # approximate reading time in minutes
    speaking_time = round(words / 130)  # approximate speaking time in minutes
    return words, characters, sentences, paragraphs, reading_time, speaking_time

def process_txt_file(uploaded_file):
    text = uploaded_file.read().decode('utf-8')
    metrics = count_text_metrics(text)
    page_count = 1  # Assuming 1 page for TXT files
    return metrics + (page_count,)

def process_pdf_file(uploaded_file):
    # Save uploaded PDF bytes as a temporary file.
    temp_filename = "temp.pdf"
    with open(temp_filename, "wb") as f:
        f.write(uploaded_file.getvalue())
    
    reader = PdfReader(temp_filename)
    text = ""
    # Extract text from every page
    for page in reader.pages:
        page_text = page.extract_text()
        if page_text:
            text += page_text
    page_count = len(reader.pages)
    metrics = count_text_metrics(text)
    
    os.remove(temp_filename)
    return metrics + (page_count,)

def process_docx_file(uploaded_file):
    # Save uploaded DOCX bytes as a temporary file.
    temp_filename = "temp.docx"
    with open(temp_filename, "wb") as f:
        f.write(uploaded_file.getvalue())
    
    doc = docx.Document(temp_filename)
    # Join all paragraph texts into a single string.
    text = "\n".join([para.text for para in doc.paragraphs])
    metrics = count_text_metrics(text)
    page_count = 1  # Page count is not intrinsic to DOCX; adjust if needed.
    
    os.remove(temp_filename)
    return metrics + (page_count,)

# ----------------- Streamlit UI -----------------
st.title("Document Scanner")
st.write(
    """
    Upload your file (PDF, DOCX, or TXT) to analyze its content and retrieve:
    - **Total Words**
    - **Characters**
    - **Sentences**
    - **Paragraphs**
    - **Estimated Reading Time**
    - **Estimated Speaking Time**
    - **Page Count**
    """
)

uploaded_file = st.file_uploader("Choose a file", type=["txt", "pdf", "docx"])

if uploaded_file is not None:
    extension = os.path.splitext(uploaded_file.name)[1].lower()
    try:
        if extension == ".txt":
            words, characters, sentences, paragraphs, reading_time, speaking_time, page_count = process_txt_file(uploaded_file)
        elif extension == ".pdf":
            words, characters, sentences, paragraphs, reading_time, speaking_time, page_count = process_pdf_file(uploaded_file)
        elif extension == ".docx":
            words, characters, sentences, paragraphs, reading_time, speaking_time, page_count = process_docx_file(uploaded_file)
        else:
            st.error("Unsupported file type. Please upload a .txt, .pdf, or .docx file.")
        
        st.header("Document Scanner Results")
        st.write(f"**Total Words:** {words}")
        st.write(f"**Characters:** {characters}")
        st.write(f"**Sentences:** {sentences}")
        st.write(f"**Paragraphs:** {paragraphs}")
        st.write(f"**Reading Time:** {reading_time} min")
        st.write(f"**Speaking Time:** {speaking_time} min")
        st.write(f"**Page Count:** {page_count}")
    except Exception as e:
        st.error(f"An error occurred: {e}")
