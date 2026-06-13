FROM python:3.10-slim

WORKDIR /app

RUN pip install --no-cache-dir \
    mlflow==3.13.0 \
    cloudpickle==3.1.2 \
    numpy==2.2.6 \
    pandas==2.3.3 \
    scikit-learn==1.6.1 \
    scipy==1.15.3 \
    fastapi==0.115.0 \
    uvicorn==0.30.0

COPY exported_model/ /mnt/models/
COPY serve.py /app/serve.py

EXPOSE 8080

CMD ["python", "serve.py"]