# Testing Guide

## Running Tests

### Quick Start

```bash
# Run all tests
make test

# Run with verbose output
pytest -v

# Run specific test file
pytest tests/unit/test_sniffer.py

# Run specific test
pytest tests/unit/test_sniffer.py::test_packet_capture
```

### Test Coverage

The project maintains a minimum of 60% code coverage.

```bash
# Generate coverage report in terminal
pytest --cov=src/plc_sniffer --cov-report=term-missing

# Generate HTML coverage report
pytest --cov=src/plc_sniffer --cov-report=html
```

#### HTML Coverage Report

After running tests with `--cov-report=html` (which happens automatically via pytest.ini), an HTML report is generated in the `htmlcov/` directory:

```bash
# View coverage report
open htmlcov/index.html  # macOS
xdg-open htmlcov/index.html  # Linux
start htmlcov/index.html  # Windows
```

The HTML report shows:
- Overall coverage percentage
- File-by-file coverage breakdown
- Line-by-line coverage with highlighting
- Missing lines marked in red

**Note:** The `htmlcov/` directory is automatically generated and should not be committed to git (it's already in .gitignore).

## Test Structure

```
tests/
├── unit/              # Unit tests
│   ├── test_sniffer.py
│   ├── test_config.py
│   ├── test_processors.py
│   └── test_health.py
├── integration/       # Integration tests
│   └── test_integration.py
└── conftest.py       # Pytest fixtures
```

## Writing Tests

### Example Unit Test

```python
import pytest
from plc_sniffer.sniffer import PacketSniffer
from plc_sniffer.config import Config

def test_sniffer_initialization():
    """Test sniffer can be initialized with valid config."""
    config = Config(interface="lo")
    sniffer = PacketSniffer(config)
    assert sniffer.config.interface == "lo"

def test_invalid_interface():
    """Test sniffer raises error with invalid interface."""
    config = Config(interface="invalid0")
    with pytest.raises(ValueError):
        PacketSniffer(config)
```

### Using Fixtures

```python
@pytest.fixture
def mock_config():
    """Provide a test configuration."""
    return Config(
        interface="lo",
        filter="udp port 9999",
        destination_ip="127.0.0.1",
        destination_port=9999
    )

def test_with_fixture(mock_config):
    """Test using fixture."""
    sniffer = PacketSniffer(mock_config)
    assert sniffer.config.filter == "udp port 9999"
```

## Test Categories

### Unit Tests
- Test individual components in isolation
- Mock external dependencies
- Fast execution
- Located in `tests/unit/`

### Integration Tests
- Test component interactions
- May use real network interfaces (loopback)
- Slower execution
- Located in `tests/integration/`

## Continuous Integration

Tests run automatically on:
- Every push to main/develop branches
- Every pull request
- Can be triggered manually

GitHub Actions workflow runs:
1. Linting (flake8)
2. Type checking (mypy)
3. Unit tests with coverage
4. Security scanning

## Testing Best Practices

1. **Write tests first** (TDD approach)
2. **One assertion per test** when possible
3. **Use descriptive test names**
4. **Mock external dependencies**
5. **Test edge cases and error conditions**
6. **Keep tests fast and independent**

## Debugging Tests

```bash
# Run tests with debugging output
pytest -v -s

# Run with pdb on failure
pytest --pdb

# Run specific test with pattern
pytest -k "test_packet"

# Show local variables on failure
pytest -l
```

## Performance Testing

For performance-critical code:

```python
import pytest
import time

def test_processing_performance(benchmark):
    """Test packet processing performance."""
    def process_packet():
        # Simulate packet processing
        time.sleep(0.001)
    
    # Benchmark will run the function multiple times
    result = benchmark(process_packet)
    
    # Assert performance requirements
    assert result < 0.002  # Must process in under 2ms
```

## Mocking Network Operations

```python
from unittest.mock import Mock, patch

@patch('scapy.all.sniff')
def test_packet_capture(mock_sniff):
    """Test packet capture with mocked scapy."""
    # Configure mock
    mock_sniff.return_value = [b'fake_packet']
    
    # Test capture
    sniffer = PacketSniffer(config)
    packets = sniffer._capture_packets()
    
    # Verify
    mock_sniff.assert_called_once()
    assert len(packets) == 1
```

## Test Configuration

The `pytest.ini` file configures:
- Default test paths
- Coverage settings
- Test discovery patterns
- Output formatting

Current settings ensure:
- Automatic coverage report generation (terminal and HTML)
- Minimum 60% coverage requirement
- Clear test output with warnings

## Pre-commit Testing

Before committing:

```bash
# Run full test suite
make test

# Run linting
make lint

# Format code
make format
```

The pre-commit hooks will also run automatically to ensure code quality.