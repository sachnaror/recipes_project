#!/bin/bash

echo "Starting Django Application Deployment..."

# Ask for details
read -p "Enter your name: " name
read -p "Enter the application name: " app_name
read -p "Enter user ID: " user_id
read -p "Is the application public or private (public/private): " app_type

# Generate necessary files
python3 generate_files.py

# Build Docker image
echo "Building Docker image..."
docker-compose build

# Start Docker containers
echo "Starting application in Docker..."
docker-compose up -d

# Get the running container's IP and port
echo "Your app is being deployed..."
container_id=$(docker ps -q --filter "ancestor=my_django_app_web")

# Extract IP address (assuming Docker is running on localhost)
app_url="http://localhost:8000"

echo "Deployment successful!"
echo "Your Django app is running at $app_url"
