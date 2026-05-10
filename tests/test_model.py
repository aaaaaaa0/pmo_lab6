from app.model_loader import full_pipeline, scaler, stacking_clf, feature_names
from app.preprocess import prepare_features

def test_pipeline_loaded():
    assert full_pipeline is not None
    assert scaler is not None
    assert stacking_clf is not None
    assert feature_names is not None

def test_preprocess():
    sample = {
        "Pclass": 2,
        "Sex": "male",
        "Age": 25.0,
        "SibSp": 1,
        "Parch": 0,
        "Fare": 20.0,
        "Embarked": "S",
        "Name": "Sample, Mr. Test"
    }
    X = prepare_features(sample)
    assert X.shape[1] == len(feature_names)