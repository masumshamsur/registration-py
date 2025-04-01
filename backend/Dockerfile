# Use official Python image
FROM python:3.10

# Set working directory
WORKDIR /app

# Copy the requirements.txt file into the container
COPY requirements.txt /app/

# Install dependencies
RUN pip install --no-cache-dir -r /app/requirements.txt

# Copy the source code and configuration files into the container
COPY src/ /app/src/
COPY config/ /app/config/

# Expose backend API port
EXPOSE 8000

# Run FastAPI app
CMD ["uvicorn", "src.app:app", "--host", "0.0.0.0", "--port", "8000"]


