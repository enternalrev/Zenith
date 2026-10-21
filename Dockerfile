FROM python:3.12-slim

# System deps: ffmpeg for pydub, gcc for compiling some Python packages
RUN apt-get update && apt-get install -y \
    ffmpeg \
    gcc \
    python3-dev \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

# Copy requirements first to leverage Docker layer cache
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy your main script (rename to match your actual file)
COPY main.py .

# Start command (rename to match your actual file)
CMD ["python", "main.py"]
