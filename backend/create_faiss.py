import os
import pickle

import faiss
import numpy as np
from sentence_transformers import SentenceTransformer

from document_loader import load_pdf, create_chunks


PDF_PATH = "../documents/Config steps - FernTel IP Phones.pdf"
FAISS_FOLDER = "../vector_db/faiss_index"


# Load embedding model
model = SentenceTransformer("all-MiniLM-L6-v2")


def create_embeddings(chunks):
    embeddings = model.encode(
        chunks,
        convert_to_numpy=True,
        show_progress_bar=True
    )

    return np.asarray(
        embeddings,
        dtype="float32"
    )


def main():

    print("Loading PDF...")

    text = load_pdf(PDF_PATH)

    print("Creating chunks...")

    chunks = create_chunks(
        text,
        chunk_size=500,
        chunk_overlap=50
    )

    print("Number of chunks:", len(chunks))

    print("Creating embeddings...")

    embeddings = create_embeddings(chunks)

    print("Embedding shape:", embeddings.shape)

    # Get embedding dimension
    dimension = embeddings.shape[1]

    # Create FAISS index
    index = faiss.IndexFlatL2(dimension)

    # Add embeddings
    index.add(embeddings)

    # Create folder
    os.makedirs(FAISS_FOLDER, exist_ok=True)

    # Save FAISS index
    faiss.write_index(
        index,
        f"{FAISS_FOLDER}/index.faiss"
    )

    # Save chunks
    with open(
        f"{FAISS_FOLDER}/chunks.pkl",
        "wb"
    ) as file:

        pickle.dump(chunks, file)

    print("FAISS index created successfully.")


if __name__ == "__main__":
    main()

