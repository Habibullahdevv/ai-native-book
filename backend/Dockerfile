# Hugging Face Spaces Dockerfile for FastAPI backend
FROM python:3.11-slim

# Set working directory
WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    gcc \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements first for better caching
COPY requirements.txt .

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY app.py .

# Create non-root user for HF Spaces
RUN useradd -m -u 1000 user
USER user

# Expose port (HF Spaces uses 7860)
EXPOSE 7860

# Run the application
CMD ["python", "app.py"]
