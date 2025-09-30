# Integration and Deployment Flow

This document outlines the complete integration and deployment workflow for the Jules orchestration system. It covers device identity validation, LiteWriter synchronization, reverse proxy setup, alerting, and a multi-stage deployment process.

---

## 🔗 Part 1: Integration Flow

This section details how Jules integrates with other critical services to form a cohesive system.

### 1. Device Identity Validation

To ensure that only authorized devices can interact with the system, Jules must validate requests against a known Android build fingerprint.

-   **Mechanism**: The build fingerprint should be passed as a custom HTTP header (e.g., `X-Device-Fingerprint`) with every request to a secured endpoint.
-   **Storage**: The authorized device fingerprint(s) should be stored securely in an `.env` file or a dedicated secrets management service (like AWS Secrets Manager or HashiCorp Vault).
    ```
    # .env file
    AUTHORIZED_FINGERPRINT="your_android_build_fingerprint_here"
    ```
-   **Implementation**: A middleware layer in the FastAPI application will intercept incoming requests, extract the fingerprint from the header, and compare it against the stored value. Unauthorized requests will be rejected with a `403 Forbidden` status.

### 2. LiteWriter Synchronization

Jules is responsible for triggering note synchronization with LiteWriter. This can be achieved through two primary methods:

-   **File Change (Webhook)**:
    -   A file watcher service (like `watchdog` in Python) monitors the notes directory for any changes.
    -   Upon detecting a change, Jules triggers a webhook or API call to the LiteWriter service to initiate a sync.
-   **Scheduled (Cron Job)**:
    -   A cron job is configured to run at regular intervals (e.g., every 5 minutes).
    -   The job calls a dedicated endpoint in Jules (e.g., `/api/sync/litewriter`), which then pushes the latest notes to LiteWriter via its WebDAV or REST API.

### 3. Domain and Reverse Proxy

A reverse proxy (like Nginx or Caddy) is essential for routing traffic, enabling TLS, and load balancing.

-   **Routing**: The proxy will route all traffic from `https://your-domain.com/jules/*` to the running Jules Docker container.
-   **TLS/SSL**: Let's Encrypt should be used to provide free, automated TLS certificates, ensuring all communication is encrypted. Caddy has built-in support for this, while Nginx can be configured with `certbot`.
-   **Sample Nginx Configuration**:
    ```nginx
    server {
        listen 80;
        server_name your-domain.com;
        return 301 https://$host$request_uri;
    }

    server {
        listen 443 ssl;
        server_name your-domain.com;

        ssl_certificate /etc/letsencrypt/live/your-domain.com/fullchain.pem;
        ssl_certificate_key /etc/letsencrypt/live/your-domain.com/privkey.pem;

        location /jules/ {
            proxy_pass http://localhost:8080/; # Assuming Jules runs on port 8080
            proxy_set_header Host $host;
            proxy_set_header X-Real-IP $remote_addr;
            proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        }
    }
    ```

### 4. Alerting

A robust alerting system is crucial for monitoring the health of the system and responding to issues quickly.

-   **Mechanism**: Jules will send webhooks to a designated channel (e.g., Telegram, Slack, or email via a service like SendGrid).
-   **Triggers**: Alerts should be configured for the following events:
    -   **Container Crash**: A lightweight external service or a Docker health check can trigger an alert if the Jules container goes down.
    -   **Sync Failure**: If the LiteWriter sync process fails repeatedly, an alert should be sent with the error details.
    -   **Authentication Mismatch**: Any unauthorized access attempt (i.e., a request with an invalid device fingerprint) should trigger a security alert.

---

## 🚀 Part 2: Deployment Flow

This section outlines the step-by-step process for deploying updates to Jules, from pre-merge checks to production monitoring.

### 1. Pre-Merge Checks

Before any new code is merged into the `main` branch, it must pass a series of automated checks.

-   **Build Test**: Build the Docker image without using the cache to ensure it can be built from scratch.
    ```bash
    docker build --no-cache -t jules:test .
    ```
-   **Integration Tests**: Run a suite of integration tests that verify the interactions between Jules, LiteWriter, and the domain/reverse proxy setup. These tests should be run against a staging environment.

### 2. Staging Deployment

Once pre-merge checks pass, the code is deployed to a staging environment that mirrors production as closely as possible.

-   **Deployment**: The `jules:test` Docker image is deployed to a staging subdomain (e.g., `staging.your-domain.com`).
-   **Validation**:
    -   Manually and automatically validate the device identity authentication flow.
    -   Trigger and verify the LiteWriter sync process.
    -   Run the `health_check.sh` script to ensure all services are healthy.

### 3. Production Merge and Deploy

After successful staging validation, the code is merged into the `main` branch and deployed to production.

-   **Tagging**: Create a new Git tag for the release to mark a stable version.
    ```bash
    git tag v1.0.0
    git push origin --tags
    ```
-   **Zero-Downtime Deployment**: Use a strategy that ensures the service remains available during the update. With `docker-compose`, this can be achieved with:
    ```bash
    docker-compose up -d --no-deps --build jules
    ```
    This command rebuilds and replaces only the `jules` service without affecting other linked services.

### 4. Post-Merge Monitoring

After deployment, the system should be closely monitored to ensure stability and performance.

-   **Log Monitoring**: Watch the container logs for any unusual errors or warnings for at least 24 hours post-deployment.
    ```bash
    docker logs -f jules
    ```
-   **Alert Verification**: Manually trigger a test alert to confirm that the alerting system is functioning correctly.
-   **Performance Metrics**: Monitor key performance indicators (KPIs) like CPU usage, memory consumption, and response times to ensure the new deployment has not introduced any regressions.