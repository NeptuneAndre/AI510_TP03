import joblib
import pandas as pd

def init():
    global model
    model = joblib.load("random_forest_model.pkl")

def run(data):
    try:
        data = pd.DataFrame(data)
        predictions = model.predict(data)
        return {"predictions": predictions.tolist()}
    except Exception as e:
        return {"error": str(e)}
