from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_predict_valid():
    payload = {
        "Pclass": 1,
        "Sex": "female",
        "Age": 30.0,
        "SibSp": 0,
        "Parch": 0,
        "Fare": 100.0,
        "Embarked": "C",
        "Name": "Test, Mrs. John"
    }
    response = client.post("/predict", json=payload)
    assert response.status_code == 200
    data = response.json()
    assert "survived" in data
    assert "probability" in data
    assert 0 <= data["probability"] <= 1

def test_predict_invalid():
    response = client.post("/predict", json={"Pclass": 5})
    assert response.status_code == 422