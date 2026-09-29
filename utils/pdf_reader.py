import os
import pandas as pd
from PyPDF2 import PdfReader
from docx import Document


def extract_pdf_text(file_path):
    """Extract text from a PDF file."""

    text = ""

    try:
        reader = PdfReader(file_path)

        for page in reader.pages:
            page_text = page.extract_text()

            if page_text:
                text += page_text + "\n"

    except Exception as e:
        raise Exception(f"Error reading PDF: {e}")

    return text


def extract_docx_text(file_path):
    """Extract text from a DOCX file."""

    text = ""

    try:
        document = Document(file_path)

        for paragraph in document.paragraphs:
            text += paragraph.text + "\n"

    except Exception as e:
        raise Exception(f"Error reading DOCX: {e}")

    return text


def extract_txt_text(file_path):
    """Extract text from a TXT file."""

    try:
        with open(file_path, "r", encoding="utf-8") as file:
            return file.read()

    except Exception as e:
        raise Exception(f"Error reading TXT: {e}")


def load_documents(folder_path):
    """
    Read all PDF, DOCX and TXT files from the documents folder
    and return the extracted data as a Pandas DataFrame.
    """

    documents = []

    for filename in os.listdir(folder_path):

        file_path = os.path.join(folder_path, filename)

        try:

            if filename.lower().endswith(".pdf"):
                text = extract_pdf_text(file_path)

            elif filename.lower().endswith(".docx"):
                text = extract_docx_text(file_path)

            elif filename.lower().endswith(".txt"):
                text = extract_txt_text(file_path)

            else:
                continue

            documents.append({
                "file_name": filename,
                "content": text
            })

        except Exception as e:

            documents.append({
                "file_name": filename,
                "content": f"ERROR: {str(e)}"
            })

    return pd.DataFrame(documents)