# Dockerfile

FROM python:3.10-slim

WORKDIR /app

COPY . /app

# 🛠️ Install system-level dependencies
RUN apt-get update && apt-get install -y \
    ffmpeg libsndfile1 espeak \
    && pip install --no-cache-dir -r requirements.txt

EXPOSE 8501

CMD ["streamlit", "run", "smartvoice_app.py", "--server.port=8501", "--server.address=0.0.0.0"]