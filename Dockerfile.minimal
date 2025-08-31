# Alternative Dockerfile - Ultra-minimal approach
FROM python:3.11-slim

# Set working directory
WORKDIR /app

# Copy minimal requirements
COPY requirements-minimal-docker.txt requirements.txt

# Install Python dependencies
RUN pip install --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY . .

# Create necessary directories
RUN mkdir -p uploads processed face_data

# Expose port
EXPOSE 5000

# Run the application with basic Flask server
CMD ["python", "-m", "flask", "run", "--host=0.0.0.0", "--port=5000"]
