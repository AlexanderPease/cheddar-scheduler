from constants import NORA, BRAD, BAKER, HOPE, TIM, KRISTEN
from models.anchor import Anchor
from models.schedule import Schedule, Block
from models.schedule_optimizer import ScheduleOptimizer


if __name__ == "__main__":
    
    blocks = [
        Block(hour=9),
        Block(hour=11, available_anchors=[HOPE, BRAD, TIM, KRISTEN, BAKER]),
        Block(hour=12, available_anchors=[BRAD, HOPE, KRISTEN, TIM]),
        Block(hour=2, available_anchors=[NORA, BRAD, HOPE, KRISTEN, TIM]),
        Block(hour=3, available_anchors=[NORA, BRAD, HOPE, KRISTEN, TIM]),
        Block(hour=4, available_anchors=[NORA, BRAD, HOPE, KRISTEN, TIM]),
        Block(hour=5, anchors= [NORA]),
    ]
    day = Schedule(blocks=blocks)


    s = ScheduleOptimizer(day)
    print(f'Generated {len(s.schedules)} schedules from {s.max_iterations} iterations')
    print('Best Schedule:')
    print(s.best_schedule)

    print('Other Schedules')
    print(s.schedules[1:5])
    