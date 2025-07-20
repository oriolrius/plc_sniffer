#!/bin/sh
set -e

# This script handles running the sniffer with proper capabilities
# when not running as root

# Check if we're running as root
if [ "$(id -u)" = "0" ]; then
    echo "Running as root, switching to sniffer user with capabilities..."
    
    # Grant necessary capabilities to python binary
    setcap cap_net_raw,cap_net_admin+eip /opt/venv/bin/python3
    
    # Switch to sniffer user
    exec su-exec sniffer "$@"
else
    # Already running as non-root
    exec "$@"
fi