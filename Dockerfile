FROM python:3.10-slim

WORKDIR /app

# Install system dependencies for Playwright
RUN apt-get update && apt-get install -y \
    libnss3 \
    libnspr4 \
    libatk1.0-0 \
    libatk-bridge2.0-0 \
    libcups2 \
    libxkbcommon0 \
    libatspi2.0-0 \
    libxcomposite1 \
    libxdamage1 \
    libxfixes3 \
    libxrandr2 \
    libgbm1 \
    libpango-1.0-0 \
    libcairo2 \
    libasound2 \
    wget \
    ca-certificates \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements file and install Python dependencies (except Playwright)
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Install Playwright and browsers separately
RUN pip install --no-cache-dir playwright
RUN playwright install

# Copy application code
COPY . .

# Create volume mount point for persistent data
VOLUME /app/news

# Expose port for Streamlit
EXPOSE 8501

# Set environment variables
ENV PYTHONUNBUFFERED=1

# Default command
CMD ["streamlit", "run", "gui.py"]
