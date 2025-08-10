# Use an official Python runtime as the base image
FROM python:3.9-slim

# Set the working directory in the container
WORKDIR /app

# Copy the current directory contents into the container at /app
COPY . /app

# Set permissions for /app to ensure it is writable
RUN chmod -R 777 /app

# Install curl and any needed packages specified in requirements.txt
RUN apt-get update && apt-get install -y curl && rm -rf /var/lib/apt/lists/* \
    && pip install --no-cache-dir -r requirements.txt

# Make port 5000 available to the world outside this container
EXPOSE 5000

# Health check to ensure the service is running properly
HEALTHCHECK --interval=1m --timeout=10s --start-period=30s --retries=3 \
    CMD curl -f http://localhost:5000/health || exit 1

# Run the application with Flask binding to 0.0.0.0
CMD ["flask", "run", "--host=0.0.0.0", "--port=5000"]
