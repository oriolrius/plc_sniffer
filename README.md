# PLC Sniffer

A network traffic sniffer specifically designed to capture UDP packets from PLCs (Programmable Logic Controllers) and forward them to a specified destination.

## Features

- Captures UDP packets based on configurable filters
- Forwards packet payloads to a specified UDP destination
- Configurable through environment variables
- Detailed logging with adjustable verbosity

## Configuration

The sniffer can be configured using the following environment variables:

- `IFACE`: Network interface to listen on (default: "qvs1")
- `FILTER`: Packet filter expression (default: "host 10.121.101.8 and udp port 4000")
- `UDP_IP`: Destination IP address for forwarded packets (default: "10.121.101.1")
- `UDP_PORT`: Destination port for forwarded packets (default: 40000)
- `LOGLEVEL`: Logging level (default: "INFO")

## Usage

```bash
# Run with default settings
python plc_sniffer.py

# Run with custom interface and filter
IFACE=eth0 FILTER="host 192.168.1.5 and udp port 502" python plc_sniffer.py

# Run with increased log verbosity
LOGLEVEL=DEBUG python plc_sniffer.py
```
