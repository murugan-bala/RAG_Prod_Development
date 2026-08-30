import os
from pypdf import PdfReader


def load_pdf(file_path):

    reader = PdfReader(file_path)

    text = ""

    for page in reader.pages:

        page_text = page.extract_text()

        if page_text:
            text += page_text
            text += "\n"

    return text


def load_all_pdfs(folder_path):

    documents = []

    for file_name in os.listdir(folder_path):

        if file_name.lower().endswith(".pdf"):

            file_path = os.path.join(
                folder_path,
                file_name
            )

            print("Loading:", file_name)

            text = load_pdf(file_path)

            documents.append({
                "file_name": file_name,
                "text": text
            })

    return documents


def create_chunks(
    text,
    chunk_size=500,
    chunk_overlap=50
):

    chunks = []

    start = 0

    while start < len(text):

        end = start + chunk_size

        chunk = text[start:end].strip()

        if chunk:
            chunks.append(chunk)

        start = end - chunk_overlap

    return chunks