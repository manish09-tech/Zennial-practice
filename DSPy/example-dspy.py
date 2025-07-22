import dspy

class MyMockLM(dspy.LanguageModel):
    def __init__(self):
        super().__init__()
        
        def __call__(self, prompt, **kwargs):
            print("Mock LM called with prompt:", prompt)
            return "Mocked response" 
        
        
dspy.configure(lm=MyMockLM())


class QA(dspy.signature):
    question: str
    answer: str

qa = dspy.Predict(QA)

result = qa(question="What is the capital of India?")

print("Answer:", result.answer)  