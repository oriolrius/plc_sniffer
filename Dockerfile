# Multi-stage build for security and size optimization
FROM python:3.13-slim AS builder

# Install build dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    gcc \
    g++ \
    libpcap-dev \
    && rm -rf /var/lib/apt/lists/*

# Create virtual environment
RUN python -m venv /opt/venv
ENV PATH="/opt/venv/bin:$PATH"

# Copy and install dependencies
WORKDIR /build
COPY pyproject.toml ./
COPY src ./src
RUN pip install --upgrade pip setuptools wheel && \
    pip install --no-cache-dir .

# Final stage
FROM python:3.13-slim

# Install runtime dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    libpcap0.8 \
    libpcap-dev \
    tcpdump \
    && rm -rf /var/lib/apt/lists/* \
    && pip uninstall -y setuptools || true

# Copy virtual environment from builder
COPY --from=builder /opt/venv /opt/venv
ENV PATH="/opt/venv/bin:$PATH"

# Create non-root user
RUN groupadd -g 1000 sniffer && \
    useradd -u 1000 -g sniffer -s /bin/bash -m sniffer

# Create app directory
WORKDIR /app

# Copy entrypoint script
COPY --chown=sniffer:sniffer scripts/docker-entrypoint.sh /usr/local/bin/

# Make entrypoint executable
RUN chmod +x /usr/local/bin/docker-entrypoint.sh

# Set environment defaults
ENV INTERFACE=eth0 \
    FILTER="udp" \
    DESTINATION_IP=127.0.0.1 \
    DESTINATION_PORT=8514 \
    LOG_LEVEL=INFO \
    MAX_PACKET_SIZE=65535 \
    RATE_LIMIT=0

# Health check
HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 \
    CMD python -c "import socket; s=socket.socket(); s.settimeout(1); s.connect(('localhost', 8080)); s.close()"

# Run as root when privileged mode is needed for packet capture
# USER sniffer  # Commented out - run as root for packet capture

# Force Scapy to use pcapy
ENV SCAPY_USE_PCAPDNET=no

# Use custom entrypoint for capability handling
ENTRYPOINT ["/usr/local/bin/docker-entrypoint.sh"]
CMD ["python", "-m", "plc_sniffer"]