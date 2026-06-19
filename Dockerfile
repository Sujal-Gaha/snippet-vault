FROM python:3.11-slim

# Prevent Python from writing pyc files to disc and buffering stdout/stderr
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

WORKDIR /app

# Install runtime dependencies (curl is used by Streamlit container health check)
RUN apt-get update && apt-get install -y --no-install-recommends \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Install Python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application source code
COPY . .

# Expose port for Streamlit
EXPOSE 1234

# Health check to ensure the service is running
HEALTHCHECK CMD curl --fail http://localhost:1234/_stcore/health || exit 1

# Configure container startup execution
ENTRYPOINT ["streamlit", "run", "app.py", "--server.port=1234", "--server.address=0.0.0.0"]
