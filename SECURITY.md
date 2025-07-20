# Security Policy

## Supported Versions

| Version | Supported          |
| ------- | ------------------ |
| 0.1.x   | :white_check_mark: |

## Reporting a Vulnerability

We take security seriously. If you discover a security vulnerability, please follow these steps:

1. **DO NOT** open a public issue
2. Email security details to: security@example.com
3. Include:
   - Description of the vulnerability
   - Steps to reproduce
   - Potential impact
   - Suggested fix (if any)

## Response Timeline

- **Acknowledgment**: Within 48 hours
- **Initial Assessment**: Within 1 week
- **Fix Development**: Varies by severity
- **Public Disclosure**: After fix is released

## Security Measures

### Current Security Features

- Input validation on all configuration
- Rate limiting to prevent DoS
- Packet size limits
- Non-root container execution
- Resource limits in Docker

### Planned Security Enhancements

- TLS support for forwarded packets
- Authentication mechanisms
- Audit logging
- Anomaly detection

## Best Practices

When deploying PLC Sniffer:

1. **Network Isolation**
   - Deploy in isolated network segments
   - Use firewall rules to restrict traffic

2. **Access Control**
   - Limit who can access the deployment
   - Use strong authentication
   - Monitor access logs

3. **Configuration Security**
   - Don't hardcode sensitive values
   - Use secrets management
   - Validate all inputs

4. **Monitoring**
   - Enable logging
   - Monitor for anomalies
   - Set up alerts

## Security Checklist

- [ ] Running with minimal privileges
- [ ] Rate limiting enabled
- [ ] Network properly segmented
- [ ] Logging configured
- [ ] Monitoring in place
- [ ] Incident response plan ready

## Responsible Disclosure

We follow responsible disclosure principles:
- Security issues are fixed before disclosure
- Credit given to reporters (if desired)
- CVEs assigned for significant vulnerabilities

Thank you for helping keep PLC Sniffer secure!