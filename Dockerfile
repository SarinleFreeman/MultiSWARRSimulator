# Use the official Python 3.9 image as the base image
FROM python:3.9.15

# Set the working directory
WORKDIR /app

# Copy the requirements file
COPY requirements.txt .

# Install the dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the application
COPY . .

# Set the default command to run your application
CMD ["python", "main.py"]
