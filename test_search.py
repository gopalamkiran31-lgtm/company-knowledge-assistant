from utils.embedding import (
    create_embeddings,
    create_question_embedding
)

from utils.search import semantic_search


chunks = [
    {
        "file_name": "EmployeeHandbook.pdf",
        "chunk": "Employees are allowed 12 casual leaves per year."
    },
    {
        "file_name": "EmployeeHandbook.pdf",
        "chunk": "The probation period for new employees is six months."
    },
    {
        "file_name": "TrainingGuide.pdf",
        "chunk": "Employees must complete security training during onboarding."
    }
]


# Create document embeddings
embeddings = create_embeddings(chunks)


# User question
question = "How many casual leaves can an employee take?"


# Create question embedding
question_embedding = create_question_embedding(question)


# Search
results = semantic_search(
    question_embedding,
    embeddings,
    chunks,
    top_k=3
)


# Display results
for result in results:

    print("\nSource:", result["file_name"])

    print("Score:", result["score"])

    print("Chunk:", result["chunk"])