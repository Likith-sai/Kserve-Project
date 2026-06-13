import mlflow
import os
import mlflow.sklearn

mlflow.set_tracking_uri('http://127.0.0.1:5000')
model = mlflow.sklearn.load_model("models:/kubeflow_churn_classifier@champion")
mlflow.sklearn.save_model(model, path="exported_model")
print("Model is saved to ./exported_model/")