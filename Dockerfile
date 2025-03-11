# Use lightweight Python image
FROM python:3.11

# Set working directory
WORKDIR /app

# Copy and install dependencies
COPY requirements.txt .
RUN pip install -r requirements.txt

# Copy all Python files
COPY . .

# Run script
CMD ["python", "main.py"]
