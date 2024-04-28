# Use the official Python base image
FROM python:3.9-slim

# Set the working directory to /app
WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    build-essential \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Copy the local files to the container
COPY . /app

# Install Python dependencies
RUN pip3 install -r requirements.txt

# Expose the port Streamlit will run on
EXPOSE 8501

# Healthcheck to ensure service is running
HEALTHCHECK CMD curl --fail http://localhost:8501/_stcore/health

# Run the Streamlit app
ENTRYPOINT ["streamlit", "run", "Home.py", "--server.port=8501", "--server.address=0.0.0.0"]
