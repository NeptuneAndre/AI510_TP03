from fastapi import FastAPI
import joblib
import pandas as pd

app = FastAPI()

# Load the trained model
model = joblib.load("model.pkl")

@app.post("/predict")
async def predict(features: dict):
    data = pd.DataFrame([features])
    prediction = model.predict(data)
    return {"prediction": prediction[0]}
