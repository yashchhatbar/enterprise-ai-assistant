
# Multi-stage Dockerfile

# Base Stage
FROM python:3.9-slim as base
WORKDIR /app
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Install system dependencies (for FAISS/OpenCV if needed)
RUN apt-get update && apt-get install -y \
    build-essential \
    libgl1-mesa-glx \
    && rm -rf /var/lib/apt/lists/*

# Copy Project Files
COPY . /app/

# Backend Stage
FROM base as backend
WORKDIR /app
RUN pip install --no-cache-dir -r backend/requirements.txt
EXPOSE 8000
CMD ["uvicorn", "backend.main:app", "--host", "0.0.0.0", "--port", "8000"]

# Frontend Stage
FROM base as frontend
WORKDIR /app
RUN pip install --no-cache-dir -r frontend/requirements.txt
EXPOSE 8501
CMD ["streamlit", "run", "frontend/app.py", "--server.port=8501", "--server.address=0.0.0.0"]
