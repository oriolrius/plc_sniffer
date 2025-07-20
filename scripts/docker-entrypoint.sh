#!/bin/sh
set -e

# This script handles running the sniffer with proper capabilities

# When running with privileged: true, we can run as root directly
# This avoids issues with capability handling
if [ "$RUN_AS_ROOT" = "true" ] || [ "$(id -u)" = "0" ]; then
    # Running as root - needed for packet capture
    exec "$@"
else
    # Already running as non-root
    echo "Warning: Running as non-root user may cause permission issues with packet capture"
    exec "$@"
fi