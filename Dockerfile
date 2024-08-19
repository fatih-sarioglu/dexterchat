ARG PYTHON_VERSION=3.11.9
FROM python:${PYTHON_VERSION}-slim as base

RUN apt-get update && apt-get install -y \
    build-essential \
    software-properties-common \
    git \
    && rm -rf /var/lib/apt/lists/*

COPY . /app

WORKDIR /app

EXPOSE 8501
    
RUN pip3 install --no-cache-dir -r requirements.txt

ENTRYPOINT ["streamlit", "run", "app.py", "--server.port=8501", "--server.address=0.0.0.0"]