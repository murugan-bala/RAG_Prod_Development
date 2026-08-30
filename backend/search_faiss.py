import pickle

import faiss
import numpy as np
from sentence_transformers import SentenceTransformer


FAISS_INDEX_PATH = "../vector_db/faiss_index/index.faiss"
CHUNKS_PATH = "../vector_db/faiss_index/chunks.pkl"
METADATA_PATH = "../vector_db/faiss_index/metadata.pkl"

TOP_K = 3


# Load embedding model
model = SentenceTransformer("all-MiniLM-L6-v2")


# Load FAISS index
index = faiss.read_index(
    FAISS_INDEX_PATH
)


# Load chunks
with open(CHUNKS_PATH, "rb") as file:
    chunks = pickle.load(file)


# Load metadata
with open(METADATA_PATH, "rb") as file:
    metadata = pickle.load(file)


def search_faiss(question):

    # Create embedding for the question
    question_embedding = model.encode(
        [question],
        convert_to_numpy=True
    )

    question_embedding = np.asarray(
        question_embedding,
        dtype="float32"
    )

    # Normalize for cosine similarity
    faiss.normalize_L2(
        question_embedding
    )

    # Search FAISS
    scores, indices = index.search(
        question_embedding,
        TOP_K
    )

    results = []

    for score, index_id in zip(
        scores[0],
        indices[0]
    ):

        if index_id < len(metadata):

            results.append({
                "file_name": metadata[index_id]["file_name"],
                "chunk": metadata[index_id]["chunk"],
                "score": float(score)
            })

    return results


if __name__ == "__main__":

    question = input(
        "Enter your question: "
    )

    results = search_faiss(question)

    print()
    print("========== SEARCH RESULTS ==========")

    for i, result in enumerate(
        results,
        start=1
    ):

        print()
        print("Result:", i)
        print("PDF:", result["file_name"])
        print("Score:", result["score"])
        print("--------------------")
        print(result["chunk"])