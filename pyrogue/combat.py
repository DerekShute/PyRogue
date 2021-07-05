"""
    Combat Formulae
"""
import random


ADD_DMG = (-7, -6, -5, -4, -3, -2, -1, 0, 0, 0, 0, 0, 0, 0, 0, 0,  # 0-15
           1, 1, 2, 3, 3, 4, 5, 5, 5, 5, 5, 5, 5, 5, 5, 6)
"""adjustments to damage done due to strength (0-31)"""

STR_PLUS = (-7, -6, -5, -4, -3, -2, -1, 0, 0, 0, 0, 0, 0, 0, 0, 0,  # 0-15
            0, 1, 1, 1, 1, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 3)
"""adjustments to hit probabilities due to strength"""


# ===== Useful Methods ====================================

def swing(attacker_level: int, defender_armor: int, attack_bonus: int = 0) -> bool:
    """Returns true if the swing hits"""
    die_roll = random.randint(0, 19)  # Given rnd(20), which is 0..19
    needs = 20 - attacker_level - defender_armor  # TODO: funky old school table math here
    return (die_roll + attack_bonus >= needs)


def roll(die_roll: str) -> int:
    """dmg as string in format COUNTxSIDES"""
    # TODO: goes elsewhere
    # TODO: there's special rules for one of the dmg descriptors
    count, _, sides = die_roll.partition('x')
    total = 0
    count = int(count)  # No elegant way to do this with _ in the middle
    sides = int(sides)
    while count > 0:
        total = total + random.randint(1, sides)
        count = count - 1
    return total


# ===== roll_em ===========================================

def roll_em(attacker, defender) -> int:  # TODO: weapon, 'hurl'
    """Roll several attacks, which are describe in the XxY/AxB/CxD damage string"""
    at_lvl, at_stren, at_dmg, at_dplus = attacker.melee_attack()
    ac = defender.ac
    damage = 0
    for attack in at_dmg.split('/'):  # TODO: some monsters have weird strings here
        if swing(at_lvl, ac, STR_PLUS[at_stren]):  # TODO: just roll this into attacker/defender logic
            damage = damage + roll(attack) + ADD_DMG[at_stren] + at_dplus
    return damage


# ===== fight =============================================

def fight(attacker, defender):  # TODO: weapon, thrown
    """The player attacks the monster."""
    # TODO: this resets quiet time, so no healing
    # TODO: resets disguise, and if so ends the attack
    # TODO: hallucination, which should probably be handled in level rendering
    damage = roll_em(attacker, defender)
    if damage > 0:
        attacker.add_hit_msg(defender)  # TODO thrown
        defender.add_was_hit_msg(attacker)
        defender.take_damage(damage)
        if defender.hpt <= 0:
            attacker.kill(defender)
            defender.death(attacker)
            del defender
        # TODO: if player can confuse monster, resolve that
    else:
        attacker.add_miss_msg(defender)
        defender.add_miss_msg(attacker)
    # TODO: returns boolean in some cases, for some reason


# ===== Testing ===========================================

# Not here: look in test_combat.py

# EOF
