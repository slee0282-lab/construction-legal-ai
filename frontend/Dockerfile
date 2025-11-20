# Use Python 3.12 as the base image
FROM python:3.12-slim

# Set environment variables
ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1

# Set working directory
WORKDIR /app

# Install dependencies
RUN pip install --no-cache-dir streamlit requests

# Copy source code
COPY src ./src

# Expose port
EXPOSE 8501

# Run the application
CMD ["streamlit", "run", "src/app.py", "--server.address=0.0.0.0"]
