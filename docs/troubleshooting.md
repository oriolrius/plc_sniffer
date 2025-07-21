# Troubleshooting Guide

## Common Issues

### 1. Permission Denied Errors

**Symptom:**
```
PermissionError: [Errno 1] Operation not permitted
```

**Solutions:**

**Docker:**
- Ensure container runs with proper capabilities:
  ```yaml
  cap_add:
    - NET_RAW
    - NET_ADMIN
  ```
- Or use privileged mode (less secure):
  ```yaml
  privileged: true
  ```

**Local Installation:**
- Run with sudo: `sudo plc-sniffer`
- Or grant capabilities: `sudo setcap cap_net_raw,cap_net_admin+eip $(which plc-sniffer)`

### 2. Module Import Errors

**Symptom:**
```
ModuleNotFoundError: No module named 'plc_sniffer'
```

**Solutions:**
- Ensure proper installation: `pip install -e .`
- Check PYTHONPATH includes the src directory
- Verify pyproject.toml is present in the root directory

### 3. No Packets Captured

**Symptom:**
- Sniffer runs but `packets_processed` remains 0

**Solutions:**

1. **Verify interface exists:**
   ```bash
   ip link show
   # or
   ifconfig
   ```

2. **Check BPF filter syntax:**
   ```bash
   # Test filter with tcpdump
   sudo tcpdump -i eth0 'udp port 502' -c 5
   ```

3. **Ensure traffic exists:**
   ```bash
   # Generate test traffic
   echo "test" | nc -u -w1 127.0.0.1 502
   ```

4. **Check firewall rules:**
   ```bash
   sudo iptables -L -n
   ```

### 4. High CPU Usage

**Symptom:**
- CPU usage near 100%

**Solutions:**

1. **Set rate limiting:**
   ```bash
   RATE_LIMIT=1000 plc-sniffer
   ```

2. **Use more specific filters:**
   ```bash
   # Instead of: FILTER="udp"
   # Use: FILTER="udp port 502 and host 192.168.1.10"
   ```

3. **Check for packet storms:**
   ```bash
   # Monitor packet rate
   curl http://localhost:8080/metrics | grep packet_rate
   ```

### 5. Memory Leaks

**Symptom:**
- Increasing memory usage over time

**Solutions:**

1. **Set packet size limits:**
   ```bash
   MAX_PACKET_SIZE=1500 plc-sniffer
   ```

2. **Enable memory limits in Docker:**
   ```yaml
   deploy:
     resources:
       limits:
         memory: 512M
   ```

### 6. Forwarding Failures

**Symptom:**
- `packets_forwarded` lower than `packets_processed`

**Solutions:**

1. **Verify destination is reachable:**
   ```bash
   nc -zvu $DESTINATION_IP $DESTINATION_PORT
   ```

2. **Check DNS resolution:**
   ```bash
   nslookup $DESTINATION_IP
   ```

3. **Test connectivity:**
   ```bash
   ping $DESTINATION_IP
   ```

4. **Check logs for errors:**
   ```bash
   LOG_LEVEL=DEBUG plc-sniffer
   ```

### 7. Docker-Specific Issues

**Container exits immediately:**
```bash
# Check logs
docker logs plc-sniffer

# Common fixes:
# 1. Ensure image is built
docker build -t plc-sniffer .

# 2. Check compose.yaml syntax
docker compose config

# 3. Verify network mode
# Use "host" for local capture
network_mode: host
```

**Cannot find libpcap:**
- The Docker image must include libpcap
- Current Dockerfile uses Debian base with libpcap-dev

### 8. Health Check Failures

**Symptom:**
- Health endpoints return 503

**Solutions:**

1. **Ensure port is configured:**
   ```bash
   HEALTH_CHECK_PORT=8080 plc-sniffer
   ```

2. **Check port conflicts:**
   ```bash
   sudo lsof -i :8080
   ```

3. **Verify metrics are updating:**
   ```bash
   # Should see increasing counters
   watch 'curl -s localhost:8080/metrics | grep total'
   ```

## Debug Mode

Enable detailed logging for troubleshooting:

```bash
LOG_LEVEL=DEBUG plc-sniffer
```

This will show:
- Configuration validation details
- Packet processing information
- Network operations
- Error stack traces

## Performance Tuning

### For High-Traffic Environments

1. **Increase receive buffer:**
   ```bash
   # System-wide
   sudo sysctl -w net.core.rmem_max=134217728
   sudo sysctl -w net.core.rmem_default=134217728
   ```

2. **Use specific BPF filters:**
   ```bash
   # Good - specific
   FILTER="udp port 502 and net 192.168.1.0/24"
   
   # Bad - too broad
   FILTER="udp"
   ```

3. **Enable CPU affinity:**
   ```bash
   # Pin to specific CPU
   taskset -c 2 plc-sniffer
   ```

### Monitoring Performance

```bash
# Real-time metrics
curl -s localhost:8080/metrics | grep -E '(rate|duration|size)'

# System resources
docker stats plc-sniffer

# Network statistics
ip -s link show eth0
```

## Getting Help

1. **Check logs first:**
   ```bash
   docker logs plc-sniffer --tail 100
   ```

2. **Enable debug mode:**
   ```bash
   LOG_LEVEL=DEBUG plc-sniffer
   ```

3. **Collect diagnostic information:**
   ```bash
   # System info
   uname -a
   python --version
   pip show plc-sniffer
   
   # Network info
   ip addr
   ip route
   
   # Docker info (if applicable)
   docker version
   docker compose version
   ```

4. **Report issues:**
   - Include all error messages
   - Provide configuration used
   - Describe expected vs actual behavior
   - Include diagnostic information