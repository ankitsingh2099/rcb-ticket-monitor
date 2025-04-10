# Use the official Playwright image (includes Node + Python + Browsers)
FROM mcr.microsoft.com/playwright/python:v1.42.0-jammy

# Set the working directory
WORKDIR /app

# Copy requirements and install
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy your code
COPY . .

# Install Playwright dependencies and browsers
RUN playwright install-deps

# Set the entrypoint
CMD ["python", "rcb.py"]
