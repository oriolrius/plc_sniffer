"""Core packet sniffer implementation with security features."""

import logging
import socket
import time
from collections import deque
from dataclasses import dataclass
from datetime import datetime
from typing import Optional, Deque

from scapy.all import sniff, IP, UDP, Raw

from .config import SnifferConfig


logger = logging.getLogger(__name__)


@dataclass
class RateLimiter:
    """Token bucket rate limiter implementation."""
    
    rate: int  # packets per second
    bucket_size: int
    tokens: float
    last_update: float
    
    def __init__(self, rate: int):
        self.rate = rate
        self.bucket_size = rate  # 1 second worth of tokens
        self.tokens = float(rate)
        self.last_update = time.time()
    
    def allow(self) -> bool:
        """Check if packet is allowed under rate limit."""
        if self.rate == 0:  # No limit
            return True
        
        now = time.time()
        elapsed = now - self.last_update
        
        # Add tokens based on elapsed time
        self.tokens = min(
            self.bucket_size,
            self.tokens + elapsed * self.rate
        )
        self.last_update = now
        
        if self.tokens >= 1:
            self.tokens -= 1
            return True
        
        return False


class PacketStats:
    """Track packet statistics."""
    
    def __init__(self, window_size: int = 60):
        self.window_size = window_size
        self.packets_processed: int = 0
        self.packets_dropped: int = 0
        self.packets_forwarded: int = 0
        self.bytes_forwarded: int = 0
        self.errors: int = 0
        self.rate_limited: int = 0
        self.oversized: int = 0
        
        # Sliding window for rate calculation
        self.recent_packets: Deque[float] = deque(maxlen=window_size)
    
    def record_packet(self, forwarded: bool, size: int = 0):
        """Record packet processing."""
        self.packets_processed += 1
        self.recent_packets.append(time.time())
        
        if forwarded:
            self.packets_forwarded += 1
            self.bytes_forwarded += size
        else:
            self.packets_dropped += 1
    
    def get_current_rate(self) -> float:
        """Calculate current packet rate."""
        if len(self.recent_packets) < 2:
            return 0.0
        
        now = time.time()
        # Remove old entries
        cutoff = now - self.window_size
        while self.recent_packets and self.recent_packets[0] < cutoff:
            self.recent_packets.popleft()
        
        if not self.recent_packets:
            return 0.0
        
        time_span = now - self.recent_packets[0]
        if time_span > 0:
            return len(self.recent_packets) / time_span
        
        return 0.0
    
    def log_stats(self):
        """Log current statistics."""
        logger.info(
            f"Stats - Processed: {self.packets_processed}, "
            f"Forwarded: {self.packets_forwarded}, "
            f"Dropped: {self.packets_dropped}, "
            f"Rate Limited: {self.rate_limited}, "
            f"Oversized: {self.oversized}, "
            f"Errors: {self.errors}, "
            f"Current Rate: {self.get_current_rate():.2f} pps"
        )


class PlcSniffer:
    """PLC packet sniffer with security features."""
    
    def __init__(self, config: SnifferConfig):
        self.config = config
        self.socket: Optional[socket.socket] = None
        self.rate_limiter = RateLimiter(config.rate_limit)
        self.stats = PacketStats()
        self.running = False
        self.last_stats_log = time.time()
        
        # Configure logging
        logging.basicConfig(
            level=getattr(logging, config.log_level),
            format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
        )
    
    def _create_socket(self) -> socket.socket:
        """Create and configure UDP socket."""
        sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        sock.settimeout(self.config.socket_timeout)
        return sock
    
    def _process_packet(self, packet) -> None:
        """Process captured packet with security checks."""
        try:
            # Check rate limit
            if not self.rate_limiter.allow():
                self.stats.rate_limited += 1
                self.stats.record_packet(forwarded=False)
                logger.debug("Packet dropped due to rate limit")
                return
            
            # Extract UDP payload
            if IP in packet and UDP in packet and Raw in packet:
                payload = bytes(packet[Raw])
                
                # Check packet size
                if len(payload) > self.config.max_packet_size:
                    self.stats.oversized += 1
                    self.stats.record_packet(forwarded=False)
                    logger.warning(
                        f"Packet dropped: size {len(payload)} exceeds "
                        f"limit {self.config.max_packet_size}"
                    )
                    return
                
                # Forward packet
                self._forward_packet(payload)
                self.stats.record_packet(forwarded=True, size=len(payload))
                
                logger.debug(
                    f"Forwarded packet from {packet[IP].src}:{packet[UDP].sport} "
                    f"to {packet[IP].dst}:{packet[UDP].dport}, "
                    f"size: {len(payload)} bytes"
                )
            else:
                self.stats.record_packet(forwarded=False)
                logger.debug("Packet dropped: not UDP or no payload")
                
        except Exception as e:
            self.stats.errors += 1
            self.stats.record_packet(forwarded=False)
            logger.error(f"Error processing packet: {e}")
    
    def _forward_packet(self, payload: bytes) -> None:
        """Forward packet payload to destination."""
        try:
            if self.socket is None:
                self.socket = self._create_socket()
            
            self.socket.sendto(
                payload,
                (self.config.destination_ip, self.config.destination_port)
            )
            
        except socket.timeout:
            logger.error("Socket timeout while forwarding packet")
            self._recreate_socket()
        except socket.error as e:
            logger.error(f"Socket error while forwarding: {e}")
            self._recreate_socket()
        except Exception as e:
            logger.error(f"Unexpected error while forwarding: {e}")
            self._recreate_socket()
    
    def _recreate_socket(self) -> None:
        """Recreate socket after error."""
        try:
            if self.socket:
                self.socket.close()
            self.socket = self._create_socket()
            logger.info("Socket recreated successfully")
        except Exception as e:
            logger.error(f"Failed to recreate socket: {e}")
            self.socket = None
    
    def _log_stats_periodically(self) -> None:
        """Log statistics periodically."""
        now = time.time()
        if now - self.last_stats_log >= 60:  # Log every minute
            self.stats.log_stats()
            self.last_stats_log = now
    
    def start(self) -> None:
        """Start packet sniffing."""
        logger.info(f"Starting PLC Sniffer on interface {self.config.interface}")
        logger.info(f"Filter: {self.config.filter}")
        logger.info(
            f"Forwarding to: {self.config.destination_ip}:"
            f"{self.config.destination_port}"
        )
        
        if self.config.rate_limit > 0:
            logger.info(f"Rate limit: {self.config.rate_limit} pps")
        
        self.running = True
        
        try:
            # Create initial socket
            self.socket = self._create_socket()
            
            # Start sniffing
            sniff(
                iface=self.config.interface,
                filter=self.config.filter,
                prn=self._process_packet,
                store=False,
                stop_filter=lambda x: not self.running
            )
            
        except KeyboardInterrupt:
            logger.info("Sniffer stopped by user")
        except Exception as e:
            logger.error(f"Sniffer error: {e}")
            raise
        finally:
            self.stop()
    
    def stop(self) -> None:
        """Stop packet sniffing and cleanup."""
        self.running = False
        
        # Final stats
        self.stats.log_stats()
        
        # Cleanup socket
        if self.socket:
            try:
                self.socket.close()
            except Exception as e:
                logger.error(f"Error closing socket: {e}")
        
        logger.info("PLC Sniffer stopped")