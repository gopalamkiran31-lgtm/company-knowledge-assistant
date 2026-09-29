import os

from dotenv import load_dotenv
from groq import Groq


# Load environment variables
load_dotenv()

api_key = os.getenv("GROQ_API_KEY")

if not api_key:
    raise ValueError(
        "GROQ_API_KEY is not configured in the .env file."
    )

client = Groq(api_key=api_key)


def get_answer(question, context):
    """
    Generate an answer using only the retrieved document context.
    """

    prompt = f"""
You are a Company Knowledge Assistant.

Answer the user's question using ONLY the information
provided in the document context below.

If the answer is not available in the context, say:

"I could not find this information in the uploaded documents."

Do not use outside knowledge.
Do not make up information.

Document Context:
{context}

User Question:
{question}

Answer:
"""

    response = client.chat.completions.create(
        model="openai/gpt-oss-120b",
        messages=[
            {
                "role": "system",
                "content": (
                    "You answer questions strictly using "
                    "the provided document context."
                )
            },
            {
                "role": "user",
                "content": prompt
            }
        ],
        temperature=0
    )

    return response.choices[0].message.content