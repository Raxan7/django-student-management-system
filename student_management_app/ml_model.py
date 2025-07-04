import os
import joblib  # Use joblib or pickle to load your model

# from Iris.Iris.settings import BASE_DIR
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent


def load_model():
    model_path = os.path.join(BASE_DIR, "student_management_app/my_model.pkl")
    model = joblib.load(model_path)  # Replace with your model file
    return model
