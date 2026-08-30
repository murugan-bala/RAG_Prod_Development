from search_faiss import search_faiss
from llm import generate_answer, generate_normal_answer


SIMILARITY_THRESHOLD = 0.70


def get_response(question):

    results = search_faiss(question)

    best_score = results[0]["score"]

    print("Best similarity score:", best_score)

    if best_score >= SIMILARITY_THRESHOLD:

        print("Routing to RAG")

        context = "\n\n".join(
            result["chunk"]
            for result in results
        )

        answer = generate_answer(
            question,
            context
        )

        return {
            "answer": answer,
            "sources": results
        }

    else:

        print("Routing to normal LLM")

        answer = generate_normal_answer(
            question
        )

        return {
            "answer": answer,
            "sources": []
        }