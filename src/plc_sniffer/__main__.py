"""Main entry point for PLC Sniffer."""

import sys
import signal
import logging
import os
from typing import Optional

from .config import ConfigManager, ValidationError
from .sniffer import PlcSniffer
from .health import HealthCheckServer


logger = logging.getLogger(__name__)
sniffer: Optional[PlcSniffer] = None
health_server: Optional[HealthCheckServer] = None


def signal_handler(signum, frame):
    """Handle shutdown signals gracefully."""
    logger.info(f"Received signal {signum}, shutting down...")
    if health_server:
        health_server.stop()
    if sniffer:
        sniffer.stop()
    sys.exit(0)


def main():
    """Main entry point."""
    global sniffer, health_server
    
    # Register signal handlers
    signal.signal(signal.SIGINT, signal_handler)
    signal.signal(signal.SIGTERM, signal_handler)
    
    try:
        # Load configuration
        config = ConfigManager.from_environment()
        
        # Create sniffer
        sniffer = PlcSniffer(config)
        
        # Start health check server if enabled
        health_port = int(os.environ.get('HEALTH_CHECK_PORT', '8080'))
        if health_port > 0:
            health_server = HealthCheckServer(port=health_port)
            health_server.start(sniffer)
        
        # Start sniffing
        sniffer.start()
        
    except ValidationError as e:
        logger.error(f"Configuration error: {e}")
        sys.exit(1)
    except Exception as e:
        logger.error(f"Unexpected error: {e}")
        sys.exit(1)
    finally:
        if health_server:
            health_server.stop()


if __name__ == "__main__":
    main()