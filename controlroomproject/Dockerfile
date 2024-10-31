# Use the official Python image
FROM python:3.13-alpine

ENV DJANGO_SETTINGS_MODULE=controlroomproject.settings_prod

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Set the working directory
WORKDIR /controlroomproject

# Install system dependencies including Node.js and npm
RUN apk add --no-cache \
    postgresql-client \
    netcat-openbsd \
    nodejs \
    npm \
    build-base \
    python3-dev \
    libffi-dev

# Install Python dependencies
COPY requirements.txt /controlroomproject/
RUN pip install -r requirements.txt

# Copy the Django application code
COPY . /controlroomproject/

# Install and build Tailwind CSS
RUN python manage.py tailwind install
RUN python manage.py tailwind build

# Create necessary directories
RUN mkdir -p /controlroomproject/staticfiles

# Expose the Django port
EXPOSE 8000

# Start Django server
CMD ["gunicorn", "--bind", "0.0.0.0:8000", "app.wsgi:application"]
