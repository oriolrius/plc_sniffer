"""Configuration management for PLC Sniffer."""

import os
from dataclasses import dataclass
from typing import Optional

from .validators import (
    validate_bpf_filter,
    validate_interface,
    validate_ip_address,
    validate_log_level,
    validate_packet_size,
    validate_port,
    validate_rate_limit,
    ValidationError
)


@dataclass
class SnifferConfig:
    """Configuration for PLC Sniffer."""
    
    interface: str
    filter: str
    destination_ip: str
    destination_port: int
    log_level: str
    max_packet_size: int = 65535
    rate_limit: int = 0  # 0 means no limit
    socket_timeout: float = 5.0
    
    def __post_init__(self):
        """Validate configuration after initialization."""
        self.interface = validate_interface(self.interface)
        self.filter = validate_bpf_filter(self.filter)
        self.destination_ip = validate_ip_address(self.destination_ip)
        self.destination_port = validate_port(self.destination_port)
        self.log_level = validate_log_level(self.log_level)
        self.max_packet_size = validate_packet_size(self.max_packet_size)
        self.rate_limit = validate_rate_limit(self.rate_limit)
        
        if self.socket_timeout <= 0:
            raise ValidationError("Socket timeout must be positive")


class ConfigManager:
    """Manages configuration loading and validation."""
    
    @staticmethod
    def from_environment() -> SnifferConfig:
        """Load configuration from environment variables.
        
        Returns:
            Validated SnifferConfig instance
            
        Raises:
            ValidationError: If any configuration value is invalid
        """
        try:
            config = SnifferConfig(
                interface=os.environ.get('INTERFACE', 'eth0'),
                filter=os.environ.get('FILTER', 'udp'),
                destination_ip=os.environ.get('DESTINATION_IP', '127.0.0.1'),
                destination_port=int(os.environ.get('DESTINATION_PORT', '8514')),
                log_level=os.environ.get('LOG_LEVEL', 'INFO'),
                max_packet_size=int(os.environ.get('MAX_PACKET_SIZE', '65535')),
                rate_limit=int(os.environ.get('RATE_LIMIT', '0')),
                socket_timeout=float(os.environ.get('SOCKET_TIMEOUT', '5.0'))
            )
            return config
        except ValueError as e:
            raise ValidationError(f"Configuration error: {e}")
    
    @staticmethod
    def from_dict(config_dict: dict) -> SnifferConfig:
        """Create configuration from dictionary.
        
        Args:
            config_dict: Dictionary with configuration values
            
        Returns:
            Validated SnifferConfig instance
            
        Raises:
            ValidationError: If any configuration value is invalid
        """
        return SnifferConfig(**config_dict)