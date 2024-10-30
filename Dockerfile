# Dockerfile
FROM python:3.12-slim

# Set the working directory
WORKDIR /receipe_project

# Copy requirements.txt and install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Collect static files
RUN python manage.py collectstatic --noinput

# Copy the rest of the application
COPY . .

# Expose the app's port
EXPOSE 8000

# Run the Django app
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]
