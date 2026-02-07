# Base Image
FROM python:3.10-slim

# Set Working Directory
WORKDIR /app

# Install Dependencies
RUN pip install requests

# Copy Source Code
COPY script.py .

# Run the Application
CMD ["python", "-u", "script.py"]
