FROM python:3.11-slim

# Set working directory
WORKDIR /app

# Copy requirements and install
COPY requirements.txt .
RUN pip install --no-cache-dir --upgrade -r requirements.txt

# Copy the actual app folder
COPY PowerFIServer/ PowerFIServer/

# Set PYTHONPATH to current workdir so Python can find PowerFIServer
ENV PYTHONPATH=/app

# Run using uvicorn
CMD ["uvicorn", "PowerFIServer.server.main:app", "--host", "0.0.0.0", "--port", "80"]
