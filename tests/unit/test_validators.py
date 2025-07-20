"""Unit tests for validators module."""

import pytest

from plc_sniffer.validators import (
    ValidationError,
    validate_ip_address,
    validate_port,
    validate_interface,
    validate_bpf_filter,
    validate_log_level,
    validate_packet_size,
    validate_rate_limit
)


class TestIPAddressValidation:
    """Test IP address validation."""
    
    def test_valid_ipv4(self):
        assert validate_ip_address("192.168.1.1") == "192.168.1.1"
        assert validate_ip_address("10.0.0.0") == "10.0.0.0"
        assert validate_ip_address("255.255.255.255") == "255.255.255.255"
    
    def test_valid_ipv6(self):
        assert validate_ip_address("::1") == "::1"
        assert validate_ip_address("2001:db8::1") == "2001:db8::1"
    
    def test_invalid_ip(self):
        with pytest.raises(ValidationError):
            validate_ip_address("256.256.256.256")
        with pytest.raises(ValidationError):
            validate_ip_address("192.168.1")
        with pytest.raises(ValidationError):
            validate_ip_address("not-an-ip")


class TestPortValidation:
    """Test port number validation."""
    
    def test_valid_ports(self):
        assert validate_port(1) == 1
        assert validate_port(80) == 80
        assert validate_port(65535) == 65535
        assert validate_port("8080") == 8080
    
    def test_invalid_ports(self):
        with pytest.raises(ValidationError):
            validate_port(0)
        with pytest.raises(ValidationError):
            validate_port(65536)
        with pytest.raises(ValidationError):
            validate_port(-1)
        with pytest.raises(ValidationError):
            validate_port("not-a-port")


class TestInterfaceValidation:
    """Test network interface validation."""
    
    def test_valid_interfaces(self):
        assert validate_interface("eth0") == "eth0"
        assert validate_interface("wlan0") == "wlan0"
        assert validate_interface("en0") == "en0"
        assert validate_interface("docker0") == "docker0"
        assert validate_interface("veth.100") == "veth.100"
    
    def test_invalid_interfaces(self):
        with pytest.raises(ValidationError):
            validate_interface("eth0$")  # Invalid character
        with pytest.raises(ValidationError):
            validate_interface("interface with spaces")
        with pytest.raises(ValidationError):
            validate_interface("toolonginterfacename")  # > 15 chars
        with pytest.raises(ValidationError):
            validate_interface("")


class TestBPFFilterValidation:
    """Test BPF filter validation."""
    
    def test_valid_filters(self):
        assert validate_bpf_filter("udp") == "udp"
        assert validate_bpf_filter("tcp port 80") == "tcp port 80"
        assert validate_bpf_filter("host 192.168.1.1") == "host 192.168.1.1"
        assert validate_bpf_filter("(udp or tcp) and port 443") == "(udp or tcp) and port 443"
    
    def test_invalid_filters(self):
        with pytest.raises(ValidationError):
            validate_bpf_filter("")  # Empty
        with pytest.raises(ValidationError):
            validate_bpf_filter("((udp")  # Unbalanced parentheses
        with pytest.raises(ValidationError):
            validate_bpf_filter("random text")  # No BPF keywords


class TestLogLevelValidation:
    """Test log level validation."""
    
    def test_valid_levels(self):
        assert validate_log_level("DEBUG") == "DEBUG"
        assert validate_log_level("info") == "INFO"
        assert validate_log_level("Warning") == "WARNING"
        assert validate_log_level("ERROR") == "ERROR"
        assert validate_log_level("critical") == "CRITICAL"
    
    def test_invalid_levels(self):
        with pytest.raises(ValidationError):
            validate_log_level("TRACE")
        with pytest.raises(ValidationError):
            validate_log_level("invalid")
        with pytest.raises(ValidationError):
            validate_log_level("")


class TestPacketSizeValidation:
    """Test packet size validation."""
    
    def test_valid_sizes(self):
        assert validate_packet_size(64) == 64
        assert validate_packet_size(1500) == 1500
        assert validate_packet_size(65535) == 65535
    
    def test_invalid_sizes(self):
        with pytest.raises(ValidationError):
            validate_packet_size(63)  # Too small
        with pytest.raises(ValidationError):
            validate_packet_size(65536)  # Too large
        with pytest.raises(ValidationError):
            validate_packet_size("not-a-number")


class TestRateLimitValidation:
    """Test rate limit validation."""
    
    def test_valid_rates(self):
        assert validate_rate_limit(0) == 0  # No limit
        assert validate_rate_limit(1000) == 1000
        assert validate_rate_limit("5000") == 5000
        assert validate_rate_limit(1000000) == 1000000  # Max
    
    def test_invalid_rates(self):
        with pytest.raises(ValidationError):
            validate_rate_limit(-1)  # Negative
        with pytest.raises(ValidationError):
            validate_rate_limit(1000001)  # Too high
        with pytest.raises(ValidationError):
            validate_rate_limit("invalid")