# Use lightweight Python image
FROM python:3.11

# Set working directory
WORKDIR /app

# Copy and install dependencies
COPY requirements.txt .
RUN pip install --proxy=http://172.24.17.18:3228  -r requirements.txt

# Copy all Python files
COPY . .

ENV http_proxy="http://172.24.17.18:3228/"
ENV https_proxy="http://172.24.17.18:3228/"


# Run script
CMD ["python", "main.py"]
