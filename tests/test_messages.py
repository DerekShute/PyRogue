"""
    Test of things in messages module
"""
import unittest
from message import MessageBuffer


# ===== Test MessageBuffer ================================

class TestMessageBuffer(unittest.TestCase):
    """Test MessageBuffer"""

    def test(self):
        mb = MessageBuffer()
        assert mb.count == 0
        assert mb.msg == ''
        mb.add('frotz')
        mb.add('foo')
        mb.add('flarg')
        assert mb.count == 3
        assert mb.msg == 'frotz'
        mb.advance()
        assert mb.msg == 'foo'
        assert mb.count == 2
        mb.advance()
        mb.advance()
        mb.advance()
        assert mb.msg == ''
        self.assertTrue(True)


# ===== Invocation ========================================

# See 'run_tests.py' in parent directory

# EOF
