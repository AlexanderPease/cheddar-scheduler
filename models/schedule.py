from datetime import timedelta
from random import randint
from time import strftime

from constants import (
    MAX_CONSECUTIVE_BLOCKS_PER_ANCHOR, 
    MAX_NUMBER_BLOCKS_PER_ANCHOR,
    ANCHORS_PER_BLOCK_DEFAULT,
    ANCHORS_FULLTIME
)


class Block(object):
    def __init__(self, start, **kwargs):
        """
        A single block of time.

        kwargs - Required
            start: a datetime object.

        kwargs - Optional
            length: a timedelta object, defaulst to 1 hour.
            name: name/description of the block.
            num_anchors: int number of anchors for this block, default 2.
            anchors: list of Anchor objects that definitely are working this block.
            available_anchors: list of Anchor objects that could work this block.
                Defaults to ANCHORS_FULLTIME.
        """
        self.start = start
        self.length = kwargs.get('length', timedelta(hours=1))
        self.name = kwargs.get('name')
        
        # Default 2 anchors per block
        self.num_anchors = kwargs.get('num_anchors', ANCHORS_PER_BLOCK_DEFAULT)

        # Default allow any FT anchor
        self.available_anchors = kwargs.get('available_anchors', ANCHORS_FULLTIME)

        # Optionally set a list of specific anchors
        self.anchors = set(kwargs.get('anchors', []))
        if len(self.anchors) > self.num_anchors:
            raise

    def __repr__(self):
        return f'Block: {self.name}; Time: {self.start.strftime("%-I %p")}; Anchors: {self.anchors}'

    @property
    def full(self):
        if len(self.anchors) > self.num_anchors:
            raise
        return len(self.anchors) == self.num_anchors
    
    def random_fill(self):
        """Randomly fills block with matching anchors."""
        while not self.full:
            self.anchors.add(
                self.available_anchors[ randint(0, len(self.available_anchors)-1) ]
            )
        return True


class Schedule(object):
    def __init__(self, blocks, **kwargs):
        self.blocks = blocks # must be an ordered list of Blocks
        self.available_anchors = kwargs.get('available_anchors', ANCHORS_FULLTIME)
        self.value = None

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


    def first_block_for(self, anchor):
        """Returns the first block for anchor."""
        for block in self.blocks:
            if anchor in block.anchors:
                return block

    def last_block_for(self, anchor):
        """Returns the first block for anchor."""
        for block in reversed(self.blocks):
            if anchor in block.anchors:
                return block

    def start_to_end_time(self, **kwargs):
        """
        Returns timedelta object from start block to end block
        for a specific anchor, or the max of all anchors.

        kwargs:
            anchors = a list of Anchor() objects
        """
        anchors = kwargs.get('anchors', self.available_anchors)
        time_max = timedelta(milliseconds=1)
        
        for anchor in anchors:
            start_block = self.first_block_for(anchor)
            end_block = self.last_block_for(anchor)
            if start_block:
                time = end_block.start + end_block.length - start_block.start
                time_max = max(time, time_max)
        
        return time_max
