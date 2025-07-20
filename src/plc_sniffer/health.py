"""Health check and monitoring server for PLC Sniffer."""

import json
import logging
import threading
import time
from datetime import datetime
from http.server import BaseHTTPRequestHandler, HTTPServer
from typing import Optional, Dict, Any

from .sniffer import PlcSniffer


logger = logging.getLogger(__name__)


class HealthCheckHandler(BaseHTTPRequestHandler):
    """HTTP request handler for health checks and metrics."""
    
    sniffer: Optional[PlcSniffer] = None
    start_time: float = time.time()
    
    def do_GET(self):
        """Handle GET requests."""
        if self.path == '/health':
            self._handle_health()
        elif self.path == '/ready':
            self._handle_ready()
        elif self.path == '/metrics':
            self._handle_metrics()
        else:
            self.send_error(404)
    
    def _handle_health(self):
        """Liveness probe - is the service running?"""
        self.send_response(200)
        self.send_header('Content-Type', 'application/json')
        self.end_headers()
        
        response = {
            'status': 'healthy',
            'timestamp': datetime.utcnow().isoformat(),
            'uptime': time.time() - self.start_time
        }
        
        self.wfile.write(json.dumps(response).encode())
    
    def _handle_ready(self):
        """Readiness probe - is the service ready to accept traffic?"""
        if self.sniffer and self.sniffer.running:
            self.send_response(200)
            self.send_header('Content-Type', 'application/json')
            self.end_headers()
            
            response = {
                'status': 'ready',
                'timestamp': datetime.utcnow().isoformat()
            }
            
            self.wfile.write(json.dumps(response).encode())
        else:
            self.send_error(503, 'Service not ready')
    
    def _handle_metrics(self):
        """Prometheus-style metrics endpoint."""
        if not self.sniffer:
            self.send_error(503, 'Service not initialized')
            return
        
        self.send_response(200)
        self.send_header('Content-Type', 'text/plain; version=0.0.4')
        self.end_headers()
        
        stats = self.sniffer.stats
        uptime = time.time() - self.start_time
        
        metrics = [
            '# HELP plc_sniffer_uptime_seconds Time since service started',
            '# TYPE plc_sniffer_uptime_seconds gauge',
            f'plc_sniffer_uptime_seconds {uptime:.2f}',
            '',
            '# HELP plc_sniffer_packets_processed_total Total packets processed',
            '# TYPE plc_sniffer_packets_processed_total counter',
            f'plc_sniffer_packets_processed_total {stats.packets_processed}',
            '',
            '# HELP plc_sniffer_packets_forwarded_total Total packets forwarded',
            '# TYPE plc_sniffer_packets_forwarded_total counter',
            f'plc_sniffer_packets_forwarded_total {stats.packets_forwarded}',
            '',
            '# HELP plc_sniffer_packets_dropped_total Total packets dropped',
            '# TYPE plc_sniffer_packets_dropped_total counter',
            f'plc_sniffer_packets_dropped_total {stats.packets_dropped}',
            '',
            '# HELP plc_sniffer_packets_rate_limited_total Packets dropped due to rate limit',
            '# TYPE plc_sniffer_packets_rate_limited_total counter',
            f'plc_sniffer_packets_rate_limited_total {stats.rate_limited}',
            '',
            '# HELP plc_sniffer_packets_oversized_total Packets dropped due to size',
            '# TYPE plc_sniffer_packets_oversized_total counter',
            f'plc_sniffer_packets_oversized_total {stats.oversized}',
            '',
            '# HELP plc_sniffer_errors_total Total errors encountered',
            '# TYPE plc_sniffer_errors_total counter',
            f'plc_sniffer_errors_total {stats.errors}',
            '',
            '# HELP plc_sniffer_bytes_forwarded_total Total bytes forwarded',
            '# TYPE plc_sniffer_bytes_forwarded_total counter',
            f'plc_sniffer_bytes_forwarded_total {stats.bytes_forwarded}',
            '',
            '# HELP plc_sniffer_current_packet_rate Current packets per second',
            '# TYPE plc_sniffer_current_packet_rate gauge',
            f'plc_sniffer_current_packet_rate {stats.get_current_rate():.2f}',
        ]
        
        self.wfile.write('\n'.join(metrics).encode())
    
    def log_message(self, format, *args):
        """Suppress default HTTP logging."""
        pass  # Health checks are noisy, only log errors


class HealthCheckServer:
    """HTTP server for health checks and metrics."""
    
    def __init__(self, port: int = 8080):
        self.port = port
        self.server: Optional[HTTPServer] = None
        self.thread: Optional[threading.Thread] = None
        self.running = False
    
    def start(self, sniffer: PlcSniffer):
        """Start the health check server."""
        HealthCheckHandler.sniffer = sniffer
        HealthCheckHandler.start_time = time.time()
        
        self.server = HTTPServer(('', self.port), HealthCheckHandler)
        self.running = True
        
        self.thread = threading.Thread(target=self._run, daemon=True)
        self.thread.start()
        
        logger.info(f"Health check server started on port {self.port}")
    
    def _run(self):
        """Run the server in a thread."""
        while self.running:
            self.server.handle_request()
    
    def stop(self):
        """Stop the health check server."""
        self.running = False
        if self.server:
            self.server.shutdown()
        if self.thread:
            self.thread.join(timeout=5)
        logger.info("Health check server stopped")