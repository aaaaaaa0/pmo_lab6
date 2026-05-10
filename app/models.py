from pydantic import BaseModel

class Passenger(BaseModel):
    Pclass: int
    Sex: str
    Age: float
    SibSp: int
    Parch: int
    Fare: float
    Embarked: str
    Name: str

class PredictionResponse(BaseModel):
    survived: int
    probability: float