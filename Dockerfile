# Use an official Python runtime as a parent image
FROM python:3.9-slim

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Set work directory
WORKDIR /app

# Install system dependencies (if any are needed later, e.g., for psycopg2)
# RUN apt-get update && apt-get install -y --no-install-recommends some-package

# Install Python dependencies
COPY requirements.txt /app/
RUN pip install --no-cache-dir -r requirements.txt

# Copy project code
COPY . /app/

# Change working directory to where manage.py is
WORKDIR /app/bus_ticketing_project

# Collect static files
RUN python manage.py collectstatic --noinput --clear

# Expose port 8000
EXPOSE 8000

# Run gunicorn
# The CMD should be structured to allow for overriding from `docker run`
CMD ["gunicorn", "--bind", "0.0.0.0:8000", "bus_ticketing_project.wsgi:application"]
