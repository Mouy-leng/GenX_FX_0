# Use a slim Debian base image
FROM debian:bullseye-slim

# Set the working directory
WORKDIR /app

# Avoid prompts from apt
ENV DEBIAN_FRONTEND=noninteractive

# Install base dependencies, including Node.js (for firebase-tools) and gnupg (for gh)
RUN apt-get update && \
    apt-get install -y --no-install-recommends \
    curl \
    openssl \
    msmtp \
    davfs2 \
    gnupg \
    ca-certificates \
    npm && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

# Install the GitHub CLI (gh)
RUN curl -fsSL https://cli.github.com/packages/githubcli-archive-keyring.gpg | dd of=/usr/share/keyrings/githubcli-archive-keyring.gpg && \
    chmod go+r /usr/share/keyrings/githubcli-archive-keyring.gpg && \
    echo "deb [arch=$(dpkg --print-architecture) signed-by=/usr/share/keyrings/githubcli-archive-keyring.gpg] https://cli.github.com/packages stable main" > /etc/apt/sources.list.d/github-cli.list && \
    apt-get update && \
    apt-get install -y gh && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

# Install firebase-tools globally using npm
RUN npm install -g firebase-tools

# Copy the orchestration script into the container
COPY jules.sh .

# Make the script executable
RUN chmod +x jules.sh

# Set the entrypoint to the script
ENTRYPOINT ["/bin/bash", "/app/jules.sh"]

# Default command is to show usage
CMD ["help"]