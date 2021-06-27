"""
    Unit test master script

    ***RUN TESTS FROM HERE***
"""

import pytest
import sys

if __name__ == '__main__':
    sys.path.insert(0, './pyrogue/')
    pytest.main(["--cov=pyrogue",
                 "--cov-branch",
                 "--no-cov-on-fail",
                 "--cov-report=term-missing",
                 "tests"])

# EOF
