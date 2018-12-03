from models.anchor import Anchor

# Hard Rules
MAX_CONSECUTIVE_BLOCKS_PER_ANCHOR = 3
MAX_NUMBER_BLOCKS_PER_ANCHOR = 4

# Optimization, values 0<x<=100
WEIGHT_CONSECUTIVE_BLOCKS = 20
WEIGHT_NUMBER_BLOCKS = 50
WEIGHT_START_TO_END_TIME = 40
WEIGHT_STARTING_TIME = 50
PENALIZE_LATER_THAN = 12  # I.e. later than noon

MAX_ITERATIONS_DEFAULT = 100


# Anchors
NORA = Anchor(name='Nora')
BRAD = Anchor(name='Brad')
BAKER = Anchor(name='Baker')
HOPE = Anchor(name='Hope')
KRISTEN = Anchor(name='Kristen')
TIM = Anchor(name='Tim')
JIMMY = Anchor(name='Jimmy')

ANCHORS_FULLTIME = [NORA, BRAD, BAKER, HOPE, KRISTEN, TIM]
ANCHORS_PER_BLOCK_DEFAULT = 2
