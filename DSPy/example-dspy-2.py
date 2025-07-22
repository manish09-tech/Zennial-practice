import dspy 

class CarService (dspy.Predict):
    def __init__ (self):
        super().__init__(signature = "body_wash, stream, interior_clean -> done")

    def forward(self, body_wash: str, stream: str, interior_clean: str ) -> str:
        return f"Your car has been serviced with {body_wash}, {stream}, and {interior_clean}."
    

predictor = CarService()
response = predictor(body_wash= "cleansie foam", stream= "hot-air", interior_clean= "vacuum and polish")
print (response)