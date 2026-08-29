from rag import get_rag_response


question = input("Enter your question: ")


answer = get_rag_response(question)


print()
print("========== ANSWER ==========")
print(answer)