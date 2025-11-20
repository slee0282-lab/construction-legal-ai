# Use Python 3.12 as the base image
FROM python:3.12-slim

# Set environment variables
ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    UV_SYSTEM_PYTHON=1

# Install system dependencies (if any needed)
RUN apt-get update && apt-get install -y --no-install-recommends \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Install uv
COPY --from=ghcr.io/astral-sh/uv:latest /uv /bin/uv

# Set working directory
WORKDIR /app

# Copy project configuration
COPY pyproject.toml ./

# Install dependencies
RUN uv sync --no-install-project

# Copy source code
COPY src ./src

# Expose port
EXPOSE 8000

# Run the application
# Assuming src/main.py has an app object. 
# If not, we might need to adjust. But based on README, it's src/main.py.
CMD ["uv", "run", "fastapi", "run", "src/main.py", "--port", "8000", "--host", "0.0.0.0"]
