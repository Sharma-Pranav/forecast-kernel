# scripts/check_python_version.py
import sys
assert sys.version_info[:2] == (3, 10), "Python 3.10.x required"