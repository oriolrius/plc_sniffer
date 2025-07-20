"""Unit tests for sniffer module."""

import time
import socket
from unittest.mock import Mock, patch, call

import pytest

from plc_sniffer.sniffer import PlcSniffer, RateLimiter, PacketStats


class TestRateLimiter:
    """Test RateLimiter functionality."""
    
    def test_no_limit(self):
        limiter = RateLimiter(0)  # No limit
        for _ in range(100):
            assert limiter.allow() is True
    
    def test_rate_limiting(self):
        limiter = RateLimiter(10)  # 10 pps
        
        # Should allow initial burst
        allowed = 0
        for _ in range(20):
            if limiter.allow():
                allowed += 1
        
        # Should have allowed around 10 (bucket size)
        assert 8 <= allowed <= 12
    
    @patch('time.time')
    def test_token_refill(self, mock_time):
        mock_time.return_value = 0
        limiter = RateLimiter(10)
        
        # Use all tokens
        for _ in range(10):
            limiter.allow()
        
        # No tokens left
        assert limiter.allow() is False
        
        # Advance time by 0.5 seconds (should get 5 tokens)
        mock_time.return_value = 0.5
        
        allowed = 0
        for _ in range(10):
            if limiter.allow():
                allowed += 1
        
        assert allowed == 5


class TestPacketStats:
    """Test PacketStats functionality."""
    
    def test_record_packet(self):
        stats = PacketStats()
        
        stats.record_packet(forwarded=True, size=100)
        assert stats.packets_processed == 1
        assert stats.packets_forwarded == 1
        assert stats.bytes_forwarded == 100
        assert stats.packets_dropped == 0
        
        stats.record_packet(forwarded=False)
        assert stats.packets_processed == 2
        assert stats.packets_forwarded == 1
        assert stats.packets_dropped == 1
    
    @patch('time.time')
    def test_get_current_rate(self, mock_time):
        mock_time.return_value = 0
        stats = PacketStats(window_size=10)
        
        # Record 10 packets over 1 second
        for i in range(10):
            mock_time.return_value = i * 0.1
            stats.record_packet(forwarded=True)
        
        mock_time.return_value = 1.0
        rate = stats.get_current_rate()
        assert 9.5 <= rate <= 10.5  # ~10 pps


class TestPlcSniffer:
    """Test PlcSniffer functionality."""
    
    def test_initialization(self, valid_config):
        sniffer = PlcSniffer(valid_config)
        
        assert sniffer.config == valid_config
        assert sniffer.socket is None
        assert sniffer.running is False
        assert isinstance(sniffer.rate_limiter, RateLimiter)
        assert isinstance(sniffer.stats, PacketStats)
    
    def test_create_socket(self, valid_config):
        sniffer = PlcSniffer(valid_config)
        
        with patch('socket.socket') as mock_socket:
            sock_instance = Mock()
            mock_socket.return_value = sock_instance
            
            result = sniffer._create_socket()
            
            assert result == sock_instance
            mock_socket.assert_called_once_with(socket.AF_INET, socket.SOCK_DGRAM)
            sock_instance.settimeout.assert_called_once_with(5.0)
    
    def test_process_packet_rate_limited(self, valid_config, sample_packet):
        config = valid_config
        config.rate_limit = 1  # Very low rate
        sniffer = PlcSniffer(config)
        
        # Mock rate limiter to always deny
        sniffer.rate_limiter.allow = Mock(return_value=False)
        
        sniffer._process_packet(sample_packet)
        
        assert sniffer.stats.rate_limited == 1
        assert sniffer.stats.packets_processed == 1
        assert sniffer.stats.packets_forwarded == 0
    
    def test_process_packet_oversized(self, valid_config, sample_packet):
        config = valid_config
        config.max_packet_size = 10  # Very small limit
        sniffer = PlcSniffer(config)
        
        sniffer._process_packet(sample_packet)
        
        assert sniffer.stats.oversized == 1
        assert sniffer.stats.packets_processed == 1
        assert sniffer.stats.packets_forwarded == 0
    
    def test_process_packet_success(self, valid_config, sample_packet, mock_socket):
        sniffer = PlcSniffer(valid_config)
        sniffer.socket = mock_socket
        
        sniffer._process_packet(sample_packet)
        
        assert sniffer.stats.packets_processed == 1
        assert sniffer.stats.packets_forwarded == 1
        assert sniffer.stats.bytes_forwarded > 0
        
        # Check socket.sendto was called
        mock_socket.sendto.assert_called_once()
        args = mock_socket.sendto.call_args[0]
        assert args[1] == ("127.0.0.1", 8514)
    
    def test_forward_packet_socket_error(self, valid_config):
        sniffer = PlcSniffer(valid_config)
        
        with patch('socket.socket') as mock_socket_class:
            mock_socket = Mock()
            mock_socket.sendto.side_effect = socket.error("Network error")
            mock_socket_class.return_value = mock_socket
            
            sniffer._forward_packet(b"test data")
            
            # Should recreate socket after error
            assert mock_socket_class.call_count >= 2
    
    def test_graceful_shutdown(self, valid_config, mock_scapy_sniff):
        sniffer = PlcSniffer(valid_config)
        
        # Mock sniff to call stop immediately
        def mock_sniff_impl(**kwargs):
            sniffer.running = False
            stop_filter = kwargs.get('stop_filter')
            if stop_filter:
                assert stop_filter(None) is True
        
        mock_scapy_sniff.side_effect = mock_sniff_impl
        
        with patch.object(sniffer, '_create_socket'):
            sniffer.start()
        
        assert sniffer.running is False
        mock_scapy_sniff.assert_called_once()