"""Input validation for PLC Sniffer configuration."""

import ipaddress
import re
from typing import Any, Union


class ValidationError(Exception):
    """Raised when validation fails."""
    pass


def validate_ip_address(ip: str) -> str:
    """Validate IP address format.
    
    Args:
        ip: IP address string to validate
        
    Returns:
        Validated IP address string
        
    Raises:
        ValidationError: If IP address format is invalid
    """
    try:
        ipaddress.ip_address(ip)
        return ip
    except ValueError as e:
        raise ValidationError(f"Invalid IP address '{ip}': {e}")


def validate_port(port: Union[str, int]) -> int:
    """Validate port number is in valid range.
    
    Args:
        port: Port number to validate
        
    Returns:
        Validated port number as integer
        
    Raises:
        ValidationError: If port is not in valid range (1-65535)
    """
    try:
        port_int = int(port)
        if not 1 <= port_int <= 65535:
            raise ValidationError(f"Port {port_int} is not in valid range (1-65535)")
        return port_int
    except ValueError:
        raise ValidationError(f"Invalid port number '{port}'")


def validate_interface(interface: str) -> str:
    """Validate network interface name.
    
    Args:
        interface: Network interface name
        
    Returns:
        Validated interface name
        
    Raises:
        ValidationError: If interface name contains invalid characters
    """
    # Interface names should be alphanumeric with some special chars
    pattern = r'^[a-zA-Z0-9\-_.]+$'
    if not re.match(pattern, interface):
        raise ValidationError(
            f"Invalid interface name '{interface}': "
            "must contain only alphanumeric characters, hyphens, dots, and underscores"
        )
    
    # Check length constraints
    if len(interface) > 15:  # Linux interface name limit
        raise ValidationError(f"Interface name '{interface}' too long (max 15 characters)")
    
    return interface


def validate_bpf_filter(filter_str: str) -> str:
    """Basic validation of BPF filter syntax.
    
    Args:
        filter_str: BPF filter string
        
    Returns:
        Validated filter string
        
    Raises:
        ValidationError: If filter contains obvious syntax errors
    """
    if not filter_str.strip():
        raise ValidationError("BPF filter cannot be empty")
    
    # Check for balanced parentheses
    paren_count = 0
    for char in filter_str:
        if char == '(':
            paren_count += 1
        elif char == ')':
            paren_count -= 1
        if paren_count < 0:
            raise ValidationError("Unbalanced parentheses in BPF filter")
    
    if paren_count != 0:
        raise ValidationError("Unbalanced parentheses in BPF filter")
    
    # Check for common BPF keywords to ensure it's likely a valid filter
    bpf_keywords = ['udp', 'tcp', 'icmp', 'ip', 'host', 'port', 'net', 'src', 'dst', 'and', 'or', 'not']
    filter_lower = filter_str.lower()
    
    if not any(keyword in filter_lower for keyword in bpf_keywords):
        raise ValidationError(
            f"BPF filter '{filter_str}' doesn't contain any recognized keywords"
        )
    
    return filter_str


def validate_log_level(level: str) -> str:
    """Validate logging level.
    
    Args:
        level: Logging level string
        
    Returns:
        Validated and uppercased log level
        
    Raises:
        ValidationError: If log level is not valid
    """
    valid_levels = {'DEBUG', 'INFO', 'WARNING', 'ERROR', 'CRITICAL'}
    level_upper = level.upper()
    
    if level_upper not in valid_levels:
        raise ValidationError(
            f"Invalid log level '{level}'. "
            f"Must be one of: {', '.join(sorted(valid_levels))}"
        )
    
    return level_upper


def validate_packet_size(size: int) -> int:
    """Validate packet size limit.
    
    Args:
        size: Maximum packet size in bytes
        
    Returns:
        Validated packet size
        
    Raises:
        ValidationError: If size is invalid
    """
    min_size = 64  # Minimum Ethernet frame size
    max_size = 65535  # Maximum UDP packet size
    
    if not isinstance(size, int):
        raise ValidationError(f"Packet size must be an integer, got {type(size)}")
    
    if not min_size <= size <= max_size:
        raise ValidationError(
            f"Packet size {size} is not in valid range ({min_size}-{max_size})"
        )
    
    return size


def validate_rate_limit(rate: Union[str, int]) -> int:
    """Validate rate limit (packets per second).
    
    Args:
        rate: Rate limit value
        
    Returns:
        Validated rate limit as integer
        
    Raises:
        ValidationError: If rate is invalid
    """
    try:
        rate_int = int(rate)
        if rate_int < 0:
            raise ValidationError("Rate limit cannot be negative")
        if rate_int > 1000000:  # Sanity check - 1M pps
            raise ValidationError("Rate limit too high (max 1000000 pps)")
        return rate_int
    except ValueError:
        raise ValidationError(f"Invalid rate limit '{rate}'")