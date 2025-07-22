import dspy
import dspy.signatures

lm = dspy.MockLM(logsprobs=True)

dspy.configure(lm=lm)


class QA(dspy.signature):
    question: str
    answer: str

qa = dspy.Predict(QA)

result = qa(question="What is the capital of India?")

print("Answer:", result.answer)  