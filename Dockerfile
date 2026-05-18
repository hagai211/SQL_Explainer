# Start from the official slim Python 3.12 image
FROM python:3.12-slim

# Set the working directory inside the container
WORKDIR /app

# Copy requirements first so Docker can cache this layer
COPY requirements.txt .

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the project into the container
COPY . .

# Default command: run the explainer with any argument passed to docker run
ENTRYPOINT ["python", "explain.py"]
