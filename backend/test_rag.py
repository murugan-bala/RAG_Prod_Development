from rag import get_response


question = input("Enter your question: ")


answer = get_response(question)


print()
print("========== ANSWER ==========")
print(answer)