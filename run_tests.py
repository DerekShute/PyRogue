"""
    Unit test master script
    
    If you have 'tests' in the name, then pytest will try to do something with it.
    
    NOTE: IDENTICAL TO pipeline
"""

import pytest
import sys

if __name__ == '__main__':
    sys.path.insert(0, './pyrogue/')
    pytest.main(["tests"])

# EOF
