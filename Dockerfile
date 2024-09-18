# Use the official Python image
FROM python:3.10-slim

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Set working directory
WORKDIR /app

# Install dependencies
COPY requirements.txt /app/
RUN pip install --no-cache-dir -r requirements.txt

# Copy the current directory contents into the container
COPY . /app/

# Expose port 8000 for Django
EXPOSE 8000

# Start the Django application (you might need to adjust depending on your setup)
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]
