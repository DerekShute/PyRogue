"""
    The tuples of strings to feed into factory constructors
"""

#
# 'worth' : value that gets added to score calculation
# 'prob' : Chance (weighted somehow) that feed into the chance-of-finding at level generation
#
ARMOR_TEMPLATES = (
    'name=leather_armor prob=20 worth=20 value=8',  # AC 8
    'name=ring_mail prob=15 worth=25 value=7',      # AC 7
    'name=studded_leather_armor prob=15 worth=20 value=7', # AC 7
    'name=scale_mail prob=13 worth=30 value=6',  # AC 6
    'name=chain_mail prob=12 worth=75 value=5',  # AC 5
    'name=splint_mail prob=10 worth=80 value=4',  # AC 4
    'name=banded_mail prob=10 worth=90 value=4',  # AC 4
    'name=plate_mail prob=5 worth=150 value=3',   # AC 3
)

# TODO: - Need three generators here: value calculation at RIP/END, probability for level generation, and the
# factory for items.

# ===== Probability calculations and whatnot ==============

