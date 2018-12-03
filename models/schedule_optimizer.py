from copy import deepcopy
from constants import (
    WEIGHT_CONSECUTIVE_BLOCKS, 
    WEIGHT_NUMBER_BLOCKS, 
    WEIGHT_START_TO_END_BLOCKS, 
    WEIGHT_STARTING_TIME, 
    PENALIZE_LATER_THAN,
    MAX_ITERATIONS_DEFAULT
)


class ScheduleOptimizer(object):
    def __init__(self, schedule, **kwargs):
        self.base_schedule = schedule  # The day to be scheduled
        self.schedules = []
        
        # How many iterations of scheduling to attempt
        self.max_iterations = kwargs.get('max_iterations', MAX_ITERATIONS_DEFAULT)

        # Optimize schedules
        self.fill_schedules()
        self.value_schedules()
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

    def value_schedules(self, **kwargs):
        """
        Sets optimization value of all schedules.
        Lower values are more optimized.
        """
        for schedule in self.schedules:
            value = 0

            for anchor in schedule.available_anchors:
                value += schedule.number_blocks(anchors=[anchor]) * WEIGHT_NUMBER_BLOCKS
                value += schedule.consecutive_blocks(anchors=[anchor]) * WEIGHT_CONSECUTIVE_BLOCKS
                value += schedule.start_to_end_blocks(anchors=[anchor]) * WEIGHT_START_TO_END_BLOCKS

                # Weight before noon start time for all anchors
                start_block = schedule.start_block_for(anchor)
                if start_block and start_block.hour > PENALIZE_LATER_THAN:
                    value += (start_block.hour - PENALIZE_LATER_THAN) * WEIGHT_STARTING_TIME

            schedule.value = value

    @property
    def best_schedule(self):
        return self.schedules[0]