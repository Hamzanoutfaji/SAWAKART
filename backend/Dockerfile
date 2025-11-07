# Use a slim Python base
FROM python:3.13-slim

# Install system dependencies required by Playwright
RUN apt-get update && apt-get install -y \
    libgtk-4-1 libgraphene-1.0-0 libgstreamer-gl1.0-0 \
    libgstreamer-plugins-base1.0-0 libenchant-2-2 \
    libsecret-1-0 libmanette-0.2-0 libgles2-mesa curl wget gnupg \
    && rm -rf /var/lib/apt/lists/*

# Set working directory
WORKDIR /app

# Copy requirements and install Python deps
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Install Playwright browsers
RUN python -m playwright install

# Copy all project files
COPY . .

# Expose the port your FastAPI uses
EXPOSE 10000

# Run the app
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "10000"]
