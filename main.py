from copy import deepcopy
from random import randint

# Hard Rules
MAX_CONSECUTIVE_BLOCKS_PER_ANCHOR = 3
MAX_NUMBER_BLOCKS_PER_ANCHOR = 4

# Optimization
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


class Day(object):
    def __init__(self):
        self.blocks = []

    def __repr__(self):
        output = ''
        for block in self.blocks:
            output += str(block) + '\n'
        output += '\n'
        return output

    def number_blocks(self, **kwargs):
        """
        Returns number of blocks for an anchor, or the max of all anchors.

        kwargs:
            anchor = an Anchor() object
        """

        anchors = kwargs.get('anchor', ANCHORS_FULLTIME)
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
            anchor = an Anchor() object
        """

        anchors = kwargs.get('anchor', ANCHORS_FULLTIME)
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

    @property
    def complete(self):
        """Returns True if schedule is complete."""
        for block in self.blocks:
            if not block.full:
                return False
        return True

    @property
    def value(self):
        """Returns the optimization value of this schedule."""
        return 10



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
        self.base_schedule = schedule  # The Day to be scheduled
        self.possible_schedules = set()
        
        # How many iterations of scheduling to attempt
        self.max_iterations = kwargs.get('max_iterations', MAX_ITERATIONS_DEFAULT)
        self.fill_schedules()

    def fill_schedules(self):
        # Calculates max_num unoptimized schedules.
        # All schedules meet the minimum Hard Requirements
        iteration = 0

        while iteration <= self.max_iterations:
            schedule = deepcopy(self.base_schedule)
            
            [block.random_fill() for block in schedule.blocks]

            if schedule.safe_number_blocks and schedule.safe_consecutive_blocks:
                self.possible_schedules.add(schedule)

            iteration += 1



if __name__ == "__main__":
    day = Day()
    for i in range(1, 10):
        day.blocks.append(
            Block(
                hour=i
            )
        )

    s = ScheduleOptimizer(day)
    print(len(s.possible_schedules))
    print(s.possible_schedules)
    