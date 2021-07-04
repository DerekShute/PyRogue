"""
    Player
"""

import random
from entity import Entity
from dataclasses import dataclass
from item import Item, Food, Equipment
from position import Pos
from message import MessageBuffer
from combat import fight
from level import Level
from menu import Menu


ACTION_COST = 8
"""Everything costs 8 ticks"""

HUNGERTIME = 1300
"""Turns before hunger state change, I guess"""

STOMACHSIZE = 2000
"""Limit on food intake.  No amusing consequences for going over."""

INIT_STATS = {
    'level': 1,
    'stren': 16,
    'arm': 10,    # Unarmed
    'maxhp': 12,
    'dmg': '1x4'  # Unarmed damage
}

PLAYER_CHAR = ord('@')

PLAYER_COLOR = (255, 255, 255)  # White TODO: consolidate definitions

HIT_NAMES = (
    "scored an excellent hit on",
    "hit",
    "have injured",
    "swing and hit",
    "scored an excellent hit on",
    "hit",
    "has injured",
    "swings and hits"
)

PLAYER_MISS = (
    "miss",
    "swing and miss",
    "barely miss",
    "don't hit"
)

MONSTER_MISS = (
    "misses",
    "swings and misses",
    "barely misses",
    "doesn't hit",
)

E_LEVELS = (
    0,   # No level 0 but need to do index magic
    0,   # 0 XP at level 1
    10,  # 10 XP at level 2
    20,
    40,
    80,
    160,
    320,
    1300,
    2600,
    5200,
    13000,
    26000,
    50000,
    100000,
    200000,
    400000,
    800000,
    2000000,
    4000000,
    8000000
    )


# ===== Service Routines ==================================

def die_roll(number: int, sides: int) -> int:
    total = 0
    count = 0
    while count < number:
        total += random.randint(1, sides)
        count += 1
    return total


# ===== Stats =============================================

@dataclass
class Stats:  # struct stats
    """
    Structure describing a fighting being
    """
    stren: int
    arm: int   # TODO: base AC 10
    dmg: str
    maxhp: int
    hpt: int = None
    exp: int = 0  # TODO: xp count for player, xp value for monsters
    level: int = 0

    def __post_init__(self):
        if self.hpt is None:
            self.hpt = self.maxhp

    def __str__(self):
        return f'Stats(Str={self.stren},XP={self.exp}({self.level}),AC={self.arm},' \
               f'Dmg=\'{self.dmg}\',HP={self.hpt}/{self.maxhp})'

    # ===== Combat ========================================

    def melee_attack(self):
        """Attack components just based on stats"""
        return self.level, self.stren, self.dmg

    @property
    def ac(self):
        """Armor class"""
        return self.arm


# ===== Player ============================================

class Player(Entity):
    _food_left: int
    _stats: Stats = None
    _cur_armor: Item = None
    _msg: MessageBuffer = None
    purse: int = 0  # Gold collected, an infinitely large pocket
    levelno: int = 0  # How deep in the dungeon? (May disconnect from _level, so keep here)
    room = None  # Room
    actionq = []
    armor: Equipment = None
    weapon: Equipment = None

    def __init__(self, pos: Pos = None, stats: Stats = None, food_left: int = HUNGERTIME):
        super().__init__(pos=pos, mtype=PLAYER_CHAR, color=PLAYER_COLOR, name='Player')
        self._msg = MessageBuffer()
        self._stats = stats
        self._food_left = food_left
        self.levelno = 0
        self.actionq = []

    def __str__(self):
        return f'Player({Pos(self.pos)},{self._stats})'

    def __repr__(self):
        # TODO: inventory
        return f'Player(pos={repr(self.pos)},stats={repr(self._stats)},food_left={self._food_left})'

    # ===== Display =======================================

    @property
    def display(self) -> str:
        """Status-line"""
        # TODO: originally 'Level: <dungeon level> Gold: %d Hp: %d/%d Str:%d(%d) Arm: %d Exp:%lvl/%xp <status>'
        return f'Level: {self.levelno} Gold: {self.purse} Hp:{self._stats.hpt}/{self._stats.maxhp} ' \
               f'Str:{self._stats.stren}({self._stats.stren}) Arm: {self.ac} Exp:{self._stats.level}({self._stats.exp})'

    def render_inventory(self, usage: str) -> Menu:
        inventory = []
        if usage == '':
            title = 'inventory'
        else:
            title = usage

        listing = ord('a')
        for item in self.pack:
            if self.armor == item:
                desc = f'{item.description} (being worn)'
            elif self.weapon == item:
                desc = f'{item.description} (wielded)'
            else:
                desc = f'{item.description}'

            if usage == '':
                inventory.append(desc)  # TODO: consolidate similar objects
                continue

            add_it = False
            if usage == 'drop':
                add_it = True
            elif usage == 'use' and item.name == 'food':
                add_it = True
            elif usage == 'equip' and isinstance(item, Equipment):
                add_it = True
            if add_it:
                inventory.append(f'{chr(listing)}: {desc}')  # TODO: consolidate
            listing = listing + 1
        return Menu(title=title, text=inventory)

    # ===== Base Interface ================================

    def attach_level(self, level: Level):
        self.level = level
        self.levelno = level.levelno if level is not None else self.levelno

    # ===== Messaging and message buffer ==================

    def add_msg(self, text: str):
        self._msg.add(text)  # TODO: censor message for visibility of source, etc.

    def advance_msg(self):
        self._msg.advance()

    @property
    def curr_msg(self):
        if self._msg.count == 0:
            return self.display
        if self._msg.count > 1:
            return f'{self._msg.msg} --MORE--'
        else:
            return self._msg.msg

    @property
    def msg_count(self) -> int:
        return self._msg.count

    # ===== Action ========================================

    def queue_action(self, action):
        self.actionq.append(action)

    def get_action(self):
        return self.actionq.pop(0) if len(self.actionq) > 0 else None

    def fight(self, entity: Entity):
        fight(self, entity)

    def bump(self, pos: Pos):
        assert pos
        self.add_msg('Ouch!')

    def descend(self):
        self.add_msg('You stumble down the stairs.')  # TODO: real message?
        self.level.remove_player()
        self.levelno = self.levelno + 1
        # Once not on the level, the game main loop takes care of it

    def drop(self, item: Item):
        if self.armor == item or self.weapon == item:
            self.equip(item)
        self.add_msg(f'You drop the {item.name}')
        self.remove_item(item)  # Remove it from inventory
        item.set_parent(None)
        item.pos = self.pos
        self.level.add_item(item)
        item.set_parent(self.level)

    def equip(self, item: Equipment):
        def equip_weapon():
            if self.weapon is None:
                self.add_msg(f'You wield the {item.name}')
                self.weapon = item
            elif self.weapon == item:
                self.add_msg(f'You put away the {item.name}')
                self.weapon = None
            else:
                self.equip(self.weapon)
                self.equip(item)

        def equip_armor():
            if self.armor is None:
                self.add_msg(f'You put on the {item.name}')
                self.armor = item
            elif self.armor == item:
                self.add_msg(f'You take off the {item.name}')
                self.armor = None
            else:
                self.equip(self.armor)
                self.equip(item)

        if item.etype == Equipment.WEAPON:
            equip_weapon()
        if item.etype == Equipment.ARMOR:
            equip_armor()

    def move(self, dx: int, dy: int):
        self.pos = Pos(self.pos.x + dx, self.pos.y + dy)  # TODO: Pos addition
        self.room = self.level.new_room(self.pos, self.room)
        # TODO : returns timer tick cost

    def pick_up(self, item: Item):
        # TODO: limit to inventory
        if item is None:
            self.add_msg('No item there to pick up!')
            return
        item.parent.remove_item(item)  # Remove it from the level
        item.set_parent(None)
        item.pos = None
        if item.name == 'gold':
            # AD&D would award XP for treasure, but not Rogue apparently
            self.add_msg(f'You pick up {item.quantity} gold pieces!')
            self.purse = self.purse + item.quantity
            del item  # Poof
        else:
            self.add_msg(f'You pick up the {item.name}')
            self.add_item(item)
            item.set_parent(self)
            # TODO: after verifying you can

    def use(self, item: Item):
        """Use an item"""
        destroy = item.use(self)
        if destroy:
            item.set_parent(None)
            self.remove_item(item)
            del item

    # ===== Timer / AI / Action Interface ==========================

    def perform(self) -> bool:
        """Act.  Return True to indicate reschedule"""
        action = self.get_action()
        if action is not None:
            self.advance_msg()
            action.perform(self)  # TODO: action cost, haste and slow effects
            self.key = self.key + ACTION_COST
        return True

    # ===== Stat interface ================================

    @property
    def lvl(self) -> int:
        return self._stats.level

    @property
    def hpt(self) -> int:
        return self._stats.hpt

    @property
    def exp(self) -> int:
        return self._stats.exp

    def add_exp(self, amount: int):
        self._stats.exp = self._stats.exp + amount
        # see check_level()
        new_lvl = 0
        for lvl in range(self._stats.level, len(E_LEVELS)):
            if self._stats.exp < E_LEVELS[lvl]:
                break
            new_lvl = lvl
        if new_lvl > self._stats.level:
            add = die_roll(new_lvl - self._stats.level, 10)
            self._stats.level = new_lvl
            self._stats.maxhp += add
            self._stats.hpt += add
            self.add_msg(f'Welcome to level {new_lvl}')

    @property
    def stren(self) -> int:
        # TODO: effects of equipment
        return self._stats.stren

    @property
    def food_left(self) -> int:
        return self._food_left

    def add_food(self):
        """Eat a piece of food.  Fruit or ration does not matter"""
        if self._food_left < 0:
            self._food_left = 0
            return
        self._food_left = self._food_left + HUNGERTIME - 200 + random.randint(0, 400)
        if self._food_left > STOMACHSIZE:
            # I thought there was some vomit case but maybe in a different game
            self._food_left = STOMACHSIZE

    # ===== Combat Interface ==============================

    @property
    def ac(self):
        """Armor class"""
        # TODO: account for armor, rings, whatever
        if self.armor is not None:
            return self.armor.value
        return self._stats.ac

    def add_hit_msg(self, entity):
        self.add_msg(f'You {random.choice(HIT_NAMES)} the {entity.name}')

    def add_was_hit_msg(self, entity):
        self.add_msg(f'The {entity.name} {random.choice(HIT_NAMES)} you')

    def add_miss_msg(self, entity):
        self.add_msg(f'You {random.choice(PLAYER_MISS)} the {entity.name}')

    def add_was_missed_msg(self, entity):
        self.add_msg(f'The {entity.name} {random.choice(MONSTER_MISS)} you')

    def death(self, entity):
        self.msg(f'You were killed by the {entity.name}!')  # TODO traps?
        # TODO raise end-of-game

    def kill(self, entity):  # TODO: monster
        self.add_msg(f'You killed the {entity.name}!')
        self.add_exp(entity.xp_value)

    def melee_attack(self):
        """Melee attack (level, strength, dmg)"""
        # TODO: effect of objects.  I think it can add to level instead of an explicit bonus
        level, stren, dmg = self._stats.melee_attack()
        if self.weapon is not None:
            dmg = self.weapon.dam
            level += self.weapon.hplus
            # TODO: starting mace is +1 damage...figure that out
        return level, stren, dmg

    def take_damage(self, amount: int):
        """Took it on the chin"""
        self._stats.hpt = max(0, self._stats.hpt - amount)

    @property
    def xp_value(self) -> int:
        return 0  # TODO: how did we get here?

    # ===== Constructor ===================================

    @staticmethod
    def factory(pos: Pos = None):   # init_player
        plr = Player(pos=pos, stats=Stats(**INIT_STATS))
        # cur_armor Armor: ring_mail, known, a_class = RING_MAIL

        # one food.  I think a ration, if I'm reading correctly
        food = Food(which=Food.GOOD_RATION)
        food.set_parent(plr)
        plr.add_item(food)

        # cur_weapon Weapon: mace, known, hplus=1 dplus=1
        # weapon: BOW, hplus=1, known
        # to pack: 25 + rnd(15) arrows, known
        return plr


# ===== Unit Test =========================================

# See test_player.py

# EOF
