# PLC Sniffer Configuration Guide

## Environment Variables

The PLC Sniffer is configured through environment variables:

| Variable | Description | Default | Valid Values |
|----------|-------------|---------|--------------|
| `INTERFACE` | Network interface to capture packets | `eth0` | Any valid interface name |
| `FILTER` | BPF filter expression | `udp` | Valid BPF syntax |
| `DESTINATION_IP` | IP to forward packets to | `127.0.0.1` | Valid IPv4/IPv6 address |
| `DESTINATION_PORT` | Port to forward packets to | `8514` | 1-65535 |
| `LOG_LEVEL` | Logging verbosity | `INFO` | DEBUG, INFO, WARNING, ERROR, CRITICAL |
| `MAX_PACKET_SIZE` | Maximum packet size in bytes | `65535` | 64-65535 |
| `RATE_LIMIT` | Max packets per second (0=unlimited) | `0` | 0-1000000 |
| `SOCKET_TIMEOUT` | Socket timeout in seconds | `5.0` | > 0 |
| `HEALTH_CHECK_PORT` | Port for health checks (0=disabled) | `8080` | 0-65535 |

## Configuration Examples

### Basic UDP Forwarding
```bash
export INTERFACE=eth0
export FILTER="udp"
export DESTINATION_IP=192.168.1.100
export DESTINATION_PORT=514
```

### Filtered Capture with Rate Limiting
```bash
export INTERFACE=eth0
export FILTER="udp and port 502"  # Modbus traffic
export DESTINATION_IP=10.0.0.50
export DESTINATION_PORT=8514
export RATE_LIMIT=1000  # Max 1000 pps
export LOG_LEVEL=DEBUG
```

### High-Security Configuration
```bash
export INTERFACE=eth0
export FILTER="udp and src net 192.168.100.0/24"
export DESTINATION_IP=127.0.0.1
export DESTINATION_PORT=8514
export MAX_PACKET_SIZE=1500  # Standard MTU
export RATE_LIMIT=5000  # Prevent flooding
export LOG_LEVEL=WARNING
```

## Docker Configuration

### Using Docker Compose
```yaml
services:
  plc_sniffer:
    image: plc-sniffer:latest
    environment:
      - INTERFACE=eth0
      - FILTER=udp port 502
      - DESTINATION_IP=syslog-server
      - DESTINATION_PORT=514
      - RATE_LIMIT=10000
      - HEALTH_CHECK_PORT=8080
```

### Using Docker Run
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
  plc-sniffer:latest
```

## BPF Filter Examples

Common filter expressions for industrial protocols:

```bash
# Modbus TCP/UDP
FILTER="port 502"

# DNP3
FILTER="port 20000"

# IEC 60870-5-104
FILTER="tcp port 2404"

# EtherNet/IP
FILTER="udp port 2222 or tcp port 44818"

# OPC UA
FILTER="tcp port 4840"

# Specific PLC subnet
FILTER="udp and src net 192.168.100.0/24"

# Multiple protocols
FILTER="(udp port 502) or (tcp port 502) or (udp port 2222)"

# Exclude broadcast/multicast
FILTER="udp and not broadcast and not multicast"
```

## Validation Rules

1. **IP Addresses**: Must be valid IPv4 or IPv6 format
2. **Ports**: Must be between 1-65535
3. **Interface Names**: Alphanumeric with hyphens, dots, underscores (max 15 chars)
4. **Packet Size**: Between 64-65535 bytes
5. **Rate Limit**: Between 0-1000000 pps
6. **BPF Filters**: Must contain valid BPF keywords and balanced parentheses

## Security Best Practices

1. **Use Rate Limiting**: Always set a reasonable `RATE_LIMIT` to prevent DoS
2. **Filter Traffic**: Use specific BPF filters to capture only required traffic
3. **Limit Packet Size**: Set `MAX_PACKET_SIZE` to expected maximum
4. **Run Non-Root**: Use Docker with capabilities instead of privileged mode
5. **Network Isolation**: Deploy in isolated network segments
6. **Monitor Logs**: Set appropriate `LOG_LEVEL` for your environment

## Troubleshooting

### Common Issues

1. **Permission Denied**
   - Ensure the process has CAP_NET_RAW capability
   - Check interface permissions

2. **Interface Not Found**
   - List available interfaces: `ip link show`
   - Check interface name spelling

3. **Invalid BPF Filter**
   - Test filter with tcpdump: `tcpdump -i eth0 'your-filter'`
   - Check for syntax errors

4. **High CPU Usage**
   - Enable rate limiting
   - Use more specific BPF filters
   - Check for packet storms

5. **Packets Not Forwarded**
   - Verify destination is reachable
   - Check firewall rules
   - Monitor error logs