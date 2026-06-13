import mlflow
import pandas as pd
from fastapi import FastAPI, Request
import uvicorn
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI()

logger.info("Loading Model...")
model = mlflow.sklearn.load_model("/mnt/models")
logger.info("Model loaded successfully")

COLOUMNS = [
    "customerID", "gender", "SeniorCitizen", "Partner", "Dependents",
    "tenure", "PhoneService", "MultipleLines", "InternetService",
    "OnlineSecurity", "OnlineBackup", "DeviceProtection", "TechSupport",
    "StreamingTV", "StreamingMovies", "Contract", "PaperlessBilling",
    "PaymentMethod", "MonthlyCharges", "TotalCharges"
]

@app.get("/health")
def health():
    return {"status": "ok"}
@app.post("/v1/models/churn-classifier:predict")
async def predict(request: Request):
    body = await request.json()
    instances = body["instances"]

    df = pd.DataFrame(instances, columns=COLOUMNS[:len(instances[0])])
    predictions = model.predict(df)

    return {"predictions": predictions.tolist()}

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8080)