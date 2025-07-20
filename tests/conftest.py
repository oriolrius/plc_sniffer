"""Pytest configuration and fixtures."""

import pytest
from unittest.mock import Mock, patch

from plc_sniffer.config import SnifferConfig


@pytest.fixture
def valid_config():
    """Provide a valid configuration for testing."""
    return SnifferConfig(
        interface="eth0",
        filter="udp",
        destination_ip="127.0.0.1",
        destination_port=8514,
        log_level="INFO",
        max_packet_size=65535,
        rate_limit=1000,
        socket_timeout=5.0
    )


@pytest.fixture
def mock_socket():
    """Mock socket for testing."""
    with patch('socket.socket') as mock:
        socket_instance = Mock()
        mock.return_value = socket_instance
        yield socket_instance


@pytest.fixture
def mock_scapy_sniff():
    """Mock scapy sniff function."""
    with patch('plc_sniffer.sniffer.sniff') as mock:
        yield mock


@pytest.fixture
def sample_packet():
    """Create a sample packet for testing."""
    from scapy.all import IP, UDP, Raw, Ether
    
    packet = Ether() / IP(src="192.168.1.100", dst="192.168.1.200") / \
             UDP(sport=1234, dport=5678) / Raw(load=b"test payload")
    return packet