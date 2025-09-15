FROM nvidia/cuda:12.1.1-runtime-ubuntu22.04

RUN apt update && apt install -y python3-pip git && rm -rf /var/lib/apt/lists/*
WORKDIR /app

RUN pip3 install torch transformers accelerate fastapi uvicorn

COPY ./download_model.py .
RUN python3 download_model.py

COPY ./api.py .

CMD ["uvicorn", "api:app", "--host", "0.0.0.0", "--port", "8000"]
