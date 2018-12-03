from constants import NORA, BRAD, BAKER, HOPE, TIM, KRISTEN, JIMMY
from models.anchor import Anchor
from datetime import datetime, timedelta

from models.schedule import Schedule, Block
from models.schedule_optimizer import ScheduleOptimizer


if __name__ == "__main__":
    blocks = [
        Block(
            name='Opening Bell',
            start=datetime(2018, 12, 3, 9),
            length=timedelta(hours=2)
        ),
        Block(
            start=datetime(2018, 12, 3, 11),
            available_anchors=[HOPE, BRAD, TIM, KRISTEN, BAKER]
        ),
        Block(
            start=datetime(2018, 12, 3, 12),
            length=timedelta(hours=2),
            available_anchors=[BRAD, HOPE, KRISTEN, TIM]),
        Block(
            start=datetime(2018, 12, 3, 14),
            available_anchors=[NORA, BRAD, HOPE, KRISTEN, TIM]
            ),
        Block(
            start=datetime(2018, 12, 3, 15),
            available_anchors=[NORA, BRAD, HOPE, KRISTEN, TIM]
        ),
        Block(
            name='Closing Bell',
            start=datetime(2018, 12, 3, 16),
            available_anchors=[NORA, BRAD, HOPE, KRISTEN, TIM]
        ),
        Block(
            name='Cheddar Sports',
            start=datetime(2018, 12, 3, 17),
            anchors=[NORA, JIMMY]
        )
    ]
    day = Schedule(blocks=blocks)
    s = ScheduleOptimizer(day)

    print(f'Generated {len(s.schedules)} schedules from {s.max_iterations} iterations')
    print('Best Schedule:')
    print(s.best_schedule)
    