# Stage 1: Builder
# This stage installs all dependencies, including build-time dependencies.
FROM python:3.13-slim as builder

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Install build essentials for packages that need compilation
RUN apt-get update && apt-get install -y --no-install-recommends build-essential

# Set the working directory
WORKDIR /app

# Copy the requirements lock file and install dependencies
COPY requirements.lock .
RUN pip install --no-cache-dir -r requirements.lock

# ---

# Stage 2: Production
# This stage creates the final, lightweight production image.
FROM python:3.13-slim as production

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Set the working directory
WORKDIR /app

# Create a non-root user for security
RUN adduser -u 5678 --disabled-password --gecos "" appuser

# Copy installed dependencies from the builder stage
COPY --from=builder /usr/local/lib/python3.13/site-packages /usr/local/lib/python3.13/site-packages
COPY --from=builder /usr/local/bin /usr/local/bin

# Copy the application code
COPY . .

# Change ownership of the app folder to the non-root user
RUN chown -R appuser:appuser /app

# Switch to the non-root user
USER appuser

# Expose the application port
EXPOSE 8080

# Define the command to run the application
CMD ["sh", "-c", "gunicorn -k uvicorn.workers.UvicornWorker --bind 0.0.0.0:${PORT:-8080} api.main:app"]