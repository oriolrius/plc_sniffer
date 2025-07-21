# PLC Sniffer

[![CI](https://github.com/oriolrius/plc_sniffer/actions/workflows/ci.yml/badge.svg)](https://github.com/oriolrius/plc_sniffer/actions/workflows/ci.yml)
[![Security Scan](https://github.com/oriolrius/plc_sniffer/actions/workflows/security.yml/badge.svg)](https://github.com/oriolrius/plc_sniffer/actions/workflows/security.yml)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

A secure, high-performance network packet sniffer designed for capturing and forwarding UDP traffic from PLCs (Programmable Logic Controllers) in industrial environments.

## Features

- **Packet Capture**: Efficient UDP packet capture using BPF filters
- **Security**: Input validation, rate limiting, and packet size limits
- **Monitoring**: Built-in health checks and Prometheus metrics
- **Containerized**: Secure Docker deployment with non-root execution
- **Configurable**: Environment-based configuration with validation
- **Production-Ready**: Comprehensive testing, CI/CD, and documentation

## Quick Start

### Using Docker (Recommended)

```bash
docker run -d \
  --name plc-sniffer \
  --cap-add NET_RAW \
  --cap-add NET_ADMIN \
  --network host \
  -e INTERFACE=eth0 \
  -e FILTER="udp" \
  -e DESTINATION_IP=192.168.1.100 \
  -e DESTINATION_PORT=514 \
  ghcr.io/oriolrius/plc-sniffer:latest
```

### Using Docker Compose

```yaml
services:
  plc_sniffer:
    image: ghcr.io/oriolrius/plc-sniffer:latest
    cap_add:
      - NET_RAW
      - NET_ADMIN
    network_mode: host
    environment:
      - INTERFACE=eth0
      - FILTER=udp port 502
      - DESTINATION_IP=syslog-server
      - DESTINATION_PORT=514
      - RATE_LIMIT=10000
      - LOG_LEVEL=INFO
```

More details and options available in the [compose.yaml](compose.yaml) file.

### Local Installation

```bash
# Clone repository
git clone https://github.com/oriolrius/plc_sniffer.git
cd plc_sniffer

# Install with pip
pip install -e .

# Run
plc-sniffer
```

## Configuration

| Variable | Description | Default |
|----------|-------------|---------|
| `INTERFACE` | Network interface to capture packets | `eth0` |
| `FILTER` | BPF filter expression | `udp` |
| `DESTINATION_IP` | IP to forward packets to | `127.0.0.1` |
| `DESTINATION_PORT` | Port to forward packets to | `8514` |
| `LOG_LEVEL` | Logging verbosity | `INFO` |
| `MAX_PACKET_SIZE` | Maximum packet size in bytes | `65535` |
| `RATE_LIMIT` | Max packets per second (0=unlimited) | `0` |
| `HEALTH_CHECK_PORT` | Port for health checks (0=disabled) | `8080` |

See [docs/configuration.md](docs/configuration.md) for detailed configuration options.

## Security Features

- **Input Validation**: All configuration validated before use
- **Rate Limiting**: Configurable packets-per-second limit
- **Packet Size Limits**: Prevent memory exhaustion
- **Non-Root Execution**: Runs with minimal privileges
- **Resource Limits**: CPU and memory constraints

See [docs/deployment-security.md](docs/deployment-security.md) for deployment security considerations.

## Monitoring

### Health Checks

```bash
# Liveness probe
curl http://localhost:8080/health

# Readiness probe
curl http://localhost:8080/ready

# Prometheus metrics
curl http://localhost:8080/metrics
```

### Metrics Available

- `plc_sniffer_packets_processed_total`: Total packets processed
- `plc_sniffer_packets_forwarded_total`: Successfully forwarded packets
- `plc_sniffer_packets_dropped_total`: Dropped packets
- `plc_sniffer_current_packet_rate`: Current packets per second
- And more...

## Development

### Setup Development Environment

```bash
# Install development dependencies
make dev-install

# Run tests
make test

# Run linting
make lint

# Format code
make format
```

### Version Management

This project uses [bumpr](https://github.com/oriolrius/bumpr) for version management:

```bash
# Bump patch version (bug fixes)
make bump-patch

# Bump minor version (new features)
make bump-minor

# Bump major version (breaking changes)
make bump-major
```

### Contributing

See [CONTRIBUTING.md](CONTRIBUTING.md) for development guidelines.

## Documentation

- [Configuration Guide](docs/configuration.md)
- [Deployment Security](docs/deployment-security.md)
- [Vulnerability Reporting](docs/vulnerability-reporting.md)
- [API Reference](docs/api.md)
- [Testing Guide](docs/testing.md)
- [Troubleshooting](docs/troubleshooting.md)
- [Changelog Management](docs/changelog-guide.md)

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Acknowledgments

- Built with [Scapy](https://scapy.net/) for packet manipulation
- Version management by [bumpr](https://github.com/oriolrius/bumpr)
- Containerization with Docker and Debian Linux