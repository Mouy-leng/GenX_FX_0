#!/bin/bash

# --- Orchestration Health Check Script ---
# This script checks the health of the Jules orchestration system,
# including Docker containers, logs, and critical endpoints.

# --- Configuration ---
# Use environment variables for configuration with fallback to default values.
JULES_DOMAIN=${JULES_DOMAIN:-"your-domain.com"}
LITEWRITER_DOMAIN=${LITEWRITER_DOMAIN:-"your-domain.com"}
JULES_CONTAINER_NAME=${JULES_CONTAINER_NAME:-"jules"}

echo "--- Starting Orchestration Health Check ---"
echo "Using the following configuration:"
echo "Jules Domain: $JULES_DOMAIN"
echo "LiteWriter Domain: $LITEWRITER_DOMAIN"
echo "Jules Container Name: $JULES_CONTAINER_NAME"
echo ""

# 1. Check Docker Container Health
echo "--- 1. Checking Docker Container Health ---"
docker ps --format "table {{.Names}}\t{{.Status}}\t{{.Ports}}"
echo ""

# 2. Inspect Logs for Jules
echo "--- 2. Inspecting Logs for Jules ---"
echo "Fetching the last 50 lines of logs for container: $JULES_CONTAINER_NAME"
docker logs --tail=50 $JULES_CONTAINER_NAME
echo ""

# 3. Verify Reverse Proxy + Jules Health Endpoints
echo "--- 3. Verifying Reverse Proxy and Health Endpoints ---"
HEALTH_URL="https://${JULES_DOMAIN}/jules/health"
echo "Pinging Jules health endpoint: $HEALTH_URL"
# Use curl -I to get headers, and grep to check for a 200 OK status.
if curl -I --silent "$HEALTH_URL" | grep -q "HTTP/2 200"; then
    echo "✅  Success: Received 200 OK from Jules health endpoint."
else
    echo "❌  Failure: Did not receive 200 OK from Jules health endpoint."
fi
echo ""

# 4. Check LiteWriter Sync Trigger
echo "--- 4. Checking LiteWriter Sync Trigger ---"
LITEWRITER_URL="https://${LITEWRITER_DOMAIN}/litewriter/status"
echo "Pinging LiteWriter status endpoint: $LITEWRITER_URL"
# Use curl -s to get the body, and jq to check for a valid JSON response.
if curl -s "$LITEWRITER_URL" | jq .; then
    echo "✅  Success: Received valid JSON response from LiteWriter status endpoint."
else
    echo "❌  Failure: Did not receive a valid JSON response from LiteWriter."
fi
echo ""

echo "--- Health Check Complete ---"