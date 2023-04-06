# Use the official Python 3.9 image as the base image
FROM python:3.9.15

# Set the working directory
WORKDIR /app

# Install required system dependencies
RUN apt-get update && \
    apt-get install -y --no-install-recommends \
    libopenmpi-dev g++ && \
    rm -rf /var/lib/apt/lists/*

# Copy the requirements file
COPY requirements_docker.txt .

# Install the dependencies
RUN pip install -r requirements_docker.txt

# Copy the rest of the application
COPY . .

# Create a simulation data directory
RUN mkdir -p /app/simulation_data

# Set the default command to run your application
CMD ["python", "src/MultiCLI/MultiCli.py"]
