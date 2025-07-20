#!/usr/bin/env python3
"""Test runner script that ensures proper Python path."""

import sys
import os
import pytest

# Add src to Python path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

if __name__ == '__main__':
    # Run pytest with all arguments passed to this script
    sys.exit(pytest.main(sys.argv[1:]))