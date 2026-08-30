import os
import pickle

import faiss
import numpy as np
from sentence_transformers import SentenceTransformer

from document_loader import (
    load_all_pdfs,
    create_chunks
)


DOCUMENTS_FOLDER = "../documents"
FAISS_FOLDER = "../vector_db/faiss_index"


model = SentenceTransformer(
    "all-MiniLM-L6-v2"
)


def create_embeddings(chunks):

    embeddings = model.encode(
        chunks,
        convert_to_numpy=True,
        show_progress_bar=True
    )

    embeddings = np.asarray(
        embeddings,
        dtype="float32"
    )

    faiss.normalize_L2(
        embeddings
    )

    return embeddings


def main():

    print("Loading PDF documents...")

    documents = load_all_pdfs(
        DOCUMENTS_FOLDER
    )

    all_chunks = []
    metadata = []

    for document in documents:

        file_name = document["file_name"]
        text = document["text"]

        chunks = create_chunks(
            text,
            chunk_size=500,
            chunk_overlap=50
        )

        print(
            file_name,
            "->",
            len(chunks),
            "chunks"
        )

        for chunk in chunks:

            all_chunks.append(chunk)

            metadata.append({
                "file_name": file_name,
                "chunk": chunk
            })

    print()
    print(
        "Total chunks:",
        len(all_chunks)
    )

    print()
    print("Creating embeddings...")

    embeddings = create_embeddings(
        all_chunks
    )

    print(
        "Embedding shape:",
        embeddings.shape
    )

    dimension = embeddings.shape[1]

    index = faiss.IndexFlatIP(
        dimension
    )

    index.add(
        embeddings
    )

    os.makedirs(
        FAISS_FOLDER,
        exist_ok=True
    )

    faiss.write_index(
        index,
        f"{FAISS_FOLDER}/index.faiss"
    )

    with open(
        f"{FAISS_FOLDER}/chunks.pkl",
        "wb"
    ) as file:

        pickle.dump(
            all_chunks,
            file
        )

    with open(
        f"{FAISS_FOLDER}/metadata.pkl",
        "wb"
    ) as file:

        pickle.dump(
            metadata,
            file
        )

    print()
    print(
        "FAISS index created successfully."
    )


if __name__ == "__main__":
    main()