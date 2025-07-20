"""Unit tests for configuration module."""

import os
import pytest
from unittest.mock import patch

from plc_sniffer.config import SnifferConfig, ConfigManager
from plc_sniffer.validators import ValidationError


class TestSnifferConfig:
    """Test SnifferConfig dataclass."""
    
    def test_valid_config_creation(self):
        config = SnifferConfig(
            interface="eth0",
            filter="udp",
            destination_ip="127.0.0.1",
            destination_port=8514,
            log_level="INFO",
            max_packet_size=65535,
            rate_limit=1000
        )
        
        assert config.interface == "eth0"
        assert config.filter == "udp"
        assert config.destination_ip == "127.0.0.1"
        assert config.destination_port == 8514
        assert config.log_level == "INFO"
        assert config.max_packet_size == 65535
        assert config.rate_limit == 1000
        assert config.socket_timeout == 5.0
    
    def test_invalid_config_validation(self):
        with pytest.raises(ValidationError):
            SnifferConfig(
                interface="invalid$interface",
                filter="udp",
                destination_ip="127.0.0.1",
                destination_port=8514,
                log_level="INFO"
            )
        
        with pytest.raises(ValidationError):
            SnifferConfig(
                interface="eth0",
                filter="udp",
                destination_ip="invalid-ip",
                destination_port=8514,
                log_level="INFO"
            )
    
    def test_invalid_socket_timeout(self):
        with pytest.raises(ValidationError):
            SnifferConfig(
                interface="eth0",
                filter="udp",
                destination_ip="127.0.0.1",
                destination_port=8514,
                log_level="INFO",
                socket_timeout=-1.0
            )


class TestConfigManager:
    """Test ConfigManager functionality."""
    
    def test_from_environment_defaults(self):
        with patch.dict(os.environ, {}, clear=True):
            config = ConfigManager.from_environment()
            
            assert config.interface == "eth0"
            assert config.filter == "udp"
            assert config.destination_ip == "127.0.0.1"
            assert config.destination_port == 8514
            assert config.log_level == "INFO"
            assert config.max_packet_size == 65535
            assert config.rate_limit == 0
    
    def test_from_environment_custom(self):
        env_vars = {
            'INTERFACE': 'wlan0',
            'FILTER': 'tcp port 80',
            'DESTINATION_IP': '192.168.1.100',
            'DESTINATION_PORT': '9999',
            'LOG_LEVEL': 'DEBUG',
            'MAX_PACKET_SIZE': '1500',
            'RATE_LIMIT': '5000',
            'SOCKET_TIMEOUT': '10.0'
        }
        
        with patch.dict(os.environ, env_vars, clear=True):
            config = ConfigManager.from_environment()
            
            assert config.interface == "wlan0"
            assert config.filter == "tcp port 80"
            assert config.destination_ip == "192.168.1.100"
            assert config.destination_port == 9999
            assert config.log_level == "DEBUG"
            assert config.max_packet_size == 1500
            assert config.rate_limit == 5000
            assert config.socket_timeout == 10.0
    
    def test_from_environment_invalid(self):
        with patch.dict(os.environ, {'DESTINATION_PORT': 'not-a-number'}, clear=True):
            with pytest.raises(ValidationError):
                ConfigManager.from_environment()
    
    def test_from_dict(self):
        config_dict = {
            'interface': 'eth1',
            'filter': 'udp port 514',
            'destination_ip': '10.0.0.1',
            'destination_port': 514,
            'log_level': 'ERROR',
            'max_packet_size': 9000,
            'rate_limit': 2000
        }
        
        config = ConfigManager.from_dict(config_dict)
        
        assert config.interface == "eth1"
        assert config.filter == "udp port 514"
        assert config.destination_ip == "10.0.0.1"
        assert config.destination_port == 514
        assert config.log_level == "ERROR"
        assert config.max_packet_size == 9000
        assert config.rate_limit == 2000