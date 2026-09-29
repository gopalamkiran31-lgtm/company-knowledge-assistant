from sentence_transformers import SentenceTransformer


# Load the embedding model once
model = SentenceTransformer("all-MiniLM-L6-v2")


def create_embeddings(chunks):
    """
    Create embeddings for document chunks.
    """

    if not chunks:
        return []

    texts = [item["chunk"] for item in chunks]

    embeddings = model.encode(
        texts,
        convert_to_numpy=True
    )

    return embeddings


def create_question_embedding(question):
    """
    Create an embedding for the user's question.
    """

    return model.encode(
        question,
        convert_to_numpy=True
    )