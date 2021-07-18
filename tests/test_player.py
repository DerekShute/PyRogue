"""
    Test of things in player module
"""

from parameterized import parameterized
import unittest
from unittest.mock import patch
from player import Player, Stats
from position import Pos
from actions import BumpAction, PickupAction, DescendAction, DropAction, UseAction, EquipAction
from level import Level
from item import Gold, Food, Equipment


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
        assert p.display == 'Level: 0 Gold: 0 Hp:12/12 Str:16(16) Arm: 10 Exp:1(0)'
        self.assertTrue(True)

    @patch('random.randint')
    def test_exp(self, mock_randint):
        """Player level gain at exp gain"""
        mock_randint.side_effect = randint_return_min
        p = Player.factory(pos=Pos(10, 10))
        assert p.lvl == 1
        assert p.display == 'Level: 0 Gold: 0 Hp:12/12 Str:16(16) Arm: 10 Exp:1(0)'
        p.add_exp(5)
        assert p.lvl == 1
        assert p.display == 'Level: 0 Gold: 0 Hp:12/12 Str:16(16) Arm: 10 Exp:1(5)'
        p.add_exp(5)
        assert p.lvl == 2
        assert p.display == 'Level: 0 Gold: 0 Hp:13/13 Str:16(16) Arm: 10 Exp:2(10)'
        assert p.curr_msg == 'Welcome to level 2'
        p.advance_msg()
        p.add_exp(1000)
        assert p.lvl == 7
        assert p.display == 'Level: 0 Gold: 0 Hp:18/18 Str:16(16) Arm: 10 Exp:7(1010)'
        assert p.curr_msg == 'Welcome to level 3 --MORE--'
        p.advance_msg()
        assert p.curr_msg == 'Welcome to level 4 --MORE--'
        p.advance_msg()
        assert p.curr_msg == 'Welcome to level 5 --MORE--'
        p.advance_msg()
        assert p.curr_msg == 'Welcome to level 6 --MORE--'
        p.advance_msg()
        assert p.curr_msg == 'Welcome to level 7'
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

    def test_inventory(self):
        p = Player.factory(pos=Pos(1, 1))
        f = Food(which=Food.FRUIT)
        f.set_parent(p)
        p.add_item(f)
        menu = p.render_inventory('')
        assert menu.title == 'inventory'
        assert menu.text[0] == 'food ration'
        assert menu.text[1] == 'slime-mold'
        self.assertTrue(True)

    def test_drop_inventory(self):
        p = Player.factory(pos=Pos(1, 1))
        e = Equipment(etype=Equipment.ARMOR, name='fake armor', value=6, worth=10, char=')', color=(0, 0, 0))
        p.add_item(e)
        p.armor = e
        menu = p.render_inventory('drop')
        assert menu.title == 'drop'
        assert menu.text[0] == 'a: food ration'
        assert menu.text[1] == 'b: fake armor (being worn)'
        self.assertTrue(True)

    def test_use_inventory(self):
        p = Player.factory(pos=Pos(1, 1))
        f = Food(which=Food.FRUIT)
        f.set_parent(p)
        p.add_item(f)
        menu = p.render_inventory('use')
        assert menu.title == 'use'
        assert menu.text[0] == 'a: food ration'
        assert menu.text[1] == 'b: slime-mold'
        self.assertTrue(True)

    def test_equip_empty_inventory(self):
        p = Player.factory(pos=Pos(1, 1))
        menu = p.render_inventory('equip')
        assert menu.title == 'equip'
        assert len(menu.text) == 0
        self.assertTrue(True)

    def test_equip_food(self):
        p = Player.factory(pos=Pos(1, 1))
        f = Food(which=Food.FRUIT)
        f.set_parent(p)
        p.add_item(f)
        p.equip(f)
        assert p.curr_msg == 'The slime-mold cannot be equipped.'
        self.assertTrue(True)

    @parameterized.expand([
        (Equipment.WEAPON, 'b: fake (wielded)'),
        (Equipment.ARMOR, 'b: fake (being worn)'),
        ])
    def test_equip(self, input, expected):
        p = Player.factory(pos=Pos(1, 1))
        e = Equipment.factory(etype=input, template='name=fake value=6 worth=10')
        p.add_item(e)
        menu = p.render_inventory('equip')
        assert menu.text[0] == 'b: fake'  # 'a' is a food ration
        p.equip(e)
        menu = p.render_inventory('equip')
        assert menu.text[0] == expected  # 'a' is a food ration
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

    # TODO: TEST EFFECTS, COUNTDOWN
    
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

    def test_equip_armor(self):
        p = Player.factory(pos=Pos(10, 10))
        e = Equipment.factory(etype=Equipment.ARMOR, template='name=fake value=6 worth=10')
        p.add_item(e)
        p.equip(e)
        assert p.armor == e
        assert p.ac == 6
        assert p.curr_msg == 'You put on the fake'
        assert p.display == 'Level: 0 Gold: 0 Hp:12/12 Str:16(16) Arm: 6 Exp:1(0)'
        self.assertTrue(True)

    def test_replace_armor(self):
        p = Player.factory(pos=Pos(10, 10))
        e = Equipment.factory(etype=Equipment.ARMOR, template='name=fake_armor value=6 worth=10')
        p.add_item(e)
        p.armor = e
        f = Equipment.factory(etype=Equipment.ARMOR, template='name=fake_armor2 value=4 worth=10')
        p.add_item(f)
        p.equip(f)
        assert p.armor == f
        assert p.ac == 4
        assert p.curr_msg == 'You take off the fake armor --MORE--'
        p.advance_msg()
        assert p.curr_msg == 'You put on the fake armor2'
        self.assertTrue(True)

    def test_equip_weapon(self):
        p = Player.factory(pos=Pos(10, 10))
        e = Equipment.factory(etype=Equipment.WEAPON, template='name=fake dam=1x99')
        p.add_item(e)
        p.equip(e)
        _, _, dmg, _ = p.melee_attack()
        assert dmg == '1x99'
        assert p.curr_msg == 'You wield the fake'
        p.advance_msg()
        f = Equipment.factory(etype=Equipment.WEAPON, template='name=fake2 dam=1x3')
        p.add_item(f)
        p.equip(f)
        _, _, dmg, _ = p.melee_attack()
        assert dmg == '1x3'
        assert p.curr_msg == 'You put away the fake --MORE--'
        p.advance_msg()
        assert p.curr_msg == 'You wield the fake2'
        self.assertTrue(True)


# ===== Test AI Callback ==================================

class TestPlayerAI(unittest.TestCase):

    def test_perform_no_action(self):
        """No action in perform"""
        p = Player.factory(pos=Pos(10, 10))
        p.perform()
        self.assertTrue(True)

    def test_perform_move_allowed(self):
        """Player was allowed to move"""
        p = Player.factory(pos=Pos(10, 10))
        p.queue_action(BumpAction(-1, -1))
        with patch.object(Level, 'can_enter', return_value=True) as patched_level:
            p.attach_level(Level(1, 80, 25, None))
            p.perform()
            patched_level.assert_called()
        assert p.pos == Pos(9, 9)
        assert p.curr_msg == p.display
        self.assertTrue(True)

    def test_perform_move_denied(self):
        """Player was not allowed to move"""
        p = Player.factory(pos=Pos(10, 10))
        p.queue_action(BumpAction(-1, -1))
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
        p.queue_action(PickupAction())
        level = Level(1, 80, 25, None)
        level.add_item(Gold(quantity=10, pos=Pos(10, 10), parent=level))
        p.attach_level(level)
        p.perform()
        assert level.items == []  # Gone from map
        assert p.display == 'Level: 1 Gold: 10 Hp:12/12 Str:16(16) Arm: 10 Exp:1(0)'
        assert p.curr_msg == 'You pick up 10 gold pieces!'
        self.assertTrue(True)

    def test_perform_pickup_denied(self):
        """Pick up an Item"""
        p = Player.factory(pos=Pos(10, 10))
        p.queue_action(PickupAction())
        level = Level(1, 80, 25, None)
        p.attach_level(level)
        p.perform()
        assert p.curr_msg == 'No item there to pick up!'
        self.assertTrue(True)

    def test_perform_pickup_food(self):
        """Pick up an Item"""
        level = Level(1, 80, 25, None)
        p = Player(pos=Pos(10, 10))
        p.queue_action(PickupAction())
        p.attach_level(level)
        food = Food(which=Food.FRUIT, pos=Pos(10, 10), parent=level)
        level.add_item(food)
        # Smoke test: is where we think
        assert level.items == [food]
        assert food.parent == level
        p.perform()
        # Action occurred
        assert p.curr_msg == 'You pick up the slime-mold'
        # Gone from level
        assert level.items == []  # Gone from map
        # Into player inventory
        assert food.parent == p
        assert food in p.pack
        self.assertTrue(True)

    def test_perform_descend(self):
        """Stumble down the stairs"""
        p = Player.factory(pos=Pos(10, 10))
        p.queue_action(DescendAction())
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
        p.queue_action(DescendAction())
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
        p.queue_action(DropAction().incorporate(0))
        # Factory creates a food in player inventory
        assert p.pack != []
        food = p.pack[0]
        assert food.parent == p
        assert food.pos is None
        level = Level(1, 80, 25, None)
        level.add_player(p)
        p.perform()
        assert food.parent == level
        assert food.pos == p.pos
        assert food in level.items
        self.assertTrue(True)

    def test_perform_drop_badindex(self):
        """Invalid object index - drop"""
        p = Player.factory(pos=Pos(10, 10))
        p.queue_action(DropAction().incorporate(1))
        # Factory creates a food in player inventory
        p.perform()
        assert p.curr_msg == 'No such item to drop!'
        self.assertTrue(True)

    def test_perform_use_badindex(self):
        """Invalid object index - use"""
        p = Player.factory(pos=Pos(10, 10))
        p.queue_action(UseAction().incorporate(1))
        # Factory creates a food in player inventory
        p.perform()
        assert p.curr_msg == 'No such item to use!'
        self.assertTrue(True)

    def test_perform_equip_badindex(self):
        """Invalid object index - equip"""
        p = Player.factory(pos=Pos(10, 10))
        p.queue_action(EquipAction().incorporate(1))
        # Factory creates a food in player inventory
        p.perform()
        assert p.curr_msg == 'No such item to equip!'
        self.assertTrue(True)

    def test_perform_equip_armor(self):
        """Drop the nonexistent food in your inventory"""
        p = Player(pos=Pos(10, 10))
        p.queue_action(EquipAction().incorporate(0))
        assert p.armor is None
        armor = Equipment.factory(etype=Equipment.ARMOR, template='name=fake_armor value=6 worth=10')
        p.add_item(armor)
        assert p.pack == [armor]
        p.perform()
        assert p.pack == [armor]
        assert p.armor == armor
        assert p.curr_msg == 'You put on the fake armor'
        self.assertTrue(True)

    def test_perform_drop_equipped_armor(self):
        """Drop the thing in your inventory"""
        p = Player.factory(pos=Pos(10, 10))
        level = Level(1, 80, 25, None)
        level.add_player(p)
        p.queue_action(DropAction().incorporate(1))  # Factory gives one food
        armor = Equipment.factory(etype=Equipment.ARMOR, template='name=fake_armor value=6 worth=10')
        p.add_item(armor)
        p.armor = armor
        p.perform()
        assert armor not in p.pack
        assert p.curr_msg == 'You take off the fake armor --MORE--'
        p.advance_msg()
        assert p.curr_msg == 'You drop the fake armor'
        self.assertTrue(True)

    def test_perform_use_food(self):
        """Use the nonexistent food in your inventory"""
        p = Player.factory(pos=Pos(10, 10))
        p.queue_action(UseAction().incorporate(0))
        # Factory creates a food in player inventory
        assert p.pack != []
        p.perform()
        print(p.curr_msg)
        assert p.pack == []
        # TODO: can't test existence of food
        # TODO: there was a message and effects
        assert p.curr_msg != ''
        self.assertTrue(True)

    # TODO: use action that doesn't destroy item

    # TODO: bump actions, etc.


# ===== Test Combat Interface =============================

class TestPlayerCombat(unittest.TestCase):
    """Player Combat Interface"""

    def test_melee_attack(self):
        """Melee attack features plus effect of equipment"""
        p = Player.factory()
        level, stren, dmg, dplus = p.melee_attack()
        assert level == 1
        assert stren == 16
        assert dmg == '1x4'
        assert dplus == 0
        w = Equipment.factory(etype=Equipment.WEAPON, template='name=fake dam=1x6')
        p.add_item(w)
        p.weapon = w
        w.dplus = 2
        w.hplus = 1
        level, stren, dmg, dplus = p.melee_attack()
        assert dmg == '1x6'
        assert level == 2
        assert dplus == 2
        self.assertTrue(True)

    def test_ac(self):
        """Armor class and the effect of equipment"""
        p = Player.factory()
        assert p.ac == 10
        armor = Equipment.factory(etype=Equipment.ARMOR, template='name=fake_armor value=6 worth=10')
        p.add_item(armor)
        p.armor = armor
        assert p.ac == 6
        self.assertTrue(True)


# ===== Invocation ========================================

if __name__ == '__main__':
    unittest.main()

# EOF
