FROM python:3.10-slim

WORKDIR /app

# Copy requirements file and install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY . .

# Create volume mount point for persistent data
VOLUME /app/news

# Expose port for Streamlit
EXPOSE 8501

# Set environment variables
ENV PYTHONUNBUFFERED=1

# Default command - can be overridden in docker-compose.yml
CMD ["streamlit", "run", "gui.py"]
