# Use a Python base image
FROM python:3.12-slim

# Set working directory
WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    libgl1 \
    libglib2.0-0 \
    && rm -rf /var/lib/apt/lists/*

# Copy application files
COPY . /app

# Install Python dependencies
RUN pip install --default-timeout=100 -i https://pypi.tuna.tsinghua.edu.cn/simple flask opencv-python pillow




# Expose the port
EXPOSE 5000

# Run the Flask app
CMD ["python", "app.py"]
