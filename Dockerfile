# Use the official Python image as the base image
FROM python:3.9-slim

# Set the working directory in the container
WORKDIR /app

# Copy the content of the local src directory to the working directory
COPY ./app /app 

# Install any dependencies
RUN pip install --no-cache-dir -r requirements.txt 

# Command to run the application
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--reload"]
