# Use a minimal Python image
FROM python:3.9-slim

# Set working directory inside container
WORKDIR /app

# Copy dependencies and install
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy app source code
COPY . .

# Expose Flask app port
EXPOSE 5000

# Run the app
CMD ["python", "app.py"]
