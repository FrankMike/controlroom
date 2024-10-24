# Use an official Python runtime as the base image
FROM python:3.12.5-alpine

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Set the working directory in the container
WORKDIR /app

# Install system dependencies
RUN apk add --no-cache gcc musl-dev linux-headers

# Install Python dependencies
COPY requirements.txt /app/
RUN pip install --no-cache-dir -r requirements.txt

# Copy the current directory contents into the container at /app
COPY . /app

# Collect static files
RUN python manage.py collectstatic --noinput

# Run migrations
RUN python manage.py migrate

# Create a non-root user and switch to it
RUN adduser -D francesco
USER francesco

# Make port 80 available to the world outside this container
EXPOSE 80

# Use Gunicorn to run the application
CMD ["gunicorn", "--bind", "0.0.0.0:80", "controlroomproject.wsgi:application"]
