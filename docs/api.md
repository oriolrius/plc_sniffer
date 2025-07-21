# API Reference

## Health Check Endpoints

The PLC Sniffer provides HTTP endpoints for monitoring and health checks when `HEALTH_CHECK_PORT` is configured.

### GET /health

Liveness probe endpoint.

**Response:**
```json
{
  "status": "healthy",
  "timestamp": "2025-07-21T10:30:00Z"
}
```

**Status Codes:**
- `200 OK`: Service is healthy
- `503 Service Unavailable`: Service is unhealthy

### GET /ready

Readiness probe endpoint. Indicates if the sniffer is ready to process packets.

**Response:**
```json
{
  "status": "ready",
  "interface": "eth0",
  "packets_processed": 12345
}
```

**Status Codes:**
- `200 OK`: Service is ready
- `503 Service Unavailable`: Service is not ready

### GET /metrics

Prometheus metrics endpoint in OpenMetrics format.

**Available Metrics:**

| Metric | Type | Description |
|--------|------|-------------|
| `plc_sniffer_packets_processed_total` | Counter | Total number of packets processed |
| `plc_sniffer_packets_forwarded_total` | Counter | Total number of packets successfully forwarded |
| `plc_sniffer_packets_dropped_total` | Counter | Total number of packets dropped |
| `plc_sniffer_packets_error_total` | Counter | Total number of packet processing errors |
| `plc_sniffer_current_packet_rate` | Gauge | Current packets per second |
| `plc_sniffer_packet_size_bytes` | Histogram | Distribution of packet sizes |
| `plc_sniffer_processing_duration_seconds` | Histogram | Time spent processing packets |

**Example Response:**
```
# HELP plc_sniffer_packets_processed_total Total number of packets processed
# TYPE plc_sniffer_packets_processed_total counter
plc_sniffer_packets_processed_total 123456

# HELP plc_sniffer_current_packet_rate Current packets per second
# TYPE plc_sniffer_current_packet_rate gauge
plc_sniffer_current_packet_rate 42.5
```

## Python API

### Main Class: PacketSniffer

```python
from plc_sniffer.sniffer import PacketSniffer
from plc_sniffer.config import Config

# Create configuration
config = Config(
    interface="eth0",
    filter="udp port 502",
    destination_ip="192.168.1.100",
    destination_port=514
)

# Initialize sniffer
sniffer = PacketSniffer(config)

# Start sniffing (blocking)
sniffer.start()
```

### Configuration Class

```python
@dataclass
class Config:
    interface: str = "eth0"
    filter: str = "udp"
    destination_ip: str = "127.0.0.1"
    destination_port: int = 8514
    max_packet_size: int = 65535
    rate_limit: int = 0
    health_check_port: int = 8080
    log_level: str = "INFO"
```

### Custom Packet Processors

You can extend the sniffer with custom packet processors:

```python
from plc_sniffer.processors import BaseProcessor

class CustomProcessor(BaseProcessor):
    def process(self, packet: bytes) -> Optional[bytes]:
        # Custom processing logic
        return packet

# Register processor
sniffer.add_processor(CustomProcessor())
```

### Exception Handling

```python
from plc_sniffer.exceptions import (
    SnifferException,
    ConfigurationError,
    NetworkError,
    RateLimitExceeded
)

try:
    sniffer.start()
except ConfigurationError as e:
    print(f"Configuration error: {e}")
except NetworkError as e:
    print(f"Network error: {e}")
except SnifferException as e:
    print(f"Sniffer error: {e}")
```

## CLI Interface

The `plc-sniffer` command accepts environment variables for configuration:

```bash
# Basic usage
plc-sniffer

# With custom configuration
INTERFACE=eth1 FILTER="udp port 502" plc-sniffer

# With all options
INTERFACE=eth0 \
FILTER="udp port 502" \
DESTINATION_IP=192.168.1.100 \
DESTINATION_PORT=514 \
RATE_LIMIT=10000 \
MAX_PACKET_SIZE=9000 \
HEALTH_CHECK_PORT=8080 \
LOG_LEVEL=DEBUG \
plc-sniffer
```

## Integration Examples

### Docker Health Check

```yaml
healthcheck:
  test: ["CMD", "curl", "-f", "http://localhost:8080/health"]
  interval: 30s
  timeout: 10s
  retries: 3
```

### Kubernetes Probes

```yaml
livenessProbe:
  httpGet:
    path: /health
    port: 8080
  initialDelaySeconds: 10
  periodSeconds: 30

readinessProbe:
  httpGet:
    path: /ready
    port: 8080
  initialDelaySeconds: 5
  periodSeconds: 10
```

### Prometheus Scrape Config

```yaml
scrape_configs:
  - job_name: 'plc-sniffer'
    static_configs:
      - targets: ['plc-sniffer:8080']
    metrics_path: '/metrics'
```