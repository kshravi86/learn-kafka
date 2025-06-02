# Use an official Python runtime as a parent image
FROM python:3.9-slim

# Set the working directory in the container
WORKDIR /app

# Copy the dependencies file to the working directory
COPY requirements.txt .

# Install any needed dependencies specified in requirements.txt
# Using --no-cache-dir to reduce image size
RUN pip install --no-cache-dir -r requirements.txt

# Copy the application code to the working directory
COPY ./main.py .
COPY ./models.py .
COPY ./auth.py .
COPY ./database.py .

# Make port 8000 available to the world outside this container
EXPOSE 8000

# Define environment variable (optional, can be used in CMD)
# ENV PORT 8000
# For simplicity, directly using 8000 in CMD

# Run the FastAPI application with Uvicorn when the container launches
# Use 0.0.0.0 to make it accessible from outside the container
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
