def chunk_text(text, chunk_size=500, overlap=100):
    """
    Split text into overlapping chunks.

    chunk_size: maximum number of characters in each chunk
    overlap: number of characters shared between consecutive chunks
    """

    chunks = []

    start = 0

    while start < len(text):

        end = start + chunk_size

        chunk = text[start:end].strip()

        if chunk:
            chunks.append(chunk)

        start += chunk_size - overlap

    return chunks