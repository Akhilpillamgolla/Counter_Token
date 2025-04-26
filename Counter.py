import streamlit as st
import os
from PyPDF2 import PdfReader
import docx

# Function to count metrics in the text
def count_text_metrics(text):
    words = len(text.split())
    characters = len(text)
    sentences = text.count('.') + text.count('!') + text.count('?')
    paragraphs = text.count('\n\n') + 1
    return words, characters, sentences, paragraphs

# Function to process TXT files
def process_txt_file(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        text = file.read()
    return count_text_metrics(text)

# Function to process PDF files
def process_pdf_file(file_path):
    reader = PdfReader(file_path)
    text = ''
    for page in reader.pages:
        text += page.extract_text()
    return count_text_metrics(text)

# Function to process DOCX files
def process_docx_file(file_path):
    doc = docx.Document(file_path)
    text = '\n'.join([paragraph.text for paragraph in doc.paragraphs])
    return count_text_metrics(text)

# Process uploaded file
def process_file(file):
    extension = os.path.splitext(file.name)[1].lower()
    if extension == '.txt':
        return count_text_metrics(file.read().decode('utf-8'))
    elif extension == '.pdf':
        with open("temp.pdf", "wb") as temp_pdf:
            temp_pdf.write(file.getvalue())
        return process_pdf_file("temp.pdf")
    elif extension == '.docx':
        with open("temp.docx", "wb") as temp_docx:
            temp_docx.write(file.getvalue())
        return process_docx_file("temp.docx")
    else:
        raise ValueError('Unsupported file type. Please upload a .txt, .pdf, or .docx file.')

# Streamlit UI
st.title("File Metrics Calculator")
st.write("Upload a file (PDF, DOCX, or TXT) to calculate its word count, character count, sentence count, and paragraph count.")

uploaded_file = st.file_uploader("Choose a file", type=["txt", "pdf", "docx"])

if uploaded_file:
    try:
        words, characters, sentences, paragraphs = process_file(uploaded_file)
        st.write(f"**Word count:** {words}")
        st.write(f"**Character count:** {characters}")
        st.write(f"**Sentence count:** {sentences}")
        st.write(f"**Paragraph count:** {paragraphs}")
    except Exception as e:
        st.error(f"An error occurred: {e}")