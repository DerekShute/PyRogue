"""
    Unit test master script
    
    If you have 'tests' in the name, then pytest will try to do something with it.
"""

import pytest
import sys


sys.path.insert(0, './pyrogue/')
pytest.main(["tests", "--omit", "pipeline.py"])

# EOF
