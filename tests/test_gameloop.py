"""
    Test of things in player module
"""

import unittest
from unittest.mock import Mock
from gameloop import MainMenuState, MainGameloop, RIPGameState
from player import Player

# ===== Test Main Menu ====================================

class TestMainMenuState(unittest.TestCase):
    """Test Main Menu"""

    def test_quit(self):
        event_return = Mock(return_value='quit')
        display_mock = Mock(dispatch_event=event_return)
        loop = MainMenuState(display=display_mock).run()
        assert loop is None
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

class TestRIPState(unittest.TestCase):
    """Test Main Menu"""

    def test_quit(self):
        p = Player.factory()
        p.add_exp(1000)
        p.purse = 500
        p.levelno = 4
        event_return = Mock(return_value='quit')
        msg_mock = Mock()
        display_mock = Mock(dispatch_event=event_return, centered_msg=msg_mock)
        loop = RIPGameState(display=display_mock, player=p, situation='quit').run()
        assert loop is None
        assert msg_mock.call_count == 4
        expected = ('A COWARDLY ESCAPE BY',
                    'A level 7 adventurer',
                    'On level 4 of The Dungeon of Doom',
                    'Clutching 500 gold pieces')
        i = 0
        for string in expected:
            _, kwargs = msg_mock.call_args_list[i] # call_args_list[x][0] is args, [1] is kwargs when unpacked
            print(kwargs['string'])
            assert kwargs['string'] == string
            i += 1
        self.assertTrue(True)

    # TODO: death and victory


# ===== Invocation ========================================

# See 'run_tests.py' in parent directory

# EOF
