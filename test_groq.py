
from utils.groq_helper import get_answer


question = "How many casual leaves can an employee take?"

context = """
Employees are allowed 12 casual leaves per year.
"""


answer = get_answer(
    question,
    context
)

print("Answer:")
print(answer)