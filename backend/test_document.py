from document_loader import load_pdf, create_chunks


pdf_path = "../documents/Config steps - FernTel IP Phones.pdf"


text = load_pdf(pdf_path)

print("========== PDF TEXT ==========")
print(text)


chunks = create_chunks(
    text,
    chunk_size=500,
    chunk_overlap=50
)


print()
print("========== CHUNKS ==========")


for i, chunk in enumerate(chunks, start=1):

    print()
    print("Chunk", i)
    print("--------------------")
    print(chunk)