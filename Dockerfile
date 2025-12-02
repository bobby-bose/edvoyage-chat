# Use Python 3.11 slim image
FROM python:3.11-slim

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Set work directory
WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    gcc \
    postgresql-client \
    && rm -rf /var/lib/apt/lists/*

# Install Python dependencies
COPY requirements.txt /app/
RUN pip install --upgrade pip && pip install -r requirements.txt

# Install gunicorn for production
RUN pip install gunicorn whitenoise

# Copy project files
COPY . /app/

# Collect static files
RUN python manage.py collectstatic --noinput

# Create media directory
RUN mkdir -p /app/media/chat_images

# Expose port
EXPOSE 8000

# Run migrations and start gunicorn
CMD python manage.py migrate && \
    gunicorn chatserver.wsgi:application --bind 0.0.0.0:8000 --workers 3
