from copy import deepcopy
from random import randint

# Hard Rules
MAX_CONSECUTIVE_BLOCKS_PER_ANCHOR = 3
MAX_NUMBER_BLOCKS_PER_ANCHOR = 4

# Optimization, values 0<x<=100
WEIGHT_CONSECUTIVE_BLOCKS = 50
WEIGHT_NUMBER_BLOCKS = 50
WEIGHT_START_TO_END_BLOCKS = 50
WEIGHT_STARTING_TIME = 50
PENALIZE_LATER_THAN = 12  # I.e. later than noon

MAX_ITERATIONS_DEFAULT = 100 


class Anchor(object):
    def __init__(self, name, **kwargs):
        self.name = name

    def __repr__(self):
        return self.name


# Anchors
NORA = Anchor(name='Nora')
BRAD = Anchor(name='Brad')
BAKER = Anchor(name='Baker')
HOPE = Anchor(name='Hope')
KRISTEN = Anchor(name='Kristen')
TIM = Anchor(name='Tim')
ANCHORS_FULLTIME = [NORA, BRAD, BAKER, HOPE, KRISTEN, TIM]
ANCHORS_PER_BLOCK_DEFAULT = 2


class Schedule(object):
    def __init__(self, blocks, **kwargs):
        self.blocks = blocks # must be an ordered list of Blocks
        self.available_anchors = kwargs.get('available_anchors', ANCHORS_FULLTIME)

    def __repr__(self):
        output = ''
        for block in self.blocks:
            output += str(block) + '\n'
        return output

    @property
    def complete(self):
        """Returns True if schedule is complete."""
        for block in self.blocks:
            if not block.full:
                return False
        return True

    def number_blocks(self, **kwargs):
        """
        Returns number of blocks for an anchor, or the max of all anchors.

        kwargs:
            anchors = a list of Anchor() object
        """

        anchors = kwargs.get('anchors', self.available_anchors)
        blocks_max = 0
        
        for anchor in anchors:
            blocks_num = 0
            for block in self.blocks:
                if anchor in block.anchors:
                    blocks_num += 1

            blocks_max = max(blocks_max, blocks_num)
        
        return blocks_max

    @property
    def safe_number_blocks(self):
        """Returns True if this day satisifies maximum number of blocks rule."""
        return self.number_blocks() <= MAX_NUMBER_BLOCKS_PER_ANCHOR

    def consecutive_blocks(self, **kwargs):
        """
        Returns consecutive blocks for an anchor, or the max of all anchors.

        kwargs:
            anchors = a list of Anchor() objects
        """

        anchors = kwargs.get('anchors', self.available_anchors)
        consecutive_blocks_max = 0
        
        for anchor in anchors:
            consecutive_blocks = 0
            for block in self.blocks:
                if anchor in block.anchors:
                    consecutive_blocks += 1
                else:
                    consecutive_blocks = 0
            consecutive_blocks_max = max(consecutive_blocks, consecutive_blocks_max)
        
        return consecutive_blocks_max


    @property
    def safe_consecutive_blocks(self):
        """Returns True if this day satisifies maximum number of blocks rule."""
        return self.consecutive_blocks() <= MAX_CONSECUTIVE_BLOCKS_PER_ANCHOR


    def start_block_for(self, anchor):
        """Returns the first block for anchor."""
        for block in self.blocks:
            if anchor in block.anchors:
                return block

    def end_block_for(self, anchor):
        """Returns the first block for anchor."""
        for block in reversed(self.blocks):
            if anchor in block.anchors:
                return block

    def start_to_end_blocks(self, **kwargs):
        """
        Returns number of blocks from start to end for an anchor, or the max of all anchors.

        kwargs:
            anchors = a list of Anchor() objects
        """

        anchors = kwargs.get('anchors', self.available_anchors)
        blocks_length_max = 0
        
        for anchor in anchors:
            start_block = self.start_block_for(anchor)
            if start_block:
                blocks_length = self.end_block_for(anchor).hour - start_block.hour
                blocks_length_max = max(blocks_length, blocks_length_max)
        
        return blocks_length_max

    @property
    def value(self):
        """Returns the optimization value of this schedule. Lower values are more optimized."""
        value = 0

        for anchor in self.available_anchors:
            value += self.number_blocks(anchors=[anchor]) * WEIGHT_NUMBER_BLOCKS
            value += self.consecutive_blocks(anchors=[anchor]) * WEIGHT_CONSECUTIVE_BLOCKS
            value += self.start_to_end_blocks(anchors=[anchor]) * WEIGHT_START_TO_END_BLOCKS

            # Weight before noon start time for all anchors
            start_block = self.start_block_for(anchor)
            if start_block and start_block.hour > PENALIZE_LATER_THAN:
                value += (start_block.hour - PENALIZE_LATER_THAN) * WEIGHT_STARTING_TIME

        return value


class Block(object):
    def __init__(self, hour, **kwargs):
        # Require kwargs
        # self.name
        self.hour = hour  # upgrade to datetime and timedelta length
        
        # Default 2 anchors per block
        self.num_anchors = kwargs.get('num_anchors', ANCHORS_PER_BLOCK_DEFAULT)

        # Default allow any anchor
        self.matching_anchors = kwargs.get('matching_anchors', ANCHORS_FULLTIME)

        # Optionally set a list of specific anchors
        self.anchors = set(kwargs.get('anchors', []))
        if len(self.anchors) > self.num_anchors:
            raise

    def __repr__(self):
        if self.anchors:
            anchors = self.anchors
        else:
            anchors = 'Empty'
        return f'Block {self.hour}, {self.num_anchors} anchors: {anchors}'

    @property
    def full(self):
        if len(self.anchors) > self.num_anchors:
            raise
        return len(self.anchors) == self.num_anchors
    

    def random_fill(self):
        """Randomly fills block with matching anchors."""
        while not self.full:
            self.anchors.add(
                self.matching_anchors[ randint(0, len(self.matching_anchors)-1) ]
            )
        return True


class ScheduleOptimizer(object):
    def __init__(self, schedule, **kwargs):
        self.base_schedule = schedule  # The day to be scheduled
        self.schedules = []
        
        # How many iterations of scheduling to attempt
        self.max_iterations = kwargs.get('max_iterations', MAX_ITERATIONS_DEFAULT)
        self.fill_schedules()

        self.schedules = sorted(self.schedules, key=lambda x: x.value, reverse=True)

    def fill_schedules(self):
        # Calculates max_num unoptimized schedules.
        # All schedules meet the minimum Hard Requirements
        iteration = 0

        while iteration <= self.max_iterations:
            schedule = deepcopy(self.base_schedule)
            
            [block.random_fill() for block in schedule.blocks]

            if schedule.safe_number_blocks and schedule.safe_consecutive_blocks:
                self.schedules.append(schedule)

            iteration += 1

        return True

    @property
    def best_schedule(self):
        return self.schedules[0]



if __name__ == "__main__":
    
    blocks = [Block(hour=i) for i in range(1, 10)]
    day = Schedule(blocks=blocks)


    s = ScheduleOptimizer(day)
    print(f'Generated {len(s.schedules)} schedules from {s.max_iterations} iterations')
    print('Best Schedule:')
    print(s.best_schedule)
    