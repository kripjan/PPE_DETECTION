FROM python:3.11-slim

# Set working directory
WORKDIR /app

# Copy application code to container
COPY . /app/

# Install required system libraries for PostgreSQL
RUN apt-get update && apt-get install -y libpq-dev \
    && rm -rf /var/lib/apt/lists/*

# Install Python dependencies
RUN pip install --upgrade pip
RUN pip install -r requirements.txt

# Expose Flask port
EXPOSE 5000

# Command to run the application
CMD ["python", "run.py"]

