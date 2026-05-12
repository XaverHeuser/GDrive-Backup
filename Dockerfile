FROM python:3.11-slim

WORKDIR /app

# Upgrade pip
RUN python -m pip install --no-cache-dir --upgrade "pip>=26.1"

# Install dependencies
COPY requirements.txt .
RUN python -m pip install --no-cache-dir -r requirements.txt

# Copy src folder
COPY src/ ./src/

# Copy main.py
COPY main.py .

# Start job
# ENV PYTHONPATH=. ensures that src is a modul
ENV PYTHONPATH=.
CMD ["python", "main.py"]