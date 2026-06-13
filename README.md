# KServe Churn Classifier 🚀

A production-ready machine learning model serving platform built with **KServe**, **MLflow**, and **FastAPI** for predicting customer churn.

---

## 📋 Table of Contents

- [Overview](#overview)
- [Architecture](#architecture)
- [Project Structure](#project-structure)
- [Quick Start](#quick-start)
- [Usage](#usage)
- [Deployment](#deployment)
- [Model Information](#model-information)
- [API Reference](#api-reference)
- [Contributing](#contributing)

---

## 🎯 Overview

This project provides a containerized ML model serving application that:
- **Pre-Requisite** You should have already experiment tracking on mlflow(could be locally or cloud). If it is in cloud. kindly change the experiment_uri tracking in model.py
- **Loads pre-trained models** from MLflow Model Registry
- **Serves predictions** via REST API using FastAPI
- **Runs on Kubernetes** via KServe InferenceService
- **Scales automatically** with industry-standard MLOps practices

### Key Features
✅ Fast, scalable inference with FastAPI  
✅ Model versioning via MLflow  
✅ Kubernetes-native deployment  
✅ Docker containerization  
✅ RESTful API with health checks  
✅ Production-ready logging  

---

## 🏗️ Architecture

### System Overview

```mermaid
graph TB
    MLFlow[("MLflow Registry<br/>Model Store")]
    Client["Client<br/>Application"]
    LoadBal["Load Balancer"]
    KServe["KServe InferenceService"]
    Container["Container<br/>FastAPI + Uvicorn"]
    Model["ML Model<br/>sklearn/xgboost"]
    
    MLFlow -->|Load Model| Container
    Client -->|HTTP Request| LoadBal
    LoadBal -->|Route| KServe
    KServe -->|Manage| Container
    Container -->|Predict| Model
    
    style MLFlow fill:#4A90E2
    style Client fill:#7ED321
    style LoadBal fill:#F5A623
    style KServe fill:#BD10E0
    style Container fill:#50E3C2
    style Model fill:#B8E986
```

### Request-Response Flow

```mermaid
sequenceDiagram
    participant Client
    participant API as FastAPI<br/>Server
    participant MLFlow
    participant Model as ML Model
    
    Client->>API: POST /v1/models/churn-classifier:predict
    API->>MLFlow: Load Model (on startup)
    MLFlow-->>API: Model Ready
    Client->>API: JSON: instances
    API->>Model: predict(data)
    Model-->>API: predictions
    API-->>Client: JSON: predictions
```

---

## 📁 Project Structure

```mermaid
graph LR
    Root["Kserve-Project/"]
    
    Root --> Serve["serve.py<br/>FastAPI App"]
    Root --> Model["model.py<br/>Model Export"]
    Root --> Docker["Dockerfile<br/>Container Image"]
    Root --> Config["inference.yaml<br/>K8s Config"]
    Root --> Req["requirements.txt<br/>Dependencies"]
    Root --> Payload["payload.json<br/>Test Data"]
    Root --> Helpers["get_col.py<br/>get_sample.py<br/>Utilities"]
    Root --> ExpModel["exported_model/<br/>MLflow Model"]
    Root --> Env["export_venv/<br/>Virtual Env"]
    
    style Root fill:#FFE6E6
    style Serve fill:#B3E5FC
    style Model fill:#C8E6C9
    style Docker fill:#F8BBD0
    style Config fill:#FFECB3
    style ExpModel fill:#D1C4E9
```

---

## 🚀 Quick Start

### 1. **Install Dependencies**

```bash
cd Kserve-Project
pip install -r requirements.txt
```

### 2. **Setup MLflow Connection**

Ensure MLflow server is running:
```bash
mlflow server --port 5000
```

### 3. **Export Model from MLflow**

```bash
python model.py
```

This loads the champion model from MLflow and exports it locally.

### 4. **Run the Server Locally**

```bash
python serve.py
```

Server starts on `http://localhost:8080`

### 5. **Test Prediction**

```bash
curl -X POST http://localhost:8080/v1/models/churn-classifier:predict \
  -H "Content-Type: application/json" \
  -d @payload.json
```

---

## 💡 Usage

### Health Check

```bash
curl http://localhost:8080/health
```

Response:
```json
{"status": "ok"}
```

### Make Predictions

**Endpoint:** `POST /v1/models/churn-classifier:predict`

**Request Format:**
```json
{
  "instances": [
    [
      "customer123",
      "Male",
      0,
      "Yes",
      "No",
      24,
      "Yes",
      "Yes",
      "Fiber optic",
      "Yes",
      "No",
      "Yes",
      "Yes",
      "Yes",
      "No",
      "Month-to-month",
      "Yes",
      "Credit card",
      65.50,
      1570.40
    ]
  ]
}
```

**Response:**
```json
{
  "predictions": [1]
}
```

---

## 🐳 Docker Deployment

### Build Docker Image

```bash
docker build -t churn-classifier:v8 .
```

### Run Container

```bash
docker run -p 8080:8080 \
  -v $(pwd)/exported_model:/mnt/models \
  churn-classifier:v8
```

---

## ☸️ Kubernetes Deployment

### Deploy with KServe

```bash
kubectl apply -f inference.yaml
```

### Monitor Deployment

```bash
kubectl get inferenceservice -n kserve
kubectl logs -f deployment/churn-classifier -n kserve
```

### Make Predictions (Kubernetes)

```bash
kubectl port-forward -n kserve service/churn-classifier 8080:8080
```

Then use the same prediction endpoint.

---

## 📊 Model Information

### Model Details

| Property | Value |
|----------|-------|
| **Name** | kubeflow_churn_classifier |
| **Framework** | scikit-learn / XGBoost |
| **Input Features** | 20 customer attributes |
| **Output** | Binary classification (Churn: 0/1) |
| **Registry** | MLflow Model Registry |
| **Stage** | Champion |

### Input Features

```
customerID, gender, SeniorCitizen, Partner, Dependents,
tenure, PhoneService, MultipleLines, InternetService,
OnlineSecurity, OnlineBackup, DeviceProtection, TechSupport,
StreamingTV, StreamingMovies, Contract, PaperlessBilling,
PaymentMethod, MonthlyCharges, TotalCharges
```

### Model Pipeline

```mermaid
flowchart LR
    Input["Customer Data<br/>20 Features"] 
    Preprocess["Data Preprocessing<br/>Feature Scaling"]
    Model["ML Model<br/>sklearn/xgboost"]
    Output["Prediction<br/>Churn Probability"]
    
    Input -->|Clean| Preprocess
    Preprocess -->|Transform| Model
    Model -->|Inference| Output
    
    style Input fill:#E8F5E9
    style Preprocess fill:#FFF3E0
    style Model fill:#F3E5F5
    style Output fill:#E0F2F1
```

---

## 📡 API Reference

### Endpoints

#### 1. Health Check
- **Method:** `GET`
- **Path:** `/health`
- **Response:** `{"status": "ok"}`

#### 2. Predictions
- **Method:** `POST`
- **Path:** `/v1/models/churn-classifier:predict`
- **Content-Type:** `application/json`
- **Body:** See [Usage](#usage) section

---

## 📚 Utility Scripts

### `get_col.py`
Extracts feature columns from data.

### `get_sample.py`
Generates sample data for testing.

### `model.py`
Exports the champion model from MLflow to local storage.

---

## 🔧 Configuration

### inference.yaml
KServe InferenceService configuration:
- **Image:** `churn-classifier:v8`
- **Port:** `8080`
- **CPU Request:** `100m` / Limit: `500m`
- **Memory Request:** `256Mi` / Limit: `512Mi`

### requirements.txt
Key dependencies:
```
mlflow          - Model registry and tracking
fastapi         - Web framework
uvicorn         - ASGI server
pandas          - Data processing
scikit-learn    - ML framework
xgboost         - Gradient boosting
```

---

## 🐛 Troubleshooting

| Issue | Solution |
|-------|----------|
| Model not found | Ensure MLflow server is running on port 5000 |
| Port 8080 in use | Change port in `serve.py` or stop other services |
| Container fails to start | Check Docker volume mount: `-v $(pwd)/exported_model:/mnt/models` |
| Slow predictions | Verify model is loaded (check logs) |

---

## 📝 License

This project is part of the MLOps Orchestration suite.

---

## 👥 Contributing

1. Create a feature branch
2. Make your changes
3. Test locally
4. Submit a pull request

---

## 📞 Support

For issues or questions, check the logs:
```bash
docker logs <container_id>
# or
kubectl logs -f deployment/churn-classifier -n kserve
```

---

**Last Updated:** June 2026  
**Status:** Production Ready ✅
