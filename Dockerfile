# Stage 1: Build the frontend
FROM node:18-alpine AS frontend-builder

WORKDIR /app

# Copy package files and install dependencies
COPY package*.json ./
RUN npm install

# Copy client and shared source code
COPY client/ ./client
COPY shared/ ./shared
COPY tsconfig.json ./

# Build the client application
RUN npm run build

# Stage 2: Build the backend
FROM python:3.10-slim

WORKDIR /app

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Install Python dependencies
COPY requirements.txt .
RUN python -m pip install --no-cache-dir -r requirements.txt

# Copy the rest of the application code
COPY . .

# Copy the built frontend from the builder stage
COPY --from=frontend-builder /app/client/dist ./client/dist
COPY --from=frontend-builder /app/node_modules ./node_modules

# Create a non-root user
RUN adduser -u 5678 --disabled-password --gecos "" appuser
USER appuser

# Copy the startup script and make it executable
COPY start-prod.sh .
RUN chmod +x start-prod.sh

# Expose the port and run the application
EXPOSE 8080
CMD ["./start-prod.sh"]