from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from . import models, database, preprocess, model_loader
from .database import PredictionLog, get_db, create_tables

app = FastAPI(title="Titanic Survival API")

create_tables()

@app.get("/")
def root():
    return {"message": "Titanic Survival API is running"}

@app.post("/predict", response_model=models.PredictionResponse)
def predict(passenger: models.Passenger, db: Session = Depends(get_db)):
    try:
        X = preprocess.prepare_features(passenger.model_dump())
        proba = model_loader.stacking_clf.predict_proba(X)[0, 1]
        survived = int(proba >= 0.5)

        log = PredictionLog(
            pclass=passenger.Pclass,
            sex=passenger.Sex,
            age=passenger.Age,
            sibsp=passenger.SibSp,
            parch=passenger.Parch,
            fare=passenger.Fare,
            embarked=passenger.Embarked,
            name=passenger.Name,
            survived_pred=survived,
            probability=float(proba),
        )
        db.add(log)
        db.commit()

        return {"survived": survived, "probability": float(proba)}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))