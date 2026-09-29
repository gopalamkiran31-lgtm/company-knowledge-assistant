from utils.embedding import create_embeddings


chunks = [
    {
        "file_name": "test.pdf",
        "chunk": "Employees are allowed 12 casual leaves per year."
    },
    {
        "file_name": "test.pdf",
        "chunk": "The probation period is six months."
    }
]


embeddings = create_embeddings(chunks)

print("Embedding shape:", embeddings.shape)
print("Number of chunks:", len(embeddings))