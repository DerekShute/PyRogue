"""
    Test of things in player module
"""

from parameterized import parameterized
import unittest
from unittest.mock import patch, Mock
from player import Player, Stats
from position import Pos
from actions import MovementAction, PickupAction, DescendAction, DropAction, UseAction
from level import Level
from item import Gold, Food


# ===== Service Routines ==================================

def randint_return_min(*args, **kwargs):
    """If asked to random.randint(x,y), return x"""
    # print(f'from {args[0]} to {args[1]}')
    assert args[0] < args[1]   # Check for stupid mistake
    return args[0]


def randint_return_max(*args, **kwargs):
    """If asked to random.randint(x,y), return y"""
    # print(f'from {args[0]} to {args[1]}')
    assert args[0] < args[1]   # Check for stupid mistake
    return args[1]


# ===== Test Player Basics ================================

class TestPlayer(unittest.TestCase):
    """Test Player"""

    def test(self):
        """Smoke test"""
        p = Player.factory(pos=(10, 10))
        # print(str(p))
        assert str(p) == 'Player(@(10,10),Stats(Str=16,XP=0(1),AC=10,Dmg=\'1x4\',HP=12/12))'
        # print(repr(p))
        assert repr(p) == 'Player(pos=(10, 10),stats=Stats(stren=16, arm=10, dmg=\'1x4\', ' \
               'maxhp=12, hpt=12, exp=0, level=1),food_left=1300)'
        assert repr(eval(repr(p))) == repr(p)
        assert p.name == 'Player'
        assert p.display == 'Level: 0 Gold: 0 Hp:12/12 Str:16(16) Arm: ? Exp:1(0)'
        self.assertTrue(True)

    def test_level(self):
        """Player attachment to level"""
        p = Player.factory(pos=Pos(10, 10))
        lvl = Level(1, 80, 25, None)
        p.attach_level(lvl)
        assert p.level == lvl  # Test point in neighborhood
        self.assertTrue(True)

    def test_pos(self):
        """Test positioning and set-positioning"""
        p = Player.factory(pos=Pos(10, 10))
        assert p.pos == Pos(10, 10)
        p.set_pos(Pos(20, 20))
        assert p.pos == Pos(20, 20)
        self.assertTrue(True)

    def test_char(self):
        """Test map display"""
        p = Player.factory(pos=Pos(10, 10))
        pos, char, color = p.char
        assert pos == Pos(10, 10)
        assert char == ord('@')
        assert color == (255, 255, 255)
        self.assertTrue(True)

    @parameterized.expand([(-1, 0),    # If <0 then 0
                           (0, 1100),  # If >0 and <STOMACHSIZE, then calculation
                           (1700, 2000)])  # If >STOMACHSIZE, then STOMACHSIZE
    @patch('random.randint')
    def test_eat(self, input, expected, mock_randint):
        """Test effect of eating something"""
        mock_randint.side_effect = randint_return_min
        p = Player(food_left=input)
        p.add_food()
        assert p.food_left == expected


# ===== Test Action =======================================

class TestPlayerActionCallback(unittest.TestCase):

    def test_move(self):
        """Move action moves the player"""
        p = Player.factory(pos=Pos(10, 10))
        p.attach_level(Level(1, 80, 25, None))
        p.move(-1, -1)
        assert p.pos == Pos(9, 9)
        self.assertTrue(True)

    def test_bump(self):
        p = Player.factory(pos=Pos(10, 10))
        p.bump(Pos(10, 9))
        assert p.pos == Pos(10, 10)
        assert p.curr_msg == 'Ouch!'
        self.assertTrue(True)


# ===== Test AI Callback ==================================

class TestPlayerAI(unittest.TestCase):

    def test_perform_no_action(self):
        """No action in perform"""
        p = Player.factory(pos=Pos(10, 10))
        input_handler = Mock(return_value=None)
        p.input_handler = Mock(get_action=input_handler)
        p.perform()
        self.assertTrue(True)

    def test_perform_move_allowed(self):
        """Player was allowed to move"""
        p = Player.factory(pos=Pos(10, 10))
        # Got all this?  input_handler is a mock that only returns MovementAction() if poked, and
        # p.input_handler becomes a mock with one method get_action() that returns the input_handler mock
        input_handler = Mock(return_value=MovementAction(-1, -1))
        p.input_handler = Mock(get_action=input_handler)
        with patch.object(Level, 'can_enter', return_value=True) as patched_level:
            p.attach_level(Level(1, 80, 25, None))
            p.perform()
            patched_level.assert_called_once()
        assert p.pos == Pos(9, 9)
        assert p.curr_msg == p.display
        self.assertTrue(True)

    def test_perform_move_denied(self):
        """Player was not allowed to move"""
        p = Player.factory(pos=Pos(10, 10))
        input_handler = Mock(return_value=MovementAction(-1, -1))
        p.input_handler = Mock(get_action=input_handler)
        with patch.object(Level, 'can_enter', return_value=False) as patched_level:
            p.attach_level(Level(1, 80, 25, None))
            p.perform()
            patched_level.assert_called_once()
        assert p.pos == Pos(10, 10)
        assert p.curr_msg == 'Ouch!'
        self.assertTrue(True)

    def test_perform_pickup_gold(self):
        """Pick up an Item"""
        p = Player.factory(pos=Pos(10, 10))
        input_handler = Mock(return_value=PickupAction())
        p.input_handler = Mock(get_action=input_handler)
        level = Level(1, 80, 25, None)
        _ = Gold(quantity=10, pos=Pos(10, 10), parent=level)
        p.attach_level(level)
        p.perform()
        assert level.items == []  # Gone from map
        assert p.display == 'Level: 1 Gold: 10 Hp:12/12 Str:16(16) Arm: ? Exp:1(0)'
        assert p.curr_msg == 'You pick up 10 gold pieces!'
        self.assertTrue(True)

    def test_perform_pickup_denied(self):
        """Pick up an Item"""
        p = Player.factory(pos=Pos(10, 10))
        input_handler = Mock(return_value=PickupAction())
        p.input_handler = Mock(get_action=input_handler)
        level = Level(1, 80, 25, None)
        p.attach_level(level)
        p.perform()
        assert p.curr_msg == 'No item there to pick up!'
        self.assertTrue(True)

    def test_perform_pickup_food(self):
        """Pick up an Item"""
        level = Level(1, 80, 25, None)
        p = Player(pos=Pos(10, 10))
        input_handler = Mock(return_value=PickupAction())
        p.input_handler = Mock(get_action=input_handler)
        p.attach_level(level)
        food = Food(which=Food.FRUIT, pos=Pos(10, 10), parent=level)
        # Smoke test: is where we think
        assert level.items == [food]
        assert food.parent == level
        p.perform()
        # Action occurred
        assert p.curr_msg == 'You pick up the food'
        # Gone from level
        assert level.items == []  # Gone from map
        # Into player inventory
        assert food.parent == p
        assert food in p.pack
        self.assertTrue(True)

    def test_perform_descend(self):
        """Stumble down the stairs"""
        p = Player.factory(pos=Pos(10, 10))
        input_handler = Mock(return_value=DescendAction())
        p.input_handler = Mock(get_action=input_handler)
        level = Level(1, 80, 25, None)
        level.add_stairs(Pos(10, 10))
        level.add_player(p)
        p.perform()
        assert p.level is None  # No longer on this level
        assert p.levelno == 2
        assert p.curr_msg == 'You stumble down the stairs.'
        # TODO: Level number in display
        self.assertTrue(True)

    def test_perform_descend_denied(self):
        """Try to stumble down non-existent stairs"""
        p = Player.factory(pos=Pos(10, 10))
        input_handler = Mock(return_value=DescendAction())
        p.input_handler = Mock(get_action=input_handler)
        level = Level(1, 80, 25, None)
        level.add_player(p)
        p.perform()
        assert p.level == level  # Haven't moved
        assert p.levelno == 1
        assert p.curr_msg == 'No stairs here!'
        self.assertTrue(True)

    def test_perform_drop_food(self):
        """Drop the thing in your inventory"""
        p = Player.factory(pos=Pos(10, 10))
        # Factory creates a food in player inventory
        assert p.pack != []
        food = p.pack[0]
        assert food.parent == p
        assert food.pos is None
        input_handler = Mock(return_value=DropAction())
        p.input_handler = Mock(get_action=input_handler)
        level = Level(1, 80, 25, None)
        level.add_player(p)
        p.perform()
        assert food.parent == level
        assert food.pos == p.pos
        assert food in level.items
        self.assertTrue(True)

    def test_perform_drop_denied(self):
        """Drop the nonexistent food in your inventory"""
        p = Player(pos=Pos(10, 10))
        assert p.pack == []
        input_handler = Mock(return_value=DropAction())
        p.input_handler = Mock(get_action=input_handler)
        p.perform()
        assert p.pack == []
        assert p.curr_msg == 'No item to drop!'
        self.assertTrue(True)

    def test_perform_use_food(self):
        """Use the nonexistent food in your inventory"""
        p = Player.factory(pos=Pos(10, 10))
        # Factory creates a food in player inventory
        assert p.pack != []
        input_handler = Mock(return_value=UseAction())
        p.input_handler = Mock(get_action=input_handler)
        p.perform()
        assert p.pack == []
        # TODO: can't test existence of food
        # TODO: there was a message and effects
        assert p.curr_msg != ''
        self.assertTrue(True)

    def test_perform_use_denied(self):
        """Use the nonexistent food in your inventory"""
        p = Player(pos=Pos(10, 10))
        assert p.pack == []
        input_handler = Mock(return_value=UseAction())
        p.input_handler = Mock(get_action=input_handler)
        p.perform()
        assert p.pack == []
        assert p.curr_msg == 'No item to use!'
        self.assertTrue(True)

    # TODO: use action that doesn't destroy item

    # TODO: bump actions, etc.


# ===== Test Combat Interface =============================

class TestPlayerCombat(unittest.TestCase):
    """Player Combat Interface"""

    def test_melee_attack(self):
        p = Player.factory()
        level, stren, dmg = p.melee_attack()
        assert level == 1
        assert stren == 16  # TODO: weapon
        assert dmg == '1x4'  # TODO: weapon
        self.assertTrue(True)

    def test_ac(self):
        p = Player.factory()
        # print (p.ac)
        assert p.ac == 10  # TODO: armor
        self.assertTrue(True)


# ===== Invocation ========================================

if __name__ == '__main__':
    unittest.main()

# EOF
