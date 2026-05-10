import joblib
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent
MODEL_DIR = BASE_DIR / "models"

# загрузка всего пайплайна
full_pipeline = joblib.load(MODEL_DIR / "titanic_stacking_pipeline.pkl")

# извлекаются отдельно scaler и модель
scaler = full_pipeline.named_steps['scaler']
stacking_clf = full_pipeline.named_steps['stacking']

# остальные артефакты
feature_names = joblib.load(MODEL_DIR / "feature_names.pkl")
age_medians = joblib.load(MODEL_DIR / "age_medians.pkl")
fare_99th = joblib.load(MODEL_DIR / "fare_99th.pkl")
fare_quantiles = joblib.load(MODEL_DIR / "fare_quantiles.pkl")