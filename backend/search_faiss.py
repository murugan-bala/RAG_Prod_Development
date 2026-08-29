import pickle

import faiss
from sentence_transformers import SentenceTransformer


FAISS_INDEX_PATH = "../vector_db/faiss_index/index.faiss"
CHUNKS_PATH = "../vector_db/faiss_index/chunks.pkl"

TOP_K = 3


# Load embedding model
model = SentenceTransformer("all-MiniLM-L6-v2")


# Load FAISS index
index = faiss.read_index(FAISS_INDEX_PATH)


# Load original chunks
with open(CHUNKS_PATH, "rb") as file:
    chunks = pickle.load(file)


def search_faiss(question):

    # Convert question into embedding
    question_embedding = model.encode(
        [question],
        convert_to_numpy=True
    )

    # FAISS expects float32
    question_embedding = question_embedding.astype("float32")

    # Search
    distances, indices = index.search(
        question_embedding,
        TOP_K
    )

    results = []

    for i in indices[0]:

        if i < len(chunks):
            results.append(chunks[i])

    return results


if __name__ == "__main__":

    question = input("Enter your question: ")

    results = search_faiss(question)

    print("\n========== SEARCH RESULTS ==========\n")

    for i, result in enumerate(results, start=1):

        print(f"--- Result {i} ---")
        print(result)
        print()
    