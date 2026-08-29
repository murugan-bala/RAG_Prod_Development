from search_faiss import search_faiss
from llm import generate_answer


def get_rag_response(question):

    # Search relevant chunks
    results = search_faiss(question)

    # Combine chunks
    context = "\n\n".join(results)

    # Generate answer using OpenAI
    answer = generate_answer(
        question,
        context
    )

    return answer


'''def get_rag_response(question: str) -> str:

    return f"RAG response will come here for: {question}"'''