"""
    Player
"""

import random
from entity import Entity
from dataclasses import dataclass
from typing import Tuple, Dict, Set, List
from item import Item, Food, Equipment, Consumable
from position import Pos
from message import MessageBuffer
from level import Level
from menu import Menu
from player.wizard import wizard_request


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
        return self.level, self.stren, self.dmg, 0

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
    rings: List[Equipment] = []
    demise: str = None
    max_str: int = 0
    effects: Dict[str, int] = {}  # Things affecting player: being confused, being hasted...
    known: Set[str] = set()       # Things that are known: what a blue potion is, etc...
    wizard: bool  # Wizard mode
    
    def __init__(self, pos: Pos = None, stats: Stats = None, food_left: int = HUNGERTIME, wizard:bool = False):
        super().__init__(pos=pos, mtype=PLAYER_CHAR, color=PLAYER_COLOR, name='Player')
        self._msg = MessageBuffer()
        self._stats = stats
        self._food_left = food_left
        self.levelno = 0
        self.actionq = []
        self.demise = None
        self.max_str = stats.stren if stats is not None else None
        self.effects = {}
        self.wizard = wizard

    def __str__(self):
        return f'Player({Pos(self.pos)},{self._stats})'

    def __repr__(self):
        # TODO: inventory, max strength, effects
        return f'Player(pos={repr(self.pos)},stats={repr(self._stats)},food_left={self._food_left})'

    # ===== Display =======================================

    @property
    def display(self) -> str:
        """Status-line"""
        # TODO: originally 'Level: <dungeon level> Gold: %d Hp: %d/%d Str:%d(%d) Arm: %d Exp:%lvl/%xp <hunger status>'
        return f'Level: {self.levelno} Gold: {self.purse} Hp:{self._stats.hpt}/{self._stats.maxhp} ' \
               f'Str:{self.stren}({self.max_str}) Arm: {self.ac} Exp:{self._stats.level}({self._stats.exp})'

    def render_inventory(self, usage: str) -> Menu:
        inventory = []
        if usage == '':
            title = 'inventory'
        else:
            title = usage

        listing = ord('a')
        for item in self.pack:
            if item in self.rings:
                desc = f'{item.description(self.known)} (being worn)'
            elif self.armor == item:
                desc = f'{item.description(self.known)} (being worn)'
            elif self.weapon == item:
                desc = f'{item.description(self.known)} (wielded)'
            else:
                desc = f'{item.description(self.known)}'

            if usage == '':
                inventory.append(desc)  # TODO: consolidate similar objects
                continue

            add_it = False
            if usage == 'drop':
                add_it = True
            elif usage == 'use':
                if item.name == 'food':  # TODO: food as consumable
                    add_it = True
                elif isinstance(item, Consumable):
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

    def quit_action(self, cause: str):
        """Player has quit or player has died"""
        self.demise = cause

    def queue_action(self, action):
        """Input handler drops an Action onto the queue"""
        if action is not None:
            self.actionq.append(action)

    def bump(self, pos: Pos):
        assert pos
        self.add_msg('Ouch!')

    def chat(self, text: str):
        if self.wizard:
            wizard_request(self, text)
        else:
            self.add_msg(f'Someone shouts "{text}"!')

    def descend(self):
        self.add_msg('You stumble down the stairs.')  # TODO: real message?
        self.level.remove_player()
        self.levelno = self.levelno + 1
        # Once not on the level, the game main loop takes care of it

    def drop(self, item: Item):
        if self.armor == item or self.weapon == item or item in self.rings:
            self.equip(item)
        self.add_msg(f'You drop the {item.description(self.known)}')
        self.remove_item(item)  # Remove it from inventory
        item.set_parent(None)
        item.pos = self.pos
        self.level.add_item(item)
        item.set_parent(self.level)

    def equip(self, item: Item):
        def equip_weapon():
            if self.weapon is None:
                self.add_msg(f'You wield the {item.description(self.known)}')
                self.weapon = item
            elif self.weapon == item:
                self.add_msg(f'You put away the {item.description(self.known)}')
                self.weapon = None
            else:
                self.equip(self.weapon)
                self.equip(item)

        def equip_armor():
            if self.armor is None:
                self.add_msg(f'You put on the {item.description(self.known)}')
                self.armor = item
            elif self.armor == item:
                self.add_msg(f'You take off the {item.description(self.known)}')
                self.armor = None
            else:
                self.equip(self.armor)
                self.equip(item)

        def equip_ring():
            # WONT-DO: believe it or not, there was a dialog to choose which hand.  I can't see how it matters
            if item in self.rings:
                self.add_msg(f'You take off the {item.description(self.known)}')
                self.rings.remove(item)
            elif len(self.rings) > 1:
                self.add_msg('You already have a ring on each hand')
            else:
                self.add_msg(f'You put on the {item.description(self.known)}')
                self.rings.append(item)

        if not isinstance(item, Equipment):
            self.add_msg(f'The {item.description(self.known)} cannot be equipped.')
            return

        # TODO: cannot un-equip cursed items

        if item.etype == Equipment.WEAPON:
            equip_weapon()
        if item.etype == Equipment.ARMOR:
            equip_armor()
        if item.etype == Equipment.RING:
            equip_ring()

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
            self.add_msg(f'You pick up the {item.description(self.known)}')
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
        if len(self.actionq) > 0:
            action = self.actionq.pop(0)
            self.advance_msg()
            action.perform(self)  # TODO: action cost, haste and slow effects
            self.key = self.key + ACTION_COST
            self.countdown_effects()
            # TODO: hunger and ring effects on hunger
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
        while self._stats.level < new_lvl:
            self.raise_level()

    @property
    def stren(self) -> int:
        """Effective player strength: includes ring of add strength"""
        stren = self._stats.stren
        for ring in self.rings:
            if ring.name == 'add strength':
                stren += ring.hplus  # This is correct: sum of adjustments
        return stren

    @property
    def food_left(self) -> int:
        return self._food_left

    def raise_level(self):
        """Player level++: you can arrive here via magic effect"""
        add = die_roll(1, 10)
        self._stats.level += 1
        if self._stats.exp < E_LEVELS[self._stats.level]:
            self._stats.exp = E_LEVELS[self._stats.level] + 1
        self._stats.maxhp += add
        self._stats.hpt += add
        self.add_msg(f'Welcome to level {self._stats.level}')

    # ===== Combat Interface ==============================

    @property
    def ac(self):
        """Armor class: Affected by armor and rings of protection"""
        if self.armor is not None:
            ac = self.armor.value - self.armor.hplus # AD&D - subtract to improve
        else:
            ac = self._stats.ac
        for ring in self.rings:
            if ring.name == 'protection':
                ac -= ring.hplus  # This is correct: sum of adjustments
        return ac

    def add_hit_msg(self, entity):
        self.add_msg(f'You {random.choice(HIT_NAMES)} the {entity.name}')

    def add_was_hit_msg(self, entity):
        self.add_msg(f'The {entity.name} {random.choice(HIT_NAMES)} you')

    def add_miss_msg(self, entity):
        self.add_msg(f'You {random.choice(PLAYER_MISS)} the {entity.name}')

    def add_was_missed_msg(self, entity):
        self.add_msg(f'The {entity.name} {random.choice(MONSTER_MISS)} you')

    def death(self, entity):
        self.add_msg(f'You were killed by the {entity.name}!')  # TODO traps?
        self.demise = entity.name

    def kill(self, entity):  # TODO: monster
        self.add_msg(f'You killed the {entity.name}!')
        self.add_exp(entity.xp_value)

    def melee_attack(self) -> Tuple[int, int, str, int]:
        """Melee attack (level, strength, dmg, dplus): affected by weapon bonuses and rings"""
        level, stren, dmg, dplus = self._stats.melee_attack()
        if self.weapon is not None:
            dmg = self.weapon.dam
            level += self.weapon.hplus
            dplus += self.weapon.dplus
        for ring in self.rings:  # This is correct: sum of adjustments
            if ring.name == 'increase damage':
                dplus += ring.hplus
            elif ring.name == 'dexterity':
                level += ring.hplus
        return level, stren, dmg, dplus

    def take_damage(self, amount: int):
        """Took it on the chin"""
        self._stats.hpt = max(0, self._stats.hpt - amount)

    @property
    def xp_value(self) -> int:
        return 0  # TODO: how did we get here?

    # ===== Effects of things =============================

    def add_effect(self, key: str, countdown: int):
        """Add an effect as a result of potion or monster or whatnot"""
        self.effects[key] = countdown

    def remove_effect(self, key: str):
        """Remove an effect outright"""
        _ = self.effects.pop(key)

    def countdown_effects(self):
        """Count down all the effects affecting player"""
        ridlist = []
        # TODO: permanent effects have countdown of 0, -1?
        for key, value in self.effects.items():
            if value <= 1:
                # Can't change the dictionary during the iteration, so keep track of what to delete
                ridlist.append(key)
            else:
                self.effects[key] -= 1
        for key in ridlist:
            _ = self.effects.pop(key)
            # TODO: most have choose_str() based on hallucinating
            if key == 'confused':  # unconfuse()
                self.add_msg('You feel less confused now.')
            elif key == 'blind':   # sight()
                self.add_msg('The veil of darkness lifts.')
            elif key == 'hasted':  # nohaste()
                self.add_msg('You feel yourself slowing down.')
            elif key == 'hallucinating':  # come_down()
                self.add_msg('Everything looks SO boring now.')
            elif key == 'levitating':     # land()
                self.add_msg('You float gently to the ground.')

    def add_food(self):
        """Eat a piece of food.  Fruit or ration does not matter"""
        # TODO: this is food.use() ?
        if self._food_left < 0:
            self._food_left = 0
            return
        self._food_left = self._food_left + HUNGERTIME - 200 + random.randint(0, 400)
        if self._food_left > STOMACHSIZE:
            # I thought there was some vomit case but maybe in a different game
            self._food_left = STOMACHSIZE

    def add_hp(self, amount: int):
        """Restore hit points, per healing potion"""
        self._stats.hpt += amount
        if self._stats.hpt > self._stats.maxhp:
            self._stats.maxhp += 1
            self._stats.hpt = self._stats.maxhp

    def change_str(self, amount: int):
        """Adjust strength.  Possibly adjust max to reflect"""
        # TODO: Not if wearing ring of sustain strength
        self._stats.stren += amount
        if amount > 0 and self._stats.stren > self.max_str:
            self.max_str = self._stats.stren

    def restore_strength(self):
        """Restore strength to maximum, do not exceed it"""
        if self._stats.stren < self.max_str:
            self._stats.stren = self.max_str
            # TODO: message here instead of in potions.py

    # ===== Constructor ===================================

    @staticmethod
    def factory(pos: Pos = None, wizard: bool = False):   # init_player
        plr = Player(pos=pos, stats=Stats(**INIT_STATS), wizard=wizard)
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
