import numpy as np
from sklearn.metrics.pairwise import cosine_similarity


def semantic_search(
    question_embedding,
    chunk_embeddings,
    chunks,
    top_k=3
):
    """
    Find the most relevant document chunks
    using cosine similarity.
    """

    if len(chunks) == 0:
        return []

    if len(chunk_embeddings) == 0:
        return []

    # Calculate similarity between question and all chunks
    similarities = cosine_similarity(
        question_embedding.reshape(1, -1),
        chunk_embeddings
    )[0]

    # Get indices of highest similarity scores
    top_indices = np.argsort(similarities)[::-1][:top_k]

    results = []

    for index in top_indices:

        results.append({
            "file_name": chunks[index]["file_name"],
            "chunk": chunks[index]["chunk"],
            "score": float(similarities[index])
        })

    return results