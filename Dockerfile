# Use the official Playwright image (includes Node + Python + Browsers)
FROM mcr.microsoft.com/playwright/python:v1.51.1-jammy

# Set the working directory
WORKDIR /app

# Copy requirements and install
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy your code
COPY . .

# Install Playwright dependencies and browsers
RUN playwright install

# Set the entrypoint
CMD ["python", "monitor.py"]
