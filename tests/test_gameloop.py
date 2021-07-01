"""
    Test of things in player module
"""

from parameterized import parameterized
import unittest
from unittest.mock import patch, Mock
from gameloop import MainMenuState, MainGameloop
from actions import QuitAction
from display import Display

# ===== Test Main Menu ====================================

class TestMainMenuState(unittest.TestCase):
    """Test Main Menu"""

    def test_quit(self):
        event_return = Mock(return_value='quit')
        display_mock = Mock(dispatch_event=event_return)
        loop = MainMenuState(display=display_mock).run()
        assert loop == None
        self.assertTrue(True)

    def test_start_game(self):
        event_return = Mock(return_value='new')
        display_mock = Mock(dispatch_event=event_return)
        loop = MainMenuState(display=display_mock).run()
        assert isinstance(loop, MainGameloop)
        self.assertTrue(True)

    def test_nonsense(self):
        event_return = Mock(return_value='')
        display_mock = Mock(dispatch_event=event_return)
        prev_loop = MainMenuState(display=display_mock).run()
        loop = prev_loop.run()
        assert loop == prev_loop
        self.assertTrue(True)


# ===== Invocation ========================================

# See 'run_tests.py' in parent directory

# EOF
